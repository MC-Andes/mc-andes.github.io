# Integración de Metal_cutting · revisión del 17 de octubre de 2026

## Diagnóstico y alcance

El portal no registraba Metal_cutting en catálogo, navegación ni página propia;
la ruta prevista respondía HTTP 404. El README del código presentaba únicamente
PFEM/Kratos, mientras que RUN_MPM.md y los módulos publicados contienen un MPM
propio que no requiere Kratos. Se inspeccionó el código público 6026aef y se
preservó el trabajo local de investigación, sin incorporarlo masivamente al Git.

El contenido de la ficha distingue esa publicación de los resultados locales
históricos y de las formulaciones locales posteriores. El único resultado nuevo
ejecutado para esta revisión es un arranque mínimo sin aceptación numérica.

## Cambios y fuentes

- Página `projects/metal-cutting/`, registrada en MkDocs y el catálogo.
- Narración de problema, hipótesis, balances, constitutiva, discretización,
  integración, reproducción y alcance de los resultados.
- Título, descripción, URL canónica, búsqueda y sitemap comprobados. El portal
  no tiene configurada generación de imágenes sociales; no se atribuye esa
  funcionalidad a estos metadatos.
- Jaspers 1999 y Klippel et al. 2024 como fuentes del material y futura comparación.
  Nairn 2015, Cortis et al. 2018 y Coombs et al. 2020 como antecedentes numéricos,
  sin atribuirles una validación de esta implementación.
- Corrección separada de la entrada del código:
  https://github.com/MC-Andes/Metal_cutting/pull/2.
  La ficha del portal no depende de su merge para resolver los enlaces existentes.

## Recursos visuales

- `geometry.svg`: esquema original de la configuración inicial; no es una solución.
- `discretization.svg`: esquema original Q4/B2; no es evidencia de convergencia.
- `plasticity.mp4` y `temperature.mp4`: renderizados desde los mismos 25 estados
  históricos autenticados, sin interpolación ni modificación de geometría.
  Campo medio de cuatro puntos de integración por dominio; no máximos puntuales.
- Dos pósteres de su último estado. Controles, reproducción silenciosa y sin
  autoplay. Los dos paneles se apilan en móvil.
- `provenance.json`: tiempos, hashes de entrada y salida, límites de color y
  `accepted=false`; sin rutas privadas. Datos NPZ y archivo completo de fuentes
  históricos aún no publicados. El script de renderizado deja explícita esa
  dependencia; el manifiesto no pretende sustituir el archivo de datos.
- Títulos y explicación en HTML; se conservan únicamente ejes, unidades y barras
  en los gráficos. Los medios se generan a partir de resultados, sin IA generativa.

## Verificaciones ejecutadas

Desde el checkout del portal:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_site_links.py site
git diff --check
```

Construcción estricta correcta; 16 HTML y 434 referencias locales sin errores.
La advertencia promocional de MkDocs Material acerca de una futura versión 2.0
no es un error de construcción. No se alteraron dependencias para silenciarla.
El nuevo comprobador se ejecuta también en el workflow de documentación.

Chrome Headless Shell mediante Playwright: escritorio 1440×1000 y móvil 390×844.
Se comprobaron título, descripción, canonical, carga de SVG, dimensiones de video,
reproducción/posicionamiento, controles, ausencia de autoplay/sonido y de errores
JavaScript, navegación desde el catálogo, foco por teclado y ausencia de
horizontal overflow. Los detalles están en `browser-checks.json` y las capturas.
Esto no representa una certificación completa WCAG ni prueba de todos los navegadores.
Para repetir esta revisión, con Playwright y Chromium headless instalados, servir
`site` en el puerto 8765 y ejecutar `node scripts/check_metal_cutting_browser.cjs`.

Enlaces externos: `external-links.json`. Catorce respuestas HTTP 200; el DOI de
Cortis recibe HTTP 403 en la comprobación automática. El registro y el texto del
artículo se verificaron en la página primaria de Wiley; el rechazo automatizado
se conserva como limitación, no se presenta como HTTP 200.

En una copia de los 70 archivos públicos de Metal_cutting, con dependencias ya
instaladas y compilación nativa nueva:

- `prepare` robust: cuatro familias nativas compiladas; PASS.
- `check`: PASS.
- `run` con h=100 µm, hm=25 µm, máximo=100 ns, inicio=25 ps, final=50 ps,
  presupuesto=30 s y un hilo: dos pasos, cero rechazos, sin fallo de ejecución.
  `completed_unverified`, `accepted=false`, defecto energético 49,9855 %.
- `python -B -m unittest discover -s tests -v`, entorno activado: 2/2 PASS.
  Cubren generación y posproceso sintético; no verifican el solver completo.

Entorno: macOS ARM64, Python 3.12.14, NumPy 2.5.2, SciPy 1.18.1, pybind11 2.13.6,
Apple Clang 21. No se probó una instalación pip nueva del modelo ni portabilidad
a Linux/Windows. Los tests de generación se ejecutaron en copia para preservar
los casos originales. Los comandos completos de arranque figuran en la página.

## Publicación y límites de cierre

El workflow existente construye PRs y sólo despliega pushes a main. Se verificó
la configuración GitHub Pages (`build_type=workflow`), el último despliegue de
main exitoso y la portada pública HTTP 200. Esto **no valida el despliegue de esta
ficha**, cuya URL pública sigue pendiente del merge y del job de despliegue:

https://mc-andes.github.io/projects/metal-cutting/

No existe preview pública configurada por PR. La vista local está disponible en
http://127.0.0.1:8765/projects/metal-cutting/ durante esta revisión. Las capturas
permiten revisar el resultado sin habilitar un servicio externo. La aprobación
de otro mantenedor y el merge permanecen pendientes conforme a CONTRIBUTING;
no se modificaron permisos ni se aprobó el propio PR.

## Información pendiente y mantenimiento

1. Equipo: confirmar responsable científico, autores/colaboradores y licencia
   del código; añadir un archivo de citación en el repositorio del modelo.
2. Datos: depositar los NPZ y las fuentes históricas con sus hashes para que
   los videos puedan regenerarse sin acceso al equipo original.
3. Ciencia: completar balances y controles espaciales/temporales antes de
   comparar un ensayo identificado de Klippel; publicar fuerzas y espesor con
   unidades, ancho representado e intervalo de comparación.
4. Software: revisar etiquetas heredadas del JSON y opciones de enlace nativas
   antes de anunciar portabilidad. No cambiar parámetros sólo para aprobar controles.
5. Portal: mantener el identificador de código revisado, el manifiesto y las
   leyendas sincronizados con cada nuevo resultado; conservar la URL estable.
6. Tras el merge: exigir éxito del job `deploy`, abrir la URL pública y comprobar
   ambos MP4, la navegación móvil y la respuesta de recursos. Si falla, registrar
   el job y error; no atribuir éxito de despliegue al build local.
