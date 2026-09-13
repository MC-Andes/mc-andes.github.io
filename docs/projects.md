# Proyectos

Software y documentación para investigar y enseñar mecánica computacional.
Cada proyecto identifica su alcance, sus ejemplos y sus condiciones de uso en
el repositorio correspondiente.

## Investigación y herramientas

<div class="grid cards" markdown>

- **Cavitación · Basilisk–MPM**

    ---

    Transferencia conservativa de cargas de una burbuja próxima a una pared.
    Conecta la formulación fluida en Basilisk con fuerzas superficiales para
    Kratos MPM mediante un contrato HDF5.

    **Estado:** investigación en desarrollo; paquete público con ejemplos
    sintéticos de verificación.

    [Ver el proyecto](projects/cavitation-coupling.md){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/cavitation-coupling){ .md-button }

- **Delaunay Mesher**

    ---

    Generación reproducible de geometrías y mallas partícula–matriz para
    mecánica computacional.

    El repositorio reúne las instrucciones y el alcance de la herramienta.

    [Código y documentación](https://github.com/MC-Andes/Delaunay_mesher){ .md-button }

</div>

## Formación

El [catálogo de cursos](courses.md) reúne el material autoguiado de la
organización, incluido el curso de FEniCSx/DOLFINx en español.

## Infraestructura compartida

| Repositorio | Propósito |
| --- | --- |
| [standards](https://github.com/MC-Andes/standards) | Gobernanza, contribución, releases y seguridad |
| [template-python-mech](https://github.com/MC-Andes/template-python-mech) | Proyectos Python con pruebas y documentación |
| [template-cpp-mech](https://github.com/MC-Andes/template-cpp-mech) | Núcleos C++17 con CMake y pruebas |
| [template-docs](https://github.com/MC-Andes/template-docs) | Documentación técnica y GitHub Pages |

## Incorporar un proyecto

Sigue las [normas de MC-Andes](https://github.com/MC-Andes/standards) y propone
su ficha mediante un Pull Request. Incluye objetivo, estado, alcance, licencia
y enlaces que permitan ejecutar los ejemplos y revisar la evidencia publicada.
