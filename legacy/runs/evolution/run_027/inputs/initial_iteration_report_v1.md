# Viral Guide Iteration Report v1

## Alcance

Este informe compara dos guías y sus respectivos dry-runs de 20 propuestas para 2B, versión *NieR:Automata*:

- `viral_premise_guide_v1.2.md`
- `viral_premise_guide_extreme_test_v1.md`
- `dry_run_2b_nier_automata_20_v12.json`
- `dry_run_2b_nier_automata_20_extreme_test_v1.json`

Ambos resultados contienen 20 propuestas con la misma distribución: 4 `closeup`, 4 `medium`, 4 `fullbody`, 4 `dynamic` y 4 `cinematic`. Ambos usaron el mismo perfil local de personaje. Por lo tanto, la diferencia observada es útil para evaluar el efecto de la guía, aunque la muestra sigue limitada a un personaje, un modelo y una ejecución por enfoque.

## Conclusión ejecutiva

La prueba extrema confirma que el modelo sí puede salir del patrón “catedral / lluvia / ruina / contemplación”. El sesgo conservador no es una limitación rígida del modelo: la prioridad y las prohibiciones expresadas en la guía cambian claramente el resultado.

Sin embargo, ninguno de los dos extremos es una solución final:

- v1.2 ofrece una arquitectura más completa y protege mejor identidad, micro-historia, variedad conceptual y potencial de animación, pero sus reglas son demasiado negociables. El modelo vuelve a sus atajos favoritos: escenarios solemnes, lluvia, soledad, gameplay genérico y belleza estática.
- Extreme consigue el cambio tonal buscado y devuelve el protagonismo a 2B, pero sobrecorrige. Reemplaza el repertorio “catedral/lluvia” por otro repertorio estrecho: smirk, mirada directa, ajuste de ropa, vapor, vestidor, giro y vestido ondeando. Aumenta la sensualidad, pero muchas propuestas pierden situación, causalidad y variedad real.

La dirección recomendada para v1.3 es conservar la estructura y los límites de v1.2, incorporar la claridad de prioridades y las prohibiciones del extreme, y agregar controles de lote medibles contra repetición y contra escenas atmosféricas o poses sin evento.

## Comparación resumida

| Dimensión | v1.2 | Extreme test | Dirección para v1.3 |
|---|---|---|---|
| Identidad de 2B | Fuerte en vestuario y silueta | Fuerte, pero subordinada a recursos sensuales repetidos | Mantener identidad como restricción dura |
| Visual appeal | Presente en la guía, irregular en la salida | Alto y consistente | Convertirlo en criterio obligatorio, no en único objetivo |
| Micro-historia | Mejor intención general, ejecución irregular | Fuerte en algunos casos, ausente en muchas poses | Exigir causa + acción/reacción visible |
| Atmósfera contemplativa | Alta: 7/20 usan el paquete atmosférico amplio | Residual: 1/20, sin catedral/ruina/lluvia como concepto | Prohibir atajos por defecto y limitar escenas environment-led |
| Gameplay genérico | 4/20 acciones claramente genéricas | 1/20 caso claro, aunque hay movimiento sin causa | Exigir que la acción revele personalidad o situación |
| Sensualidad | Moderada y frecuentemente neutralizada | Alta y evidente | Mantenerla alta, con variedad de mecanismos |
| Variedad | Más variedad de ambientes, menos de hooks | Menos variedad de ambientes y hooks | Controlar ambas dimensiones con un ledger de lote |
| Repetición dominante | lluvia, soledad, catedral, salto/carrera | smirk/mirada, ajuste de ropa, vapor, giro | Límites explícitos por familia de hook |
| Cinematic | Tiende a wallpaper solemne | Tiende a low-angle + pose dominante | Cinematic debe contener evento, no sólo tratamiento visual |

Los conteos son diagnósticos por familias de patrones, no un scoring absoluto. En v1.2, el grupo atmosférico amplio aparece en `b01_03`, `b01_05`, `b02_05`, `b03_03`, `b03_05`, `b04_03` y `b04_05`. En extreme, el único caso cercano es `b03_05`, por su luz cálida, silueta y acción vaga. No hay propuestas de catedral, ruina o lluvia en extreme.

## Enfoque v1.2

### Fortalezas

1. **Arquitectura conceptual completa.** La fórmula `character appeal + personality + visual hook + situation + potential motion` es una base correcta. También son valiosas las secciones de identidad, micro-historia, contraste, animación, variedad y checklist final.

2. **Buen límite de contenido.** Permite tensión erótica, exposición sugerida y strategic coverage, pero mantiene una frontera no explícita clara. Ese límite sirve para producción y no necesita una escalada adicional.

3. **Comprende que una premise debe ser un momento.** La distinción entre pose bonita y acción/reacción es correcta. Ejemplos de la salida que se acercan a ese objetivo:

   - `b01_02`: ajuste de guantes con postura y tensión visibles.
   - `b02_02`: manos retorciendo el vestido antes de hablar; hay estado emocional y anticipación.
   - `b02_03`: carta escondida detrás de la espalda y smirk; combina prop, personalidad y curiosidad.
   - `b04_01`: pétalo sobre el blindfold y reacción inmediata; es pequeño, pero causal y legible.

4. **Protege el carácter reconocible.** Las propuestas conservan pelo blanco, blindfold, vestido negro, guantes, mangas, botas y silueta. El personaje no se vuelve una mujer genérica.

5. **Tiene ambición de variedad.** La guía enumera locaciones, actividades, emociones y estilos distintos. El problema está en que esas instrucciones no son suficientemente vinculantes para vencer los hábitos del modelo.

### Fallos observados

1. **Las prioridades compiten entre sí sin una regla de desempate fuerte.** “Visual appeal”, “situation”, “canon”, “animation” y “atmosphere” aparecen como objetivos compatibles. Cuando el modelo debe elegir, suele resolver la premise con una escena estética y segura.

2. **Las prohibiciones son blandas.** La guía dice evitar standing in ruins, wind-blown hair, dramatic sunset y gameplay, pero permite ruinas, castillos, templos y ambientes dramáticos en otras secciones. El modelo interpreta “avoid repetition” como permiso ocasional y luego repite el patrón entre lotes.

3. **El modo contemplativo sigue activo.** Los casos más claros son:

   - `b01_05`: estructura tipo catedral, personaje sola, haces de luz, artefacto flotante y “mysterious awe”.
   - `b02_05`: hologramas, rim light, serenidad, aislamiento y grandeza.
   - `b03_03`: 2B quieta en una azotea con brisa y cityscape.
   - `b03_05`: sola en callejón mojado, neón e intensidad.
   - `b04_03`: calle mojada, neón y paraguas dramático.
   - `b04_05`: catedral, luna, techo roto, polvo y revelación del ojo.

4. **Se repite el paquete lluvia + reflejo + neón.** Aparece en `b01_03`, `b03_05` y `b04_03`. Cambia el encuadre, pero no cambia la idea.

5. **Dynamic deriva a gameplay o acción genérica.** Los cuatro dynamic usan aterrizaje, salto, carrera o salto entre edificios. La acción es visible, pero podría pertenecer a casi cualquier heroína y rara vez crea tensión sensual, humor o personalidad específica.

6. **Cinematic se confunde con tratamiento visual.** Iluminación, escala, soledad y perspectiva sustituyen el evento. La categoría termina funcionando como generador de wallpaper.

7. **Algunos closeups son estados, no momentos.** Inclinar la cabeza, mechón sobre el blindfold, sonrisa tenue o revelación del ojo se repiten sin una causa suficientemente concreta.

## Enfoque extreme test

### Fortalezas

1. **Demuestra control tonal.** La salida abandona catedrales, ruinas, lluvia, paisajes solemnes y misiones. La hipótesis “el modelo no puede salir de ese estilo” queda refutada por este test.

2. **2B vuelve a ser el centro visual.** Los escenarios son subordinados: vestidor, vanity, mesa, bañera, ducha, railing. La premise sigue funcionando aunque se elimine gran parte del fondo.

3. **La sensualidad es concreta y visible.** No depende de adjetivos abstractos. Usa postura, tela, manos, botas, silueta, cobertura, vapor, movimiento y expresión. Esto es más útil para una etapa posterior de construcción de prompts.

4. **Hay buenos modelos de “atracción + situación”.** Los mejores casos para rescatar son:

   - `b01_03`: salida detrás de una cortina, paso interrumpido y strategic coverage.
   - `b02_02`: ponerse las botas frente a una vanity; manos, material, postura y mirada forman un momento concreto.
   - `b02_03`: equilibrio sobre una pierna mientras ajusta la bota; silueta y acción coinciden.
   - `b02_04`: giro causado por un ruido; reacción, movimiento y actitud son legibles.
   - `b02_05`: bañera, estiramiento, vapor como cobertura y mirada; sensualidad integrada en una acción.
   - `b03_02`: el vestido se desplaza y la expresión cambia al advertirlo; hay causa y reacción.
   - `b03_03`: salida de la ducha sosteniendo el vestido cerrado; estado, gesto y cobertura están conectados.

5. **Cinematic deja de ser paisaje.** Incluso cuando la micro-historia es débil, el encuadre se concentra en 2B, su expresión y su lenguaje corporal.

### Fallos observados

1. **La variedad aparente oculta repetición estructural.** Nueve propuestas contienen smirk, knowing gaze, half-lidded gaze, mirada directa o teasing; ocho giran alrededor de ajustar, tirar, sostener o acomodar ropa/accesorios.

2. **Los cuatro dynamic pertenecen a una sola familia.** Todos usan giro, spin, backflip o dress flare. El test eliminó el gameplay, pero lo reemplazó por una plantilla de movimiento igualmente estrecha.

3. **Vapor/baño/ducha se convierte en un nuevo atajo.** Aparece en tres propuestas. Es efectivo una vez; repetido, se vuelve equivalente funcional de la lluvia en v1.2.

4. **El último lote pierde micro-historia casi por completo.** `b04_01` a `b04_05` son, en esencia, expresión + gesto o pose + encuadre. No hay consecuencia, sorpresa, interacción significativa ni pregunta narrativa fuerte.

5. **Algunas propuestas sólo describen body display.** `b04_03` es una pose de cuerpo completo; `b04_05` es una pose dominante inclinada sobre una superficie; `b01_05` usa mesa y vapor, pero no establece qué ocurre. Cumplen tono, no premise.

6. **Expresiones homogeneizadas.** 2B aparece una y otra vez segura, teasing, smirking o challenging. Se pierde contraste: molestia controlada, concentración, sorpresa seca, humor accidental, vulnerabilidad breve o curiosidad genuina.

7. **El observador implícito se vuelve una muleta.** Direct eye contact, unseen observer y viewer's space aparecen como sustituto de una interacción dentro de la escena.

8. **Riesgo de deriva de identidad factual.** Los resultados inventan ojos azules o verdes aunque el perfil local suministrado no contiene color de ojos. La guía futura debe impedir convertir una inferencia visual no respaldada en dato canónico preciso.

## Fallos repetidos en ambos enfoques

1. **Generación por lotes sin memoria efectiva de diversidad.** Cada lote de cinco es razonablemente variado por categoría, pero repite las mismas soluciones de lotes anteriores.

2. **La categoría domina la idea.** `closeup` produce head tilt/gaze, `fullbody` produce weight shift o pose de silueta, `dynamic` produce salto/giro y `cinematic` produce low angle + luz. El encuadre se está usando como generador conceptual cuando debería ser una forma de presentar un hook previamente elegido.

3. **Repetición de verbos y estados.** Tilt, look, stand, lean, adjust, turn y flare aparecen como soluciones recurrentes. Falta diversidad de interacciones y consecuencias.

4. **Micro-historia nominal.** Muchas propuestas incluyen un gesto, pero no una relación causal. “Está ajustando X” no siempre crea una pregunta, un obstáculo o un cambio de estado.

5. **Props poco específicos o sin función.** Floating artifact, data streams, glossy table, railing, polished surface y unseen source funcionan como decoración. Un prop fuerte debe causar, complicar o resolver el momento.

6. **La personalidad se reduce a expresión facial.** Smirk, surprise o determination se agregan al final, sin cambiar lo que el personaje hace.

## Patrones deseados para v1.3

1. **Atracción integrada en una acción concreta.** La silueta, ropa o postura deben participar físicamente del momento, no ser un comentario adicional.

2. **Causa y cambio visibles.** Algo acaba de ocurrir o está ocurriendo, y 2B hace, evita, descubre, corrige, atrapa, oculta, sostiene o responde a ello.

3. **Personalidad demostrada mediante decisión.** La compostura, desafío, incomodidad controlada o humor seco deben verse en cómo resuelve la situación.

4. **Escenario subordinado.** El entorno aporta una causa, obstáculo, cobertura o contraste. No es el hook principal.

5. **Sensualidad diversa.** Alternar silueta, cercanía, clothing tension, movimiento, strategic coverage, postura, contacto con props, contraste emocional y situación accidental. No depender siempre de exposición o mirada directa.

6. **Movimiento con efecto.** El movimiento debe modificar pelo, ropa, equilibrio, distancia, objeto o expresión de forma relevante.

7. **Contraste de carácter.** Ejemplos: compostura frente a una pequeña complicación; eficiencia aplicada a una situación íntima; confianza que se quiebra por un segundo; elegancia en una tarea mundana; desafío sin mirar al viewer.

8. **Composición al servicio del hook.** Primero se decide qué ocurre; después se elige closeup, medium, fullbody, dynamic o cinematic para hacerlo legible.

## Patrones no deseados para v1.3

- Catedral, ruina, lluvia, calle mojada, neón, luna, polvo flotante o paisaje solitario usados como concepto principal.
- “Standing somewhere looking beautiful”, aunque incluya low angle, rim light o body emphasis.
- Salto, carrera, aterrizaje, combate o debris sin un hook específico de personaje.
- Head tilt + hair strand + faint/knowing smirk como fórmula de closeup.
- Mirada directa o unseen observer como reemplazo de una situación.
- Ajuste de ropa repetido en distintas prendas como si fueran ideas distintas.
- Vestidor, espejo, vanity, baño, ducha, vapor o cama repetidos como familia de ambiente íntimo.
- Giro + dress flare como solución automática para dynamic.
- Lean over surface como solución automática para cinematic.
- Adjetivos de tono —serene, mysterious, provocative, dominant— sin evidencia física dentro del frame.
- Datos canónicos precisos no presentes en el perfil local.

## Propuesta concreta para `viral_premise_guide_v1.3.md`

### 1. Mantener de v1.2

Conservar, con edición menor:

- Character Identity Priority.
- Erotic Non-Explicit Direction.
- Strategic Censorship and Suggestion.
- Micro-Story Requirement.
- Animation Potential.
- Personality Usage y Canon Personality Rules.
- Category Guidance.
- Visual Contrast.
- Final Premise Checklist.

Estas secciones contienen la filosofía productiva correcta. El problema principal no es su existencia, sino su orden de prioridad y la ausencia de enforcement de lote.

### 2. Reemplazar la prioridad general

Usar una jerarquía explícita:

1. Recognizable character identity and factual correctness.
2. Immediate character-centered visual hook.
3. Concrete cause, action or reaction visible in the frame.
4. Attractive body language or sensual tension integrated into that event.
5. Personality expressed through behavior.
6. Composition and environment supporting the hook.
7. Motion potential.

Regla de desempate propuesta:

> When two ideas are equally coherent, choose the one with stronger character-centered attraction and a more concrete visible event. Never choose atmosphere, lore or scenery as the tie-breaker.

### 3. Añadir un contrato mínimo obligatorio por premise

Cada premise debe contener, de forma legible:

- **hook:** qué detiene el scroll;
- **event:** qué está ocurriendo ahora;
- **character behavior:** qué hace 2B al respecto;
- **visible consequence:** qué cambia en postura, ropa, objeto, equilibrio o expresión;
- **identity anchor:** al menos un rasgo reconocible relevante;
- **composition:** encuadre elegido para mostrar lo anterior.

No es necesario escribir estos campos por separado en el JSON, pero el modelo debe verificarlos internamente. Si sólo hay pose + outfit + expression, la premise debe rechazarse.

### 4. Convertir los anti-patrones en reglas duras

Texto propuesto:

> Do not use cathedral, ruins, rain, wet neon streets, moonlight, sunset, lonely landscapes, floating dust, generic battle, generic running, generic jumping or official-game atmosphere as default idea generators. They may appear only when explicitly requested or when they cause a unique character-centered event that cannot be expressed more directly.

> Cinematic is not permission to create wallpaper. Every cinematic premise still requires a concrete event, interaction or consequence centered on the character.

> Dynamic is not permission to create generic action. Movement must reveal personality, sensual tension, humor, vulnerability or a distinctive interaction.

### 5. Añadir un diversity ledger obligatorio para el lote

Antes de aceptar cada nueva propuesta, comparar contra las ya generadas en seis ejes:

- location/environment family;
- primary action/verb;
- sensual hook family;
- expression/attitude;
- prop or interaction;
- composition/viewpoint pattern.

Límites sugeridos para un lote de 20:

- máximo 2 propuestas por familia de ambiente;
- máximo 2 por familia de acción principal;
- máximo 2 con direct eye contact como hook;
- máximo 2 basadas en clothing adjustment;
- máximo 2 con steam/water/strategic coverage;
- máximo 2 con turn/spin/flaring fabric;
- máximo 2 environment-led, y ninguna puramente contemplativa;
- al menos 14 con causa → acción/reacción → consecuencia visible;
- al menos 12 claramente attraction-forward;
- al menos 6 donde el hook no dependa de mirada directa, smirk o exposición.

Si una idea excede un límite, debe cambiarse la familia conceptual, no sólo la locación o el encuadre.

### 6. Separar ideación de composición

Orden de trabajo interno propuesto:

1. Elegir una familia de situación aún no usada.
2. Definir causa, comportamiento y consecuencia.
3. Integrar visual appeal de manera física.
4. Verificar identidad y personalidad.
5. Seleccionar la categoría de composición que mejor comunica el hook.

Esto evita que `dynamic` signifique automáticamente “jump/spin” y que `cinematic` signifique automáticamente “low angle + dramatic light”.

### 7. Reescribir las reglas por categoría

**Closeup**

- Debe mostrar una reacción a algo visible o claramente inferible dentro del frame.
- Máximo un closeup del lote basado sólo en gaze/head tilt.
- Manos, prop, reflejo funcional o cambio de expresión deben aportar causalidad.

**Medium**

- Priorizar interacción de manos, torso, objeto y ropa.
- El gesto debe resolver o complicar una situación, no sólo exhibir el outfit.

**Fullbody**

- La silueta completa debe participar de una acción, equilibrio, desplazamiento o contraste.
- Rechazar weight-shifted standing pose sin evento.

**Dynamic**

- Exigir causa y consecuencia únicas.
- No usar salto, carrera, giro o dress flare salvo que el movimiento produzca un hook específico y no repetido.

**Cinematic**

- El evento sigue siendo obligatorio.
- El environment puede amplificar intimidad, poder, humor o tensión, pero nunca reemplazarlos.
- Rechazar cualquier premise que siga funcionando sólo como wallpaper después de quitar la acción.

### 8. Ampliar el repertorio emocional y situacional

Pedir distribución de actitudes, no una personalidad única repetida:

- controlled annoyance;
- dry amusement;
- brief surprise;
- focused concentration;
- reluctant vulnerability;
- confident challenge;
- curiosity;
- recovery of composure.

Pedir también familias de interacción diversas: tarea cotidiana, pequeña falla mecánica, objeto rebelde, reflejo que revela algo, equilibrio incómodo, interrupción, preparación, recuperación, ocultamiento, captura, error elegante, elección deliberada y contraste entre eficiencia y situación íntima.

### 9. Añadir verificación factual

Texto propuesto:

> Use the local character profile as the source of factual identity. Do not invent precise eye color, relationships, lore, accessories or anatomy facts absent from that profile. When a visual fact is uncertain, describe the expression or lighting without asserting a new canonical detail.

### 10. Checklist de aceptación v1.3

Una premise se acepta sólo si todas son verdaderas:

1. El personaje, no el fondo, detiene el scroll.
2. Hay un evento presente, no sólo pose o atmósfera.
3. Existe causa, comportamiento o consecuencia visible.
4. La atracción está integrada en la acción.
5. La personalidad afecta lo que hace, no sólo la expresión añadida.
6. No repite familia de hook, ambiente, verbo o actitud más allá del límite.
7. La categoría mejora la legibilidad de la idea.
8. Puede animarse durante 5–10 segundos sin inventar una acción nueva.
9. Respeta identidad sin introducir datos no respaldados.
10. No parece gameplay, wallpaper ni una pose sensual genérica.

## Resultado esperado de v1.3

v1.3 no debería producir una media aritmética entre ambos tests. Debería conservar la disciplina narrativa de v1.2 y la decisión visual del extreme, mientras elimina los atajos de los dos.

La señal de éxito en un próximo dry-run de 20 sería:

- 0 catedrales/ruinas/lluvia como hook;
- 0 escenas puramente contemplativas;
- como máximo 2 ideas por familia sensual o de movimiento;
- 14 o más premises con causalidad visible;
- 12 o más attraction-forward;
- cinematic y dynamic con situaciones específicas, no plantillas de encuadre;
- variedad emocional reconocible;
- ninguna invención factual fuera del perfil local.

El hallazgo principal es favorable: el modelo responde a una dirección más firme. La próxima iteración debe usar esa capacidad con controles de diversidad y causalidad, no volver a suavizar el tono ni mantener el extreme como guía productiva.
