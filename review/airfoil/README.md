# Auditoría editorial y de integración: aeroelasticidad pasiva

Fecha: 17 de octubre de 2026. Proyecto: Passive Airfoil Aeroelasticity MATLAB,
MC-Andes. Portal base: `fdbcd5eb82d240678b72a62806bcfb7fb9b303ff`, rama `main`.
La revisión del código científico se fija en la ficha y en
`docs/assets/airfoil/evidence.json`; no se selecciona la última carpeta por fecha.

## Diagnóstico inicial y correcciones

| Problema observado | Corrección revisable |
| --- | --- |
| El proyecto no tenía ficha ni registro en el portal | Nueva ruta `projects/passive-airfoil-aeroelasticity/`, registro en navegación, catálogo y portada |
| El PR del proyecto describía 33 controles y la etapa anterior | Se actualizó el PR científico #4 con los desarrollos reales y 69 controles; el portal enlaza un commit exacto |
| No había relato científico ni recursos del álabe en el portal | Página autocontenida: fenómeno, hipótesis, ecuaciones explicadas, discretización, ejecución, resultados y límites |
| Los resultados locales no eran recursos web accesibles | Cinco figuras redibujadas, portada de video y MP4 H.264 silencioso de unos 200 kB, datos reducidos y hashes |
| Riesgo de confundir comparación bibliográfica con validación del CAD | Se separan controles analíticos, cilindro numérico, ensayos de placa y predicciones condicionales |
| El DOI de Malim devuelve 403 a este verificador automático | Se conserva el DOI como identificación y se enlaza el PDF institucional VUB, comprobado con HTTP 200 |
| El portal carecía de comprobación específica para esta ficha | Validador sin dependencias: registro, referencias locales, metadatos, licencias/hashes, dimensiones y video |
| Los PR solo compilaban y no archivaban el sitio | Se conserva el artefacto GitHub Pages también en PR; el despliegue sigue limitado a push en main |

No se modifican componentes globales innecesarios. La tipografía, el fondo,
los enlaces y la paleta proceden del tema actual. El CSS nuevo se limita a
figuras y ecuaciones de la ficha; la plantilla Open Graph solo se selecciona
en esta página.

## Fuentes y recursos

La ficha cita autores, títulos, publicaciones y enlaces persistentes para
Theodorsen (NACA 496), Malim et al. (Aerospace 2023), Morettini et al. (2022),
Huang–Zhang (Mendeley v2, 2026), Russell–Wang (JCP 2003) y del Carre et al.
(SHARPy, JOSS 2019). Incluye el enlace a la ficha metodológica de Sears y su
convención de fase. SHARPy y Russell–Wang no son motores del código propio.
No se reproduce ninguna figura editorial de esos trabajos.

`geometry.png` muestra la sección/malla; `convergence.png`, la respuesta a la
misma carga controlada; `free-response.png`, la perturbación calculada del TE;
`plate-comparison.png`, primer modo de nueve placas con medias/SD publicadas;
`viscous-wake.png`, la vorticidad media realmente calculada. `motion-poster.png`
y `posterior-motion.mp4` muestran la evolución de la piel posterior en sus
propias unidades. Cada recurso tiene texto alternativo o etiqueta accesible y
leyenda con configuración, interpretación y límites. La licencia MIT de los
recursos originales y CC BY 4.0 del derivado Huang–Zhang se registran en
`docs/assets/airfoil/LICENSE.txt`.

Los exportadores se versionan en el repositorio del proyecto:
`matlab/export_portal_fields.m` y `tools/export_portal_assets.py`.
Las dependencias opcionales de figuras se fijan en `tools/requirements-portal.txt`.
El solver sigue requiriendo MATLAB base. El STEP y los estados MAT voluminosos
no se redistribuyen.

## Verificación ejecutada

- Proyecto: `addpath('matlab'); run_verification();` en MATLAB R2026a Update 4:
  **69 controles pasan**, siete suites. Ejecutado de nuevo para esta publicación.
- Proyecto: `python3 tools/check_repository.py`: **274 archivos, 20 entradas
  con hash, 124 enlaces locales**; `git diff --check`, limpio.
- Portal: `mkdocs build --strict`: compilación limpia, sin warnings.
- Portal: `python tools/check_airfoil_page.py`: **51 referencias locales,
  15 recursos con hash y 241 estados de video**; metadatos, registro y
  dimensiones comprobados. `python -m py_compile tools/check_airfoil_page.py`
  y `git diff --check`, limpios.
- Enlaces externos: **18 URL con HTTP 200**, incluidas referencias y enlaces
  al commit científico exacto. Véase `external-links.json`. La URL pública
  nueva se evalúa por separado como despliegue pendiente, no como enlace ya publicado.
- Navegador real: escritorio **1440×1000**, móvil **390×844** y **360×800**;
  ancho de documento igual al viewport, sin desplazamiento horizontal global.
  Las cinco imágenes cargan; no se deforman y usan dimensiones intrínsecas.
- MP4 reproducido en el navegador: **8,033333 s**, 864×504, `readyState=4`,
  silencioso. Son 241 muestras reales de la ventana física 0–1,2 s, sin
  interpolar estados. No hay reproducción automática.
- Teclado: Tab alcanza el enlace Repositorio MATLAB con contorno visible.
  El navegador no registró errores ni avisos de consola durante la revisión.
  Texto #1a1a1a sobre fondo #faf9f7; las comparaciones usan símbolos distintos,
  además del color. No se afirma una auditoría WCAG completa.

Las [capturas de escritorio](desktop.jpg), [geometría en escritorio](desktop-geometry.jpg),
[resultados](desktop-results.jpg), [móvil](mobile.jpg),
[geometría móvil](mobile-geometry.jpg) y [video móvil](mobile-motion.jpg)
se guardan para revisión. `mobile-browser-check.json` conserva las comprobaciones
DOM de recursos y dimensiones.

## Despliegue y criterios pendientes

La página pública nueva devolvía **404** durante esta auditoría. Eso es
coherente con un cambio aún no integrado; no se declara desplegada. La
configuración efectiva de GitHub Pages usa Actions, y el último workflow
`docs` del portal base terminó con compilación y despliegue satisfactorios
(run `34781323111`). El PR ejecuta compilación y archiva el sitio, pero su
job `deploy` está condicionado a `push` en main.

La protección de `main` exige **una aprobación independiente**, también para
administradores. No se elimina esa protección ni se autoaprueba el cambio.
Tras aprobación e integración, revisar el job `deploy` y abrir
`https://mc-andes.github.io/projects/passive-airfoil-aeroelasticity/`:
comprobar HTTP 200, la navegación y al menos una figura y el MP4 en la página
real. La compilación local y el artefacto del PR no sustituyen esa comprobación.

## Información que debe confirmar el equipo y mantenimiento

1. Responsable individual, integrantes y colaboradores; la atribución
   corporativa MC-Andes es la única confirmada en CITATION.cff.
2. Material/proceso real, montaje y mecanismo de guía, datos experimentales
   de forma/frecuencias/presión/velocidad e incertidumbres.
3. Permiso y modalidad de distribución del CAD si se desea hacer reproducible
   toda la campaña fina desde un clon público.
4. Aprobar e integrar los PR y verificar el despliegue real; no equivale a
   confirmar científicamente las predicciones del espécimen.

Al integrar el PR #4 del proyecto, actualizar el estado editorial de esa
referencia; mantener el commit fijo o una release identificable. Al cambiar
cifras, regenerar datos, figuras, licencias y hashes juntos. Comprobar cada
nueva animación en móvil y con movimiento reducido; no introducir autoplay.
Revisar las referencias y URLs al actualizar una versión, sin sustituirlas por
búsquedas genéricas ni cambiar parámetros para mejorar artificialmente las
comparaciones.
