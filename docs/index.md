# Mecánica computacional abierta y reproducible

**Investigación, software y formación**{ .course-kicker }

**MC-Andes** reúne herramientas, documentación y prácticas comunes para
investigar y enseñar mecánica computacional en la Universidad de los Andes.
Construimos resultados que puedan revisarse, ejecutarse y extenderse.

[Explorar proyectos](projects.md){ .md-button .md-button--primary }
[Comenzar un curso](courses.md){ .md-button }

<div class="grid cards" markdown>

- **Software verificable**

    ---

    Plantillas con lint, pruebas, documentación y revisiones obligatorias.

- **Investigación reproducible**

    ---

    Supuestos, datos, ejemplos y limitaciones documentados cerca del código.

- **Colaboración sostenible**

    ---

    Gobernanza clara, permisos mínimos y decisiones técnicas trazables.

</div>

## Aprende con MC-Andes

<div class="grid cards" markdown>

- **Curso destacado**{ .course-kicker }

    **FEniCSx/DOLFINx para mecánica computacional**

    ---

    Curso abierto y autocontenido en español: comienza con forma débil y un
    problema de Poisson; después abre rutas de calor, sólidos, fluidos y
    multifísica. Incluye trece lecciones y ejemplos verificables con ejecución
    serial/MPI en FEniCSx 0.11 y Python 3.12.

    No requiere inscripción, docente ni calificaciones: cada persona aprende y
    comprueba los resultados a su propio ritmo.

    [Entrar al curso](https://mc-andes.github.io/fenicsx-course/){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/fenicsx-course){ .md-button }
    [Release v0.1.1](https://github.com/MC-Andes/fenicsx-course/releases/tag/v0.1.1){ .md-button }

</div>

## Proyectos de investigación

<div class="grid cards" markdown>

- **Corte ortogonal de metales · MPM**

    ---

    Deformación plástica, contacto y calentamiento durante el avance de una
    herramienta. Un modelo termomecánico para estudiar la formación de viruta.

    **Estado:** desarrollo y verificación numérica; corte completo y validación
    experimental pendientes.

    [Ver el proyecto](projects/metal-cutting.md){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/Metal_cutting){ .md-button }

- **Cavitación · Basilisk–MPM**

    ---

    Del colapso de una burbuja a la respuesta de una pared. Un proyecto de
    transferencia conservativa de cargas entre Basilisk y Kratos MPM, con
    contratos HDF5 y ejemplos sintéticos de verificación.

    **Estado:** investigación en desarrollo; paquete público con ejemplos
    sintéticos de verificación.

    [Ver el proyecto](projects/cavitation-coupling.md){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/cavitation-coupling){ .md-button }

- **Aeroelasticidad pasiva · MATLAB**

    ---

    Deformación y vibración de un álabe fijo en aire, conservando el sólido
    original. FEM, VLM/UVLM y Navier–Stokes laminar propios.

    **Estado:** investigación en desarrollo; verificación numérica bajo
    hipótesis explícitas, sin validación experimental del espécimen.

    [Ver el proyecto](projects/passive-airfoil-aeroelasticity.md){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab){ .md-button }

- **Delaunay Mesher**

    ---

    Generación reproducible de geometrías y mallas partícula–matriz para
    mecánica computacional, con un ejemplo público y comprobaciones geométricas.

    **Estado:** desarrollo y verificación geométrica; validación experimental
    pendiente.

    [Ver el proyecto](projects/delaunay-mesher.md){ .md-button .md-button--primary }
    [Código](https://github.com/MC-Andes/Delaunay_mesher){ .md-button }

</div>

[Explorar el catálogo completo](projects.md){ .md-button }

## Encuentra tu punto de entrada

| Si quieres… | Empieza en… |
| --- | --- |
| aprender una herramienta científica | [Cursos autoguiados](courses.md) |
| reutilizar una base de software | [Proyectos y plantillas](projects.md) |
| conocer decisiones y avances | [Blog](blog/index.md) |
| proponer una mejora | [Guía para contribuir](contributing.md) |
| consultar las reglas comunes | [Estándares organizacionales](https://github.com/MC-Andes/standards) |

!!! info "Cómo leer el catálogo"
    Cada ficha distingue entre desarrollo, verificación y validación. Los
    resultados preliminares se presentan con sus supuestos, procedencia y
    limitaciones, sin tratarlos como evidencia experimental validada.
