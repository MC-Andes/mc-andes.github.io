# Auditoría editorial y técnica: Delaunay Mesher

## Diagnóstico y alcance

Proyecto confirmado por `origin`: MC-Andes/Delaunay_mesher. Portal:
MC-Andes/mc-andes.github.io, base `main` en `fdbcd5e`.
Rama de trabajo: `codex/delaunay-project-profile`.
La ficha faltaba: el catálogo solo enlazaba al código y la navegación no tenía entrada.
Se conservó el trabajo local de la campaña; no se enviaron trabajos Slurm ni se
modificaron productores, auditorías, contratos o resultados PI192.

El `main` público del proyecto (`04d3d362677397aeb290d77cb2a9d02959fd44c8`)
exporta el formato histórico `single_matrix`. No contiene `docs/contrato_vem.md`
ni el contrato PI192-v3 presente en el trabajo local. Publicar enlaces a esos
archivos en `main` produciría 404 y mezclaría versiones científicas.
No se promovió en bloque el trabajo de investigación al repositorio público.

## Cambios

- Ficha narrativa con problema, modelo geométrico, variables, hipótesis, unidades,
  condiciones pendientes, implementación, reproducción, resultados y limitaciones.
- Entrada en navegación y botón desde el catálogo, con estado consistente.
- Título, descripción y URL canónica mediante el mecanismo existente de MkDocs.
- Dos SVG originales, con ejes/leyendas y explicaciones fuera de la imagen;
  colores del portal y rayado para no depender solo del color.
- Ejemplo pequeño, configuración y comprobantes con hashes. Datos completos del
  ejemplo: 28 inclusiones, 214 nodos, 5700 mm², fracción 0,285 frente a 0,30.
- Separación explícita entre versión pública, investigación PI192, verificación
  geométrica, convergencia de solución y validación experimental.
- Referencias originales de Quey/Dawson/Barbe (2011), Geuzaine/Remacle (2009),
  manual oficial Gmsh y código fijado por SHA. Ninguna es una validación
  experimental de este proyecto. No se reutilizó arte gráfico externo.

## Verificación ejecutada

En el checkout público del proyecto, con Python 3.9 y NumPy 2.0.2:

```bash
python -m external_postprocess.cli generate-campaign \
  --config examples/external_campaign.json \
  --outdir /tmp/delaunay-portal-pinned \
  --case CA1_A2_G1_R01 --no-previews
python -m pytest -q -p no:cacheprovider \
  tests/test_external_config_sampling.py tests/test_external_shape_placement.py \
  tests/test_external_topology_export.py tests/test_external_validation_preview.py \
  tests/test_external_cli.py
```

Resultado: caso `ok`; 72 pruebas aprobadas. Repetición con NumPy fijado:
seis archivos coinciden por SHA-256 (`reproduction.json`). No se ejecutó un
solver estructural ni la suite completa de rutas Neper/Gmsh/PyBullet.

En el portal, con `mkdocs-material==9.6.18`:

```bash
python -m mkdocs build --strict
python3 scripts/delaunay/check_site.py
git diff --check
```

Resultado: compilación estricta aprobada; cero enlaces/fragmentos locales
faltantes en el sitio generado; los 12 enlaces/recursos externos comprobados
responden HTTP 200. El DOI de Wiley inicialmente respondió 403 al cliente
programático: se conserva como identificador textual y se enlaza el artículo
en el repositorio institucional de Lieja, que devuelve 200.

Chromium/Playwright: 1440×1000 y 390×844, carga de ambas figuras comprobada tras
desplazarse hasta ellas, cero errores JavaScript y ancho de documento igual al
viewport. Inspección visual de cabecera y figuras, textos alternativos, un H1,
URL canónica y enlace de salto accesible con Tab comprobados. Capturas completas
y de detalle en esta carpeta; resultados en `browser.json`. Tablas y bloques de
código conservan el desplazamiento interno de Material, sin desbordar la página.
No se afirma una auditoría WCAG completa.

## Publicación

Ruta prevista: https://mc-andes.github.io/projects/delaunay-mesher/
Antes de integrar el PR devuelve 404, como corresponde a una página nueva.
El portal existente `/projects/` devuelve 200 y GitHub Pages está configurado
con `build_type=workflow`. El workflow `.github/workflows/docs.yml` ejecuta
compilación en PR y despliega solo en `push` a `main`; no ofrece preview por PR.
La compilación local y la CI del PR no prueban un despliegue de esta nueva ruta.
El despliegue y su inspección pública quedan pendientes de revisión e integración.

## Pendientes y responsables

El equipo debe confirmar responsables individuales y colaboradores, licencia
del repositorio del proyecto, origen de parámetros materiales/granulometrías,
ensayo y datos experimentales con condiciones de reutilización, y publicación
versionada del contrato PI192-v3 con auditorías y resultados 3D. Faltan
verificación del solver VEM, comparación mecánica VEM–FEM y visto bueno del PI.
No se fabricaron esas evidencias ni se declaró completada la campaña.

La arquitectura actual no genera imágenes sociales por página; se verificaron
los metadatos que sí admite, sin añadir un servicio o dependencia global.
No hay video temporal: el ejemplo es estático. El proyecto no necesitó cambios
para reproducir este caso, por lo que este PR afecta únicamente al portal.

## Mantenimiento

- Conservar el SHA del ejemplo y la URL de la ficha; no reemplazar resultados
  históricos por métricas de una campaña diferente.
- Cuando se publique PI192, añadir una sección versionada con contrato, datos,
  licencia y auditorías, y volver a comprobar enlaces antes de actualizar cifras.
- Regenerar SVG con `python3 scripts/delaunay/render_figures.py` (NumPy y
  Matplotlib), comprobar los hashes y revisar ambas capturas de tamaño de pantalla.
- Ejecutar compilación estricta y el comprobador de enlaces en cada edición.
- Tras integrar, comprobar el workflow de despliegue y la URL pública en ambos
  tamaños. Registrar responsable y fecha de la revisión científica del PI.
