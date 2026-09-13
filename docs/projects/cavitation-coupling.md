---
description: Proyecto MC-Andes para transferir cargas de cavitación entre Basilisk y Kratos MPM con contratos HDF5 y verificación conservativa.
---

# Cavitación · Basilisk–MPM

**Del colapso de una burbuja a la carga sobre una pared.** El proyecto desarrolla
un intercambio reproducible entre el modelo fluido y la respuesta estructural,
con unidades, procedencia y comprobaciones de fuerza e impulso.

[Documentación](https://mc-andes.github.io/cavitation-coupling/){ .md-button .md-button--primary }
[Repositorio](https://github.com/MC-Andes/cavitation-coupling){ .md-button }

## Problema de investigación

Una burbuja que colapsa cerca de una superficie genera una carga transitoria.
El primer caso plantea una cavidad axisimétrica frente a una pared rígida en
Basilisk y transfiere su presión a una pared homogénea elástica en Kratos MPM.
La respuesta del sólido no regresa al fluido en este acoplamiento
unidireccional.

## Componentes

| Componente | Función |
| --- | --- |
| Basilisk | Formulación del problema fluido y de la presión de pared |
| HDF5 | Historia de cargas con anillos, tiempos, unidades y procedencia |
| Paquete Python | Mapeo y comprobación de fuerza e impulso |
| Kratos MPM | Solver estructural seleccionado y adaptador de fuerzas |
| ParaView | Inspección de la presión transferida y su evolución |

## Qué está publicado

El repositorio ofrece el contrato HDF5, un mapeador conservativo, un adaptador
para Kratos y exportación VTK. Los ejemplos sintéticos permiten verificar el
intercambio sin instalar los solvers externos.

!!! info "Investigación en desarrollo"
    Los ejemplos publicados verifican el software con cargas sintéticas.
    No representan un caso físico completo validado de cavitación ni una
    predicción de daño o erosión. Consulta el
    [alcance de la versión pública](https://mc-andes.github.io/cavitation-coupling/project-status/).

## Empezar y contribuir

- [Inicio rápido](https://mc-andes.github.io/cavitation-coupling/getting-started/):
  instalación y ejemplos con Python 3.11 o superior.
- [Formulación y transferencia](https://mc-andes.github.io/cavitation-coupling/coupling/):
  definición de cargas, unidades y conservación.
- [Contribución](https://github.com/MC-Andes/cavitation-coupling/blob/main/CONTRIBUTING.md):
  cambios mediante revisión y pruebas.
- [Citación](https://github.com/MC-Andes/cavitation-coupling/blob/main/CITATION.cff):
  identifica la versión del software y los solvers utilizados.

El paquete público usa licencia MIT. Las dependencias mantienen sus propias
licencias y reconocimientos en el repositorio.

[Volver al catálogo](../projects.md){ .md-button }
