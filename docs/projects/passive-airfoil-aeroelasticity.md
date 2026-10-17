---
template: airfoil-project.html
title: Aeroelasticidad pasiva de un álabe · MATLAB
description: Cómo se deforma y vibra un álabe flexible fijo en aire. FEM Tet10, VLM/UVLM y Navier–Stokes propios, verificación numérica y límites experimentales explícitos.
---

# Aeroelasticidad pasiva de un álabe

**Passive Airfoil Aeroelasticity MATLAB**{ .course-kicker }

Una pieza flexible puede cambiar de forma por la propia acción del aire. Ese
cambio modifica a su vez la carga aerodinámica: la estructura y el flujo se
influyen mutuamente. El proyecto estudia esta realimentación en el borde
posterior de un álabe **fijo en una corriente de aire**, conservando su
geometría sólida e interfaces internas.

El objetivo es distinguir una deformación útil de una respuesta vibratoria que
pueda comprometer el funcionamiento. Antes de proponer un diseño o un umbral
de inestabilidad, hace falta separar tres preguntas: si las ecuaciones se
resuelven correctamente, cuánto cambian los resultados al refinar la
simulación y cuánto representan a una pieza impresa real.

[Repositorio MATLAB](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab){ .md-button .md-button--primary }
[Informe técnico](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/docs/cad-original-results.md){ .md-button }
[Ejemplos y documentación](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/docs/index.md){ .md-button }

!!! info "Investigación en desarrollo · verificación numérica"
    La campaña del 17 de octubre de 2026 pasa **69 controles** del software y
    los criterios numéricos principales del modelo condicional. No dispone de
    caracterización del espécimen, mediciones de presión o una validación
    experimental del álabe. El código ampliado está en
    [revisión en el PR #4](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/pull/4).
    Las figuras de esta página son resultados numéricos, salvo la comparación
    con datos modales identificada expresamente.

**Equipo y licencia.** El software y esta síntesis se atribuyen a
[MC-Andes](https://github.com/MC-Andes), comunidad de mecánica computacional de
la Universidad de los Andes. La citación del repositorio identifica a MC-Andes
como autor colectivo. El responsable individual, los integrantes y los
colaboradores de este estudio requieren confirmación del equipo; los autores
citados abajo son fuentes bibliográficas, no integrantes del proyecto.
El código propio tiene licencia MIT. Los datos modales externos conservan
CC BY 4.0.

## De la geometría a la pregunta física

El CAD original contiene un único sólido conectado, con nervaduras, huecos y
una barra interna candidata a guía. Su cuerda es **c = 0,247 m** y la
extrusión tiene **b = 0,360 m** de envergadura. Las pieles posteriores son
finas: su flexibilidad puede concentrar el movimiento aunque el conjunto
parezca rígido a simple vista.

La sección siguiente muestra la discretización de una tapa del sólido
original. Los espacios blancos pertenecen a sus cavidades. El rayado marca
el apoyo supuesto; no representa un montaje medido.

<figure class="airfoil-figure">
  <img src="../../assets/airfoil/geometry.png" alt="Malla triangular de la sección original del álabe, con cavidades y nervaduras; región x/c menor o igual a 0,30 rayada como apoyo supuesto." width="1164" height="263" loading="eager">
  <figcaption>Sección del CAD y malla superficial de preparación. Los ejes x/c y z/c son posición en cuerda y altura normalizadas por la cuerda. La familia sólida fina tiene 232.452 tetraedros Tet10 y 1.134.945 grados de libertad. La figura permite reconocer las cavidades sin sustituir la estructura por una placa.</figcaption>
</figure>

Se usa x para la cuerda, y para la envergadura y z para la altura.
La coordenada η recorre la envergadura entre 0 y 1; TE designa el borde de
salida. Los sensores siguen puntos materiales, en lugar de volver a buscar un
punto distinto cuando la estructura se deforma.

La pieza se estudia con tres hipótesis de guía: **A**, sólido monolítico;
**B**, seis coordenadas rígidas medias de la barra bloqueadas; **C**,
traslación media en cuerda libre y las otras cinco bloqueadas. No se separan
artificialmente las uniones del CAD ni se da por identificado un contacto
real. El apoyo primario fija los desplazamientos para x/c ≤ 0,30, y la
orientación gravitatoria primaria supone envergadura vertical. Los puertos de
las cavidades estructurales se suponen abiertos a ambiente. La gravedad se
evalúa por separado en el modelo lineal; las respuestas de flujo se expresan
respecto a la referencia sin flujo.

## Qué modelo conecta el aire con la deformación

La referencia material del sólido es un sustituto bibliográfico de Tough PLA:
E = 2,617 GPa, densidad ρₛ = 1.160 kg/m³ y coeficiente de Poisson supuesto
ν = 0,35. No son mediciones de esta impresión. El amortiguamiento modal
primario ζ = 0,008 también es una hipótesis; se estudia su sensibilidad.
Las fichas de [hipótesis y fuentes](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/cases/cad_original/assumptions.json)
distinguen estos valores de los datos confirmados del CAD.

Para los movimientos pequeños de la campaña principal, el equilibrio dinámico
se escribe de forma compacta:

<div class="airfoil-equation" role="math" aria-label="M por aceleración más C por velocidad más K por desplazamiento igual a fuerza aerodinámica más gravedad">M ü + C u̇ + K u = f<sub>aire</sub>(u, u̇, historia) + f<sub>g</sub></div>

Aquí u reúne los desplazamientos nodales; M representa la inercia, C la
disipación supuesta y K la rigidez. La fuerza del aire depende de la forma y
del movimiento actuales, y de la circulación emitida a la estela. Por eso una
presión sinusoidal impuesta no equivale a calcular la respuesta aeroelástica.
El código incluye además un sólido total Lagrangiano para verificar rotaciones
y deformaciones finitas; la campaña primaria utiliza la aproximación lineal.

El **VLM** aproxima el flujo exterior adherido e incompresible mediante
vórtices sobre una superficie media obtenida de las pieles reales. Su extensión
**UVLM** emite circulación a la estela, impone las condiciones de Kutta y
Kelvin e incluye el término no estacionario de Bernoulli. Las fuerzas y los
desplazamientos se intercambian mediante operadores adjuntos: el trabajo
virtual transferido al sólido coincide con el del lado fluido. La malla
fluida y la sólida pueden tener resoluciones distintas. Se impone no
penetración en la superficie media. La campaña principal convecta la estela
con la corriente uniforme; no presupone un enrollamiento libre validado.

Este flujo potencial no describe rozamiento, separación o turbulencia. La
rama **Navier–Stokes laminar** calcula por separado velocidad, presión y
vorticidad en una malla cartesiana escalonada. Impone incompresibilidad y
una frontera inmersa mediante penalización de Brinkman acoplada a presión.
En términos físicos:

<div class="airfoil-equation" role="math" aria-label="Divergencia de velocidad igual a cero; aceleración del fluido igual a gradiente negativo de presión dividido por densidad más difusión viscosa y fuerza de frontera">∇·v = 0 &nbsp;;&nbsp; ∂v/∂t + (v·∇)v = −∇p/ρ + ν<sub>f</sub>∇²v + f<sub>frontera</sub></div>

La primera ecuación conserva el volumen de fluido. En la segunda, el cambio de
velocidad responde a presión, viscosidad y acción de la frontera. La viscosidad
cinemática ν<sub>f</sub> del aire es distinta del coeficiente de Poisson ν del
sólido. El dominio viscoso es una caja periódica con franjas de relajación que
restablecen la corriente lejos del cuerpo; la adherencia en la pared se
aproxima mediante la penalización. El caso 2D mostrado usa x/c = −2…5 y
z/c = −1,75…1,75, con reinicios de estados calculados para prolongar el
transitorio. No representa por sí solo un dominio exterior infinito.
El número de Reynolds **Re = Uc/ν<sub>f</sub>** compara transporte
inercial y difusión viscosa: cambiar U cambia el problema físico, no solo la
escala de una gráfica.

## Cómo se resuelve y qué se necesita para repetirlo

| Componente | Desarrollo y función |
| --- | --- |
| MATLAB R2026a base | FEM Tet4/Tet10 y placa MITC4, modos, Newmark, transferencia, VLM/UVLM, FSI fuerte y Navier–Stokes MAC 2D/3D propios |
| Python, Gmsh y OpenCASCADE | Preparación y auditoría geométrica, mallas y proyección de nodos al CAD; no resuelven FEM o CFD |
| C opcional | Acelera el mismo núcleo Biot–Savart; existe alternativa MATLAB comprobada |
| MATLAB y Python de posprocesamiento | Figuras y tablas; el exportador editorial usa NumPy, Matplotlib, h5py y FFmpeg |
| JSON, CSV y MAT | Contratos y configuración; mallas y tablas; matrices, estados e historia numérica |

El código se organiza en `+fem3d`, `+pae`, `+uvlm`, `+fsi`, `+nsflow` y `+cad`;
los paquetes no requieren un solver estructural o fluido externo. Las pruebas
se encuentran en `matlab/tests/`, y las entradas trazables en `data/` y `cases/`.
[SHARPy](https://joss.theoj.org/papers/10.21105/joss.01885) es una referencia de
arquitectura aeroelástica, no el motor de esta implementación.

Una secuencia del cálculo acoplado es: malla sólida → modos y corrección
estática → superficie aerodinámica y transferencia → equilibrio deformado →
perturbación libre → actualización de circulación y estela → fuerzas → nueva
respuesta estructural. En el control no lineal se itera dentro de cada paso;
la campaña tangente usa una eliminación algebraica equivalente sin truncar la
historia de circulación.

Para reproducir controles pequeños no hacen falta el STEP privado, Python ni
herramientas CAD. Clona el repositorio y utiliza la revisión exacta que generó
la publicación:

```bash
git clone https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab.git
cd passive-airfoil-aeroelasticity-matlab
git checkout 28bb2fca284d31edb99968ddd7c75f83982774ef
matlab -batch "addpath('matlab'); run_verification(); run_tail_benchmarks();"
```

El resultado esperado es `Verification passed: 69 total checks across seven
physics suites.` y tablas/figuras del benchmark de placas en `results/`.
Las pruebas incluyen soluciones analíticas e invariantes; no ejecutan cada vez
la campaña fina del CAD. La [guía de reproducción](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/docs/cad-original.md)
explica las dependencias adicionales, mallas y presupuesto de la campaña
completa. El STEP original no se redistribuye: se identifica mediante SHA256.
Reproducir toda esa campaña requiere disponer de ese mismo archivo y generar
las mallas; no se promete que el clon por sí solo contenga el experimento o el CAD.

## Qué muestran las campañas del CAD

Primero se aplica una carga controlada independiente del modelo de aire:
**100 Pa sobre la piel superior**, con huella física x/c = 0,78–0,84 y
η = 0,25–0,75. Esto permite examinar la estructura sin confundir su error con
el del flujo. Tres mallas producen la siguiente tendencia.

<figure class="airfoil-figure">
  <img src="../../assets/airfoil/convergence.png" alt="Desplazamiento máximo de borde de salida a 100 Pa: 0,219615, 0,223638 y 0,224243 milímetros en tres mallas cada vez más finas." width="1211" height="717" loading="lazy">
  <figcaption>Convergencia estructural del escenario A con la misma huella física. El último cambio del vector TE es 0,270% y el de energía 0,526%. La frecuencia fundamental es 20,591 Hz. Estos cambios estiman sensibilidad a la discretización; no son cotas certificadas ni precisión experimental.</figcaption>
</figure>

La malla curva proyectada al CAD cambia el vector TE apenas 0,00190% frente a
la geometría afín fina. La sexta frecuencia todavía cambia 1,479% entre las
últimas mallas: queda fuera del cierre al 1% y de la banda principal de A,
0–60 Hz. La derivada de curvatura posterior cambia 3,20%; no se le atribuye la
precisión del desplazamiento.

Después se calcula el flujo acoplado a incidencia de 3°, densidad del aire
1,225 kg/m³ y velocidades U = 2,5–10 m/s. La respuesta parte de una perturbación
modal libre de 10 µm alrededor del equilibrio UVLM. El paso más fino del caso
A a 10 m/s es 15,625 µs y la ventana física tiene 1,2 s, suficiente para
observar el decaimiento de unos veinte ciclos válidos.

<figure class="airfoil-figure">
  <img src="../../assets/airfoil/free-response.png" alt="Desplazamiento transversal del borde de salida en la estación media: oscilaciones inicialmente de diez micrómetros que decaen hacia el equilibrio durante 1,2 segundos." width="1159" height="719" loading="lazy">
  <figcaption>Historia calculada del TE respecto a su equilibrio deformado, escenario A a U = 10 m/s. La frecuencia ajustada es 20,429 Hz y la tasa exponencial −6,581 s⁻¹. Se calcula la realimentación aerodinámica; no se impone una presión oscilante.</figcaption>
</figure>

La evolución de la piel posterior permite ver cómo ese movimiento varía a lo
largo de la cuerda. El siguiente video utiliza 241 estados muestreados de la
misma respuesta, sin generar estados intermedios artificiales.

<figure class="airfoil-figure">
  <video controls muted playsinline preload="none" poster="../../assets/airfoil/motion-poster.png" width="864" height="504" aria-label="Evolución numérica del desplazamiento de la piel posterior respecto al equilibrio">
    <source src="../../assets/airfoil/posterior-motion.mp4" type="video/mp4">
    Tu navegador no reproduce este video. <a href="../../assets/airfoil/posterior-motion.mp4">Descargar video MP4</a>.
  </video>
  <figcaption>Resultado numérico en η = 0,5, x/c = 0,68–0,995: desplazamiento vertical respecto al equilibrio, en micrómetros. La ventana física de 0–1,2 s se reproduce en 8,03 s (aproximadamente 6,7 veces más lenta). Se grafica desplazamiento, no una geometría amplificada; no contiene audio. Los <a href="../../assets/airfoil/posterior-motion.csv">estados muestreados</a> y sus <a href="../../assets/airfoil/motion-source.json">unidades y procedencia</a> acompañan el video.</figcaption>
</figure>

| U [m/s] | Frecuencia acoplada [Hz] | Tasa de crecimiento [s⁻¹] |
| ---: | ---: | ---: |
| 2,5 | 20,313 | −2,434 |
| 5,0 | 20,336 | −3,805 |
| 7,5 | 20,376 | −5,164 |
| 10,0 | 20,429 | −6,581 |

Las cuatro tasas negativas indican decaimiento **en estas hipótesis y en estas
ventanas**. No establecen un umbral de flutter real ni una oscilación
sostenida. Las guías B y C también se estudiaron como variantes condicionales.
En A, la última refinación temporal cambia el decaimiento 1,08%, el RMS 0,54%
y la fase 0,41°; el cambio espacial 96/128 en cuerda es 1,63% en decaimiento.

## Qué referencias comprueban cada parte

La verificación analítica y los ensayos externos cumplen funciones diferentes.
El UVLM se contrasta con las respuestas de **Theodorsen y Sears** en frecuencia
reducida k = ωc/(2U) = 0,5; 1,6; 6,4. Los casos refinados quedan por debajo de
2% en amplitud y 2° en fase. Eso comprueba el modelo potencial bajo sus
hipótesis; no prueba que el flujo real permanezca adherido.

Para la estructura hay además una comparación independiente: nueve geometrías
de placa PLA y 27 observaciones modales del conjunto de Huang y Zhang. La
figura muestra el primer modo de flexión, el único identificado sin ambigüedad
en este extracto. En las etiquetas, AR = L/c es la relación entre longitud
libre y cuerda, y f es la fracción flexible posterior en cuerda (f = 0 indica
placa uniforme). Ω es una frecuencia adimensional que combina longitud,
densidad y rigidez de placa; permite comparar las geometrías con su referencia.

<figure class="airfoil-figure">
  <img src="../../assets/airfoil/plate-comparison.png" alt="Primeras frecuencias adimensionales de nueve placas: datos modales publicados con dispersión muestral frente al cálculo MITC4, con discrepancias visibles en las placas escalonadas." width="1223" height="1018" loading="lazy">
  <figcaption>Comparación experimental externa, no del CAD original. Huang y Zhang, Mendeley Data v2, DOI 10.17632/8jxw5533py.2, CC BY 4.0. Figura derivada por MC-Andes: medias publicadas y desviaciones estándar muestrales frente al modelo nominal. Las ambigüedades de etiquetas y medias publicadas se conservan en la auditoría del repositorio; las barras no son intervalos de confianza.</figcaption>
</figure>

El error del primer modo varía de +0,68% a −10,87%, aunque la refinación de la
placa cambia como máximo 0,108%. Una malla convergida no elimina una
discrepancia física. No se ajustó E para borrar esa diferencia, y los ensayos
de placa no se transfieren como validación del mecanismo original.

La rama viscosa tiene su propio control: un cilindro fijo a Re = 20 da
C<sub>D</sub> = 2,0475, frente a 2,05 atribuido a Dennis y Chang en la tabla 2 de
Russell y Wang. La comparación es con una referencia **numérica publicada**,
no con una medición de este proyecto. Su diferencia de aproximadamente 0,12%
no fija la precisión de las presiones sobre las pieles del álabe.

<figure class="airfoil-figure">
  <img src="../../assets/airfoil/viscous-wake.png" alt="Campo calculado de vorticidad transversal alrededor y detrás de la sección del álabe, con escalas de signos opuestos y contorno del cuerpo en negro." width="1186" height="546" loading="lazy">
  <figcaption>Navier–Stokes laminar 2D, Re = 100, malla 640×320; vorticidad media en t* = tU/c entre 12,4 y 14. La barra muestra ωc/U, con saturación fuera de ±8; la región sólida se enmascara. La estela procede de la solución fluida y no de un dibujo ilustrativo.</figcaption>
</figure>

Estos casos viscosos utilizan una envolvente exterior rellena; el caso 3D
Re = 20 tiene extremos tapados. Son variantes explícitas del dominio fluido,
no cambios del sólido FEM. Los perfiles de estela cambian menos de 0,5% entre
las últimas mallas, pero C<sub>L</sub> conserva dispersión de 4–5% y el arrastre
integrado cerca de la piel difiere de la reacción inmersa. A U = 10 m/s el
Reynolds sería aproximadamente 1,67×10⁵: no se extrapolan los resultados
laminares Re = 20/100 a esa condición ni se afirma DNS, URANS o LES validado.

## Referencias y datos trazables

No se reproducen figuras editoriales de terceros. Los resultados originales
se redibujaron con la paleta del portal; la comparación modal conserva la
atribución y licencia de los datos. Las fuentes principales son:

1. **Theodore Theodorsen (1935).** *General Theory of Aerodynamic Instability
   and the Mechanism of Flutter*. NACA Report 496.
   [Informe original en NASA NTRS](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19930090935.pdf).
   Referencia analítica de fuerzas no estacionarias; no ensayo del álabe.
2. **Ahmed Malim, Nikolaos Mourousias, Benoît G. Marinus y Tim De Troyer (2023).**
   *Structural Design of a Large-Scale 3D-Printed High-Altitude Propeller:
   Methodology and Experimental Validation*. Aerospace 10, 256.
   [DOI 10.3390/aerospace10030256 · PDF institucional](https://cris.vub.be/ws/portalfiles/portal/95005631/malim2023aero.pdf).
   Fuente de las propiedades de referencia Tough PLA; su validación de hélice
   no identifica el material de esta pieza.
3. **Giulia Morettini, Massimiliano Palmieri, Lorenzo Capponi y Luca Landi (2022).**
   *Comprehensive characterization of mechanical and physical properties of
   PLA structures printed by FFF-3D-printing process in different directions*.
   Progress in Additive Manufacturing 7, 1111–1122.
   [DOI 10.1007/s40964-022-00285-8](https://doi.org/10.1007/s40964-022-00285-8).
   Contexto de variación por impresión y amortiguamiento; PLA y proceso
   distintos del sustituto Tough PLA y del espécimen desconocido.
4. **Ke Huang y Jiaying Zhang (2026).** *Experimental and numerical data from
   comparative analysis of candidate structural models for active camber
   morphing wings*. Mendeley Data, versión 2.
   [DOI 10.17632/8jxw5533py.2](https://data.mendeley.com/datasets/8jxw5533py/2),
   [licencia CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
   [Extracto y auditoría de procedencia](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/data/benchmarks/huang2026_provenance.json).
5. **David Russell y Z. Jane Wang (2003).** *A cartesian grid method for modeling
   multiple moving objects in 2D incompressible viscous flow*. Journal of
   Computational Physics 191, 177–205.
   [DOI 10.1016/S0021-9991(03)00310-3](https://doi.org/10.1016/S0021-9991(03)00310-3).
   Se utiliza su tabla de resultados de cilindro como referencia; su método
   streamfunction–vorticity no es el solver MAC/Brinkman de este proyecto.
6. **Alfonso del Carre et al. (2019).** *SHARPy: A dynamic aeroelastic simulation
   toolbox for very flexible aircraft and wind turbines*. JOSS 4(44), 1885.
   [DOI 10.21105/joss.01885](https://joss.theoj.org/papers/10.21105/joss.01885).
   Referencia metodológica y de organización del acoplamiento.

La formulación y convención de fase del control de Sears se documentan en la
[ficha de fuentes UVLM](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/data/benchmarks/cad_literature.json),
con enlace al manuscrito de Smyth, Young y Di Mare. No se trasladan curvas de
otros perfiles como si fueran mediciones de este CAD.

## Límites actuales y próximo paso

La evidencia apoya un **estudio numérico condicional del sólido original**.
No determina resistencia de la impresión, holgura o fricción reales,
C<sub>p</sub> de ambas pieles, un límite de flutter experimental o una estela
validada mediante PIV. Las cargas del VLM son resultantes normales
equivalentes; sus idealizaciones estacionarias conservan una discrepancia
que la refinación de paneles no elimina.

El siguiente paso físico es caracterizar material y montaje, medir formas y
frecuencias en reposo y con flujo, y registrar presiones o velocidades con
incertidumbre. Esos datos permitirían sustituir las hipótesis, revisar la guía
y contrastar las predicciones sin ajustar parámetros para ocultar errores.
Responsable individual y disponibilidad pública del CAD siguen pendientes de
confirmación; el código verificable y los datos de placa sí están disponibles.

Los [datos reducidos de esta publicación](../assets/airfoil/evidence.json),
[historial TE](../assets/airfoil/te-history.csv),
[hashes de los recursos](../assets/airfoil/asset-hashes.json) y
[licencias](../assets/airfoil/LICENSE.txt) permiten
rastrear cifras y archivos. La reproducción completa y sus restricciones se
explican en la [guía editorial del proyecto](https://github.com/MC-Andes/passive-airfoil-aeroelasticity-matlab/blob/28bb2fca284d31edb99968ddd7c75f83982774ef/docs/portal-publication.md).

[Volver al catálogo](../projects.md){ .md-button }
