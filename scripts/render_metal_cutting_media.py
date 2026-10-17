#!/usr/bin/env python3
"""Render two public illustrations from the authenticated 25-state MPM prefix.

Usage: python scripts/render_metal_cutting_media.py SOURCE_DIRECTORY OUTPUT_DIRECTORY
Dependencies: numpy, matplotlib, imageio-ffmpeg. No simulation is executed.
SOURCE_DIRECTORY must contain the original case.json, source_identity.json,
source_archive/, initial.npz and state_00001.npz through state_00024.npz.
The original NPZ data and archived solver sources are not distributed here.
Use --overwrite to replace this script's five generated media/provenance files.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True

import imageio_ffmpeg
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter
from matplotlib.collections import LineCollection, PolyCollection


SOURCE_SHA256 = "3bcccf4fb6b6d10153f68e238c2c771ff8df0bb5065d7522404427a4d714a22a"
CASE_SHA256 = "2846a9e5f8664034502af32e681167433af4b3f99c29102d5cb388efa182987b"
IDENTITY_SHA256 = "6243ff630818199cbfa70d7fb3a8cabfcb8331275a7f3d9631da3690fe80ec22"
# Independently authenticated historical index; names deliberately omit private paths.
INPUT_SHA256 = (
    "10f6d7d731e793662525868dd220fe7abbd4900204a8b4e7c890626c032ad343",
    "601e1ff8a651518f4d5fdcf28aa1298e7da6b7f2830f750c121ef7edbe47d0d7",
    "716275a89fd15b2ddfe687b4fc07e113ec7983fcde7b46303edf17ae173454a9",
    "e713d9d2e126bd7e517e0da9f332c3eefc95fdc9f5b8c7e6b29adbb529eea9eb",
    "960f26bae28282e8b2823eeaed312d2ad95372c4f62d035ef3c2f403a61744db",
    "ea5ffeb75921f45e7addbbba4a4c40c14ec0f67bd3880fef35a476fb6a29bc74",
    "3792644e82c654bcf5a846a7709f8f10094ceeedbd9075cb47e766f54cb7610c",
    "03dbad15e557bfff1339b3a75d1e089709c05d678d5a5a22ea97ee3323dee43d",
    "9bd18b95ace5dc2af4f0c33aacb76a5c71d6237c0ba4bee1ea246da64ab049bb",
    "cd68d89cd5b422026f40b40cbf73141d816053588e696365596f34fd5a3bec4e",
    "def1ba399189f6ee2703d82311d26e5d7a3bccdc3aabe416d2d8db6024ddd07f",
    "95c0726ac904a3b9314f346641995b0eaeee75460ac7392d2be659e760fcf386",
    "a19c719c275c2ed92d70ac66997da32e7f51ea0dbedc5960798c7a9c00b0bef0",
    "0668c86de3f84c1d3fe08e5140a88f0144a198f59d11666b2137602b7c95d4f0",
    "5e0edb5bd1cc7ab685bb2bde4faede483bf0cc84469caeb33f9f2eb872ccf92d",
    "f53652e5208b4b42e573add37f3eddd1f012cf472fc0674603a7060653388f17",
    "c308240c99cef088d85da4c665c4c3e9aeb5022a2f2fe46f1bb4e4563cefca74",
    "94a6eabdb2dc7ca5f627b424ca49868acb01b56a5277ab0faa9eef9b1a7067e5",
    "5cbbacffde444e71f32fd7a49c31ca48258d0c31809e8d6cc08a5e2ccf641500",
    "d09c23550d837edcf8ac44ed21b38c37330551db2b49163899f9175c77b130cd",
    "037f499e5acf7ec45ab2e3f002c1faa3889996a558d4ac4c6873d56f12d8fb45",
    "f261bcce6ab9c5181d0fe0643f3521c0d44f02a91c95c0906d622a9f850655ef",
    "07a509987ac08f897568682f5d98270ce4196eefcfe5c8d7f12ea79a8bc59b9e",
    "961c614dea90324cf6710320e04aa37ccc17857e5a224d035ac1a81c6b29036a",
    "92316a1f03f4e689994e2b1b4fba6fdb546987e96b30bf29ca95c6d2cd8fe09a",
)
PRODUCTS = ("plasticity.mp4", "temperature.mp4", "plasticity.png", "temperature.png", "provenance.json")
FPS = 3
DPI = 120
SIZE_PX = 768
CONTROL_MARGIN_PX = 160
HEIGHT_PX = SIZE_PX + CONTROL_MARGIN_PX


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_hash(path: Path, expected: str) -> None:
    if sha256(path) != expected:
        raise ValueError(f"Authenticated input differs: {path.name}")


def load_inputs(source: Path):
    require_hash(source / "case.json", CASE_SHA256)
    require_hash(source / "source_identity.json", IDENTITY_SHA256)
    case = json.loads((source / "case.json").read_text())
    identity = json.loads((source / "source_identity.json").read_text())
    if identity["source_sha256"] != SOURCE_SHA256:
        raise ValueError("Unexpected archived runtime identity")
    archive = source / "source_archive"
    dependencies = ("cutting2d/__init__.py", "cutting2d/cases.py", "cutting2d/config.py",
                    "scripts/klippel_material_cards.py", "scripts/rounded_tool_geometry.py")
    for name in dependencies:
        require_hash(archive / name, identity["files"][name])
    # This imports only authenticated geometry/configuration helpers, never a solver.
    sys.path.insert(0, str(archive))
    cases = importlib.import_module("cutting2d.cases")
    for name in ("cutting2d.cases", "cutting2d.config", "scripts.rounded_tool_geometry",
                 "scripts.klippel_material_cards"):
        module = sys.modules[name]
        relative = Path(module.__file__).resolve().relative_to(archive.resolve()).as_posix()
        require_hash(Path(module.__file__), identity["files"][relative])
    frames, entries = [], {}
    cells = None
    for number, digest in enumerate(INPUT_SHA256):
        name = "initial.npz" if number == 0 else f"state_{number:05d}.npz"
        path = source / name
        require_hash(path, digest)
        with np.load(path, allow_pickle=False) as data:
            if str(data["formulation"]) != "MPM_shared_domain_B2_four_persistent_GP_v1":
                raise ValueError("Expected shared-material-domain MPM states")
            time_s = float(data["time_s"])
            if abs(time_s - number * 2.4e-6) > 8 * np.spacing(max(time_s, 2.4e-6)):
                raise ValueError("Unexpected physical snapshot time")
            current_cells = data["cells"].copy()
            if cells is None:
                cells = current_cells
            elif not np.array_equal(current_cells, cells):
                raise ValueError("Material connectivity changed within the prefix")
            q = data["q"].copy()
            fields = {key: data[key].reshape(-1, 4).mean(axis=1) for key in ("alpha", "T")}
            if any(not np.isfinite(value).all() for value in (q, *fields.values())):
                raise ValueError("Nonfinite geometry or displayed field")
            if any(len(value) != len(cells) for value in fields.values()):
                raise ValueError("Expected four persistent Gauss points per material cell")
            grid_h = float(data["grid_h_m"])
            material_h = float(data["material_h_m"])
        frames.append({"time_s": time_s, "q": q, **fields})
        entries[name] = {"sha256": digest, "bytes": path.stat().st_size, "time_s": time_s}
    edges = np.concatenate([cells[:, [i, (i + 1) % 4]] for i in range(4)])
    unique, counts = np.unique(np.sort(edges, axis=1), axis=0, return_counts=True)
    return case, cases.make_tool, frames, cells, unique[counts == 1], entries, grid_h, material_h


def render(source: Path, output: Path, overwrite: bool = False) -> dict:
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not overwrite and any((output / name).exists() for name in PRODUCTS):
        raise FileExistsError("Generated media exist; pass --overwrite to replace these five files")
    case, make_tool, frames, cells, boundary, inputs, grid_h, material_h = load_inputs(source)
    config = SimpleNamespace(geometry=SimpleNamespace(**case["geometry"]))
    speed = config.geometry.tool_speed
    last_time = frames[-1]["time_s"]
    xlim = (-50., max(last_time * speed * 1e6 + 220., 300.))
    ylim = (350., max(max(float(frame["q"][:, 1].max()) * 1e6 for frame in frames) + 50., 740.))
    ffmpeg = Path(imageio_ffmpeg.get_ffmpeg_exe())
    matplotlib.rcParams["animation.ffmpeg_path"] = str(ffmpeg)
    plt.rcParams.update({"font.size": 17, "axes.labelsize": 19,
                         "xtick.labelsize": 16, "ytick.labelsize": 16,
                         "font.family": "DejaVu Sans", "figure.facecolor": "white"})
    metadata = {}
    with tempfile.TemporaryDirectory(prefix=".render-", dir=output) as temporary:
        work = Path(temporary)
        for stem, field, cmap, label in (
            ("plasticity", "alpha", "viridis", "Deformación plástica equivalente\n(adimensional)"),
            ("temperature", "T", "inferno", "Temperatura (K)"),
        ):
            limits = (min(float(frame[field].min()) for frame in frames),
                      max(float(frame[field].max()) for frame in frames))
            fig, ax = plt.subplots(figsize=(SIZE_PX / DPI, HEIGHT_PX / DPI), layout="constrained")
            # Preserve the original 768x768 scientific region above a white strip.
            # Native browser video controls can occupy this strip without covering data.
            fig.get_layout_engine().set(rect=(0., CONTROL_MARGIN_PX / HEIGHT_PX,
                                              1., SIZE_PX / HEIGHT_PX))
            art = PolyCollection([], array=np.array([]), cmap=cmap, clim=limits,
                                 edgecolors="none", antialiaseds=False)
            outline = LineCollection([], colors="#263342", linewidths=.65, zorder=3)
            ax.add_collection(art)
            ax.add_collection(outline)
            tool_artist = ax.fill([], [], facecolor="#aeb8c2", edgecolor="#4d5965", linewidth=1., zorder=4)[0]
            ax.set(xlim=xlim, ylim=ylim, aspect="equal", xlabel="x (µm)", ylabel="y (µm)")
            ax.axhline((config.geometry.height - config.geometry.uncut_thickness) * 1e6,
                       color="#6d8495", lw=.7, ls=":", zorder=0)
            fig.colorbar(art, ax=ax, location="bottom", label=label, shrink=.96, pad=.03)
            writer = FFMpegWriter(fps=FPS, codec="libx264", metadata={},
                                 extra_args=["-pix_fmt", "yuv420p", "-crf", "22", "-preset", "slow", "-movflags", "+faststart"])
            with writer.saving(fig, work / f"{stem}.mp4", dpi=DPI):
                for frame in frames:
                    art.set_verts(frame["q"][cells] * 1e6)
                    art.set_array(frame[field])
                    outline.set_segments(frame["q"][boundary] * 1e6)
                    tool = make_tool(config, frame["time_s"])
                    polygon = np.array([*tool.vertices[1:], *[
                        tool.boundary_point(i / 160)[0] for i in range(160, -1, -1)]]) * 1e6
                    tool_artist.set_xy(polygon)
                    writer.grab_frame()
            # The figure still contains the last computed frame, not a fabricated state.
            fig.savefig(work / f"{stem}.png", dpi=DPI, metadata={"Software": "Matplotlib"})
            plt.close(fig)
            check = subprocess.run([str(ffmpeg), "-v", "error", "-xerror", "-i", str(work / f"{stem}.mp4"),
                                    "-f", "null", "-"], capture_output=True, text=True, check=False)
            if check.returncode:
                raise RuntimeError(f"Video decoding failed for {stem}: {check.stderr}")
            metadata[stem] = {"field": field, "unit": "1" if field == "alpha" else "K",
                              "colormap": cmap, "color_limits": list(limits),
                              "decoded_successfully": True, "poster_state": "state_00024.npz"}
        # Protect against concurrent input changes; no altered prefix is published.
        for name, entry in inputs.items():
            require_hash(source / name, entry["sha256"])
        files = {name: {"bytes": (work / name).stat().st_size, "sha256": sha256(work / name)}
                 for name in PRODUCTS if name != "provenance.json"}
        times = [frame["time_s"] for frame in frames]
        manifest = {
            "schema": "metal-cutting-portal-media-v1", "accepted": False,
            "origin": "Historical 25-state prefix of shared-material-domain MPM, V7",
            "formulation": "MPM_shared_domain_B2_four_persistent_GP_v1",
            "source_sha256": SOURCE_SHA256,
            "case": {"name": "Ck45 bibliographic material approximation", "sha256": CASE_SHA256,
                     "tool_speed_m_s": speed, "background_spacing_m": grid_h,
                     "material_spacing_m": material_h},
            "inputs": inputs, "npz_data_published": False, "archived_solver_sources_published": False,
            "frame_count": len(frames), "frame_times_s": times,
            "physical_time_interval_s": [times[0], times[-1]],
            "advance_interval_m": [times[0] * speed, times[-1] * speed],
            "frames_per_second": FPS, "playback_duration_s": len(frames) / FPS,
            "temporal_interpolation": False, "geometry_interpolation_or_repair": False,
            "geometry": "Actual q/cells; equal-axis plot; original rounded-tool geometry",
            "field_display": "Arithmetic mean of four persistent Gauss points per material domain",
            "plot_limits_um": {"x": xlim, "y": ylim}, "fields": metadata,
            "layout": {"scientific_region_px": [0, 0, SIZE_PX, SIZE_PX],
                       "bottom_white_control_margin_px": CONTROL_MARGIN_PX,
                       "note": "Blank margin reserved for native video controls; no field or geometry is cropped."},
            "limitations": [
                "Diagnostic prefix only; no accepted developed chip or completed 500 micrometre cut.",
                "No experimental validation or calibration is claimed.",
                "Cell-mean colours are not pointwise maxima and conceal intra-cell variation.",
                "Playback time differs from physical time; chronology is specified in frame_times_s.",
                "Titles and timestamps are intentionally outside the videos; accompanying captions must retain this scope.",
                "The source NPZ data and solver archive are not published with these derived visualisations.",
            ],
            "encoding": {"codec": "H.264/libx264", "pixel_format": "yuv420p", "crf": 22,
                         "preset": "slow", "faststart": True, "width": SIZE_PX, "height": HEIGHT_PX,
                         "audio": False, "ffmpeg_binary_sha256": sha256(ffmpeg),
                         "ffmpeg_version": subprocess.check_output([str(ffmpeg), "-version"], text=True).splitlines()[0]},
            "renderer": {"file": "render_metal_cutting_media.py", "sha256": sha256(Path(__file__)),
                         "python": platform.python_version(), "numpy": np.__version__,
                         "matplotlib": matplotlib.__version__, "imageio_ffmpeg": imageio_ffmpeg.__version__,
                         "command": "python scripts/render_metal_cutting_media.py SOURCE_DIRECTORY OUTPUT_DIRECTORY"},
            "files": files,
        }
        (work / "provenance.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        for name in PRODUCTS:
            (work / name).replace(output / name)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = render(args.source_directory, args.output_directory, args.overwrite)
    print(json.dumps({"accepted": result["accepted"], "files": result["files"]}, indent=2))
