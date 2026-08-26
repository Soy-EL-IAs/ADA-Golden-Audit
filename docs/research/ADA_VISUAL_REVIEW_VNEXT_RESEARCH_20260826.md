# ADA Visual Review vNext — Investigación evidence-first (agosto 2026)

Antes de la tabla, tres hallazgos que cambian el planteamiento del problema. No son opinión mía: están medidos.

## 0. Diagnóstico: tu reviewer no está "mal configurado", está en el régimen esperado

**(a) Un VLM de 8B como juez pairwise está apenas por encima del azar.** En Multimodal RewardBench 2 (Meta FAIR), el benchmark cubre cuatro tareas —text-to-image, image editing, generación interleaved y razonamiento multimodal— con 1.000 pares de preferencia anotados por expertos por tarea; Gemini 3 Pro alcanza 75-80%, GPT-5 y Gemini 2.5 Pro 66-75%, frente a >90% de humanos, y el mejor modelo open-source, Qwen3-VL-32B, llega a \~64%. Los números por subtarea (reproducidos en MJ1, Haize Labs): Qwen3-VL-8B obtiene 59,4 en T2I, 61,7 en Editing, 61,5 en Interleaved y 54,6 en Reasoning (media 59,3); Qwen2.5-VL-7B obtiene 50,9 de media. Con azar = 50, tu `qwen3-vl-8b` acierta \~1 de cada 10 comparaciones difíciles por encima del azar.

**(b) La complacencia en anatomía está cuantificada y es brutal.** ArtifactLens (Stanford + Snap, feb 2026) mide detección de artefactos anatómicos humanos sobre cinco benchmarks: Qwen2.5-VL-7B en zero-shot obtiene F1 = 0,017 con precisión 0,646 y recall 0,009 — es decir, prácticamente nunca marca un artefacto; GPT-4o 0,217 y Gemini-2.5-Pro 0,560. Los autores atribuyen los malos resultados a un recall muy bajo: los modelos casi nunca clasifican como artefacto. Y el diagnóstico causal es clave para ti: los generadores de instrucciones LLM tienden a producir prompts conservadores ("solo marca artefactos si estás seguro"), pero los VLM ya están sesgados en contra de la clase 'artefacto' y se benefician de la guía opuesta. Tu confidence 1.0 y tus 10/10 son ese sesgo, no un bug de prompt.

**(c) El scoring pointwise 0-10 es el formato equivocado.** GEditBench v2 (NTU + StepFun, mar 2026) lo prueba empíricamente: la comparación pairwise logra consistentemente mayor acuerdo con juicios humanos que el rating absoluto en las tres dimensiones (instruction following, visual quality, visual consistency); además los evaluadores pointwise aprenden un mapeo rígido a puntuaciones absolutas que limita su techo cognitivo a la distribución de entrenamiento, produciendo puntuaciones similares ante ediciones fuera de distribución. Tencent (WeGenBench) mide lo mismo desde otro ángulo: el scoring VLM basado en reglas es muy propenso a sesgo de tendencia central (concentración masiva de imágenes en 7-8), y el esquema "describir-luego-puntuar" induce al VLM a un modo hipercrítico de nitpicking donde las alucinaciones en texto largo producen acumulación en cascada de errores.

**(d) Sorpresa contraintuitiva: para un modelo de 8B, razonar antes de decidir empeora el juicio.** Forzar a Qwen3-VL-8B-Instruct a generar una justificación primero provoca una degradación significativa del rendimiento, atribuida a que generar texto previo extenso diluye la atención visual y corrompe el juicio estructural final; "Decide-Only" y "Decide-Before-Reason" rinden casi idénticamente. El matiz: una cadena *estructurada* con observación visual primero sí ayuda, pero se ha demostrado en un modelo de 30B — el prompting de "grounded verification" mejora la accuracy de Qwen3-VL-30B-A3B en +3,8 puntos en Image Editing y +1,7 en Reasoning sin ningún entrenamiento, frente a razonamiento open-ended. Regla práctica: **CoT libre = veneno a 8B; extracción estructurada de observaciones = útil, pero mide antes de asumirlo en tu escala.**

---

## 1. Tabla de candidatos relevantes

| # Modelo Org / fecha Base Params Tarea entrenada Benchmark → resultado Weights / Licencia GGUF LM Studio VRAM aprox. Multi-img Pairwise Explica Evidencia  |                                              |                                            |                                       |                   |                                                                     |                                                                                       |                                             |                              |                             |                                  |                       |                 |                     |                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------ | ------------------------------------- | ----------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------- | --------------------------- | -------------------------------- | --------------------- | --------------- | ------------------- | -------------------------------------------------------------------- |
| 1                                                                                                                                                          | **EvoQuality**                               | ByteDance + CityU HK, ICLR 2026            | Qwen2.5-VL-7B                         | 8B                | NR-IQA auto-supervisado (voting + ranking)                          | AGIQA PLCC 0,839 / SRCC 0,777; WAVG 0,751 PLCC (ckpt liberado)                        | HF `ByteDance/EvoQuality`, Apache-2.0       | Sí (comunitario)             | Sí                          | \~9 GB Q8\_0                     | Sí (pares)            | Sí (nativo)     | Parcial (`<think>`) | **Paper peer-reviewed (ICLR 2026)**                                  |
| 2                                                                                                                                                          | **Q-ReAlign Lite-4B** (+ Mini-0.8B / Pro-9B) | Q-Future, jun 2026                         | Qwen3.5-VL                            | 5B                | IQA + IAA + VQA (niveles discretos)                                 | AGI SRCC 0,829 / PLCC 0,871; media 7 benchmarks 0,889 vs Q-Align 0,869                | HF `q-future/Q-ReAlign-Lite-4B`, Apache-2.0 | No                           | Improbable (arq. `qwen3_5`) | \~10,3 GB BF16                   | Sí (vídeo)            | No nativo       | No (escalar puro)   | **Model card** (sin paper propio)                                    |
| 3                                                                                                                                                          | **RALI**                                     | ByteDance + PKU + CUHK, **ICLR 2026 Oral** | CLIP (sin LLM)                        | \~5% de Q-Insight | IQA por alineación contrastiva imagen↔texto de calidad              | Generalización comparable a modelos reasoning con <5% de params y tiempo              | GitHub `xuanyuzhang21/RALI`                 | N/A                          | N/A (servicio propio)       | <1 GB                            | No                    | No              | No                  | **Paper peer-reviewed (Oral)**                                       |
| 4                                                                                                                                                          | **EditScore-Qwen3-VL-4B / 8B**               | VectorSpaceLab, **ICLR 2026**              | Qwen3-VL-4B/8B + LoRA                 | 4B / 8B           | Reward model para edición guiada por instrucción                    | EditReward-Bench (13 subtareas); el 4B iguala al 32B original y el 8B al 72B original | HF `EditScore/*`, Apache-2.0                | No oficial (LoRA fusionable) | Probable tras fusión        | \~3-6 GB Q5/Q6                   | **Sí (input+output)** | Sí              | Sí (JSON)           | **Paper peer-reviewed + benchmark oficial**                          |
| 5                                                                                                                                                          | **PVC-Judge**                                | NTU + StepFun, mar 2026                    | Qwen3-VL-8B + LoRA r64                | 8B                | **Pairwise visual consistency** (identidad, estructura, coherencia) | VCReward-Bench: 81,82 media vs GPT-5.1 76,89                                          | HF `GEditBench-v2/PVC-Judge`                | No                           | Probable tras fusión        | \~6 GB Q5\_K\_M                  | Sí                    | **Sí (nativo)** | Sí                  | **Preprint + benchmark oficial (3.506 pares anotados por expertos)** |
| 6                                                                                                                                                          | **HADM-L / HADM-G**                          | Adobe + BU, 2024 (v2 mar 2025)             | EVA-02-L ViTDet + Cascade R-CNN       | \~0,3B ×2         | **Detección/localización de artefactos humanos** (box-level)        | F1 global 0,758 en 5 benchmarks (meta-eval independiente)                             | GitHub `wangkaihong/HADM`                   | N/A                          | N/A (servicio propio)       | \~2-3 GB                         | No                    | No              | Sí (cajas + clase)  | **Preprint + meta-eval independiente**                               |
| 7                                                                                                                                                          | **MagicAssessor-7B**                         | MagicMirror, sep 2025                      | VLM 7B (SFT+GRPO sobre MagicData340K) | 7B                | Assessment fine-grained de artefactos físicos                       | F1 global 0,754 en 5 benchmarks                                                       | HF `wj-inf/MagicAssessor-7B`                | No                           | Probable                    | \~5-6 GB Q5                      | No                    | No              | Sí (etiquetas)      | **Preprint + meta-eval independiente**                               |
| 8                                                                                                                                                          | **ArtifactLens** (scaffold, no modelo)       | Stanford + Snap, feb 2026                  | Cualquier VLM congelado               | —                 | Detección de artefactos vía specialists + ICL + prompt-opt          | F1 0,817 (Gemini-2.5-Pro); **Qwen2.5-VL-7B: 0,017 → 0,501**                           | Método (DSPy)                               | N/A                          | N/A                         | = tu VLM                         | Sí                    | No              | Sí                  | **Preprint, primer multi-benchmark del área**                        |
| 9                                                                                                                                                          | **HPSv3**                                    | MizzenAI + CUHK, **ICCV 2025**             | Qwen2-VL                              | \~8B              | Preferencia humana wide-spectrum (calidad + alignment)              | 72,8% PickScore-test / 85,4% HPDv2 / 76,9% HPDv3; Spearman r=0,94                     | HF `MizzenAI/HPSv3`                         | No                           | Improbable                  | \~6 GB                           | No                    | Sí (ranking)    | No                  | **Paper peer-reviewed**                                              |
| 10                                                                                                                                                         | **Q-Eval-Score**                             | SJTU + Meituan, **CVPR 2025 Oral**         | LMM SFT sobre Q-EVAL-100K             | \~7B              | **Calidad + alignment desacoplados**, long-prompt                   | Q-EVAL-100K: 960K anotaciones humanas, 60K imágenes                                   | Código/datos anunciados                     | No                           | Improbable                  | \~6 GB                           | No                    | No              | Parcial             | **Paper peer-reviewed (Oral)**                                       |
| 11                                                                                                                                                         | **MJ1**                                      | Haize Labs, mar 2026                       | Qwen3-VL-30B-A3B + LoRA               | 30B (3B activos)  | Juez multimodal con grounded verification                           | **MMRB2 77,0%** (T2I 80,2 / Edit 78,1), supera a Gemini-3-Pro                         | Solo demo pública                           | No                           | —                           | \~18 GB Q4 (MoE, offload viable) | Sí                    | Sí              | Sí (XML)            | **Preprint; pesos no confirmados**                                   |
| 12                                                                                                                                                         | **ID-Sim / DINOv3 / ArcFace / DreamSim**     | Varios, hasta abr 2026                     | Embeddings                            | 0,1-0,6B          | Similitud de identidad                                              | ID-Sim: mejor balance sensibilidad-identidad vs invarianza contextual                 | Mixto                                       | N/A                          | N/A                         | <2 GB                            | Sí                    | Sí (numérico)   | No                  | **Preprint + papers**                                                |

**Notas de disponibilidad que importan:**

- Qwen3-VL tiene GGUF oficiales y compatibilidad con llama.cpp, Ollama y otras herramientas GGUF, con soporte CUDA, y permite mezclar niveles de precisión entre los componentes de lenguaje y visión; llama.cpp soporta GGUF de Qwen3-VL desde el 30 de octubre de 2025. Esto **no** se extiende automáticamente a Qwen3.5/3.6-VL: la vision de Qwen 3.5 y 3.6 seguía sin funcionar en Ollama en julio de 2026 porque el sidecar mmproj no estaba conectado, aunque llama.cpp / LM Studio se citan como ruta viable. **Verifica esto antes de comprometerte con Q-ReAlign.**
- Tu RTX 5070 Ti es Blackwell (sm\_120). HADM está construido sobre Detectron2 con torch 1.12+cu116 — no arranca tal cual en Blackwell. Existe una reimplementación single-file sin Detectron2 del backbone EVA-02 de HADM que corre en Blackwell/sm\_120 vía SDPA con \~0,999 de paridad coseno, pero eso cubre el backbone, no la cabeza de detección. Cuenta con una tarde de fricción.

---

## 2. Verificación específica: ¿EvoQuality Q8\_0 para ADA?

**Lo que se confirma:**

- EvoQuality existe, es de ByteDance + City University of Hong Kong, y es paper de conferencia en ICLR 2026. Es NR-IQA que soporta tanto scoring de imagen única como comparación pairwise; el backbone es Qwen2.5-VL-7B, licencia Apache-2.0, 8B params, y los pesos liberados corresponden a T=1 (primera ronda de auto-evolución).
- Los resultados del paper en AGIQA-3K: EvoQuality\@Round1 obtiene PLCC 0,839 y SRCC 0,777 en AGIQA, frente a 0,766/0,681 del Qwen2.5-VL-7B base; la media ponderada sube de 0,615 a 0,751 PLCC.

**Lo que no cuadra con las cifras del repo GGUF.** Tú citas BF16 PLCC 0,8033 / SRCC 0,7177 sobre \~99 imágenes de AGIQA-3K. El paper reporta 0,839 / 0,777 sobre el conjunto completo (\~2.982 imágenes). El PLCC es compatible dentro del ruido; **el SRCC está 0,06 por debajo**. Con n=99, el intervalo de confianza al 95% de un SRCC de \~0,72 es aproximadamente ±0,10 — así que no hay contradicción estadística, pero **esas cifras no distinguen BF16 de Q8\_0 ni de Q5\_K\_M**. Las diferencias que reportas (0,8033 vs 0,8037 vs 0,7999) son ruido de muestreo, no señal de cuantización. La recomendación "Q8\_0 para GPUs ≥16 GB" del repo es razonable por prudencia, pero **no está respaldada por esa medición**. El proveedor del GGUF, Doradus Research, lo publicó el 13 de junio de 2026 como la primera versión GGUF de EvoQuality, con seis variantes de 4 a 14 GB y >200 tokens/s en una GPU de consumo — es un actor con infraestructura seria, pero es evidencia de model card, no benchmark independiente.

**Veredicto para ADA: sí, pero para una sola de tus siete tareas, y con dos advertencias de dominio.**

1. **EvoQuality solo cubre tu categoría 4 (perceptual image quality).** No hace prompt adherence, no hace identidad, no hace img2img preservation, y no está entrenado para detectar anatomía imposible. Su propia model card lo dice: el uso recomendado es NR-IQA, comparación de generalización cross-dataset, ranking/filtrado de calidad y señales auxiliares para limpieza de datos; no se recomienda como criterio único de calidad para decisiones de alto riesgo.
2. **Dominio.** EvoQuality se entrena exclusivamente sobre KONIQ, aumentado con distorsiones sintéticas: 10 variantes por imagen muestreando 10 de 35 tipos de distorsión y 5 niveles de severidad. KonIQ son fotografías naturales. Sus mejores ganancias están en distorsiones sintéticas (TID2013 +77,4%, PIPAL +46,2%). Tu pipeline produce ilustración y anime, no fotos con ruido JPEG. El propio model card avisa: las pseudo-etiquetas derivan de sus propios votos, lo que puede amplificar preferencias sistemáticas o puntos ciegos del modelo base, y puede fallar en imágenes de dominios específicos. Esto no es teórico: en customización T2I ya se documentó que los modelos IQA punteros (LIQE, MANIQA, artifact scorer) pueden no ser adecuados por distribution shift, con un sesgo importante que favorece o desfavorece imágenes de ciertas categorías.
3. **Bug de configuración probable en tu integración.** Los prompts del paper requieren salidas en formato `<think>...</think>` con `boxed{score}`; para integración se recomienda parsear solo el valor dentro de `boxed{}` y considerar cómo la temperatura y la estrategia de sampling afectan la consistencia. Y crítico: el modelo se entrenó con K=32 respuestas por muestra, y el ablation muestra que K=1 (sin mecanismo de consenso) es sustancialmente peor que K=32 en todos los benchmarks. Si llamas a EvoQuality una vez con temperature 0, estás operando fuera de su régimen. Usa **al menos K=8, idealmente K=16**, y toma la mediana.

**Alternativa con mejor coste/beneficio para el eje perceptual:** RALI. Elimina la dependencia del proceso de razonamiento e incluso la necesidad de cargar un LLM en inferencia; para la tarea de scoring de calidad alcanza generalización comparable a los modelos basados en reasoning con menos del 5% de sus parámetros y tiempo de inferencia. Para ADA, eso significa: cero VRAM swap, latencia despreciable, y puedes correrlo **en cada imagen** en vez de racionar llamadas. Los pesos preentrenados de RALI están disponibles y el repo es de los mismos autores de ByteDance que Q-Insight.

---

## 3. ¿Existe algo mejor que EvoQuality para 2026?

Para *calidad perceptual pura* en fotografía: marginalmente. Q-Hawkeye (AMAP/Alibaba, ene-feb 2026) propone optimización de política visual con reponderación por incertidumbre y una Implicit Perception Loss que fuerza al modelo a anclar sus juicios en evidencia visual genuina, y reporta superar a los métodos SOTA generalizando mejor entre datasets. Está construido sobre un backbone de escala Qwen2.5-VL-7B, con huella de memoria similar a Q-Align, DeQA-Score, Q-Insight y VisualQuality-R1. Pero **no aporta ninguna de las capacidades que a ti te faltan** (identidad, adherencia, img2img).

Para lo que ADA realmente necesita, el trabajo que importa de 2025-2026 **no es IQA**, es *reward modeling de edición y consistencia*:

- **EditScore** es el hallazgo más directamente aplicable a tu fallback Miaomiao→Lustify. Es una serie de reward models (7B-72B) para evaluar calidad de edición guiada por instrucción, con EditReward-Bench como benchmark de evaluación sistemática, y las variantes Qwen3-VL de 4B y 8B logran que el 4B iguale al 32B original y el 8B iguale al 72B original. La API es literalmente `scorer.evaluate([input_image, output_image], instruction)` — tu caso de uso exacto.
- **PVC-Judge** es lo más cercano a un juez de identidad open-source que existe. Es un modelo pairwise de consistencia visual —preservación de identidad, estructura y coherencia semántica entre imagen editada y original— fine-tuneado desde Qwen3-VL-8B-Instruct con LoRA r=64, que alcanza 81,82 de accuracy media en VCReward-Bench frente a 76,89 de GPT-5.1.

**Nada open-source resuelve bien "compara candidato contra 1-5 referencias".** Es un vacío real del campo, y GEditBench v2 explica por qué lo evitaron: excluyeron tareas de edición multi-imagen porque los VLM open-source muestran una brecha sustancial frente a los propietarios en comprensión multi-imagen: Qwen2.5-VL-7B queda 8,41% por debajo de GPT-4o con cuatro imágenes, y la brecha se expande a 30,05% al aumentar el número de imágenes. **Consecuencia directa para ADA: nunca pases 5 referencias + candidato en una sola llamada. Haz N comparaciones 1-vs-1 y agrega.**

---

## 4. Rankings por tarea

### Mejor para calidad visual (perceptual)

1. **RALI** — mejor relación evidencia/VRAM/latencia del campo; ICLR 2026 Oral.
2. **EvoQuality Q8\_0** — mejor generalización cross-dataset entre VLM-IQA sin GT; corre en LM Studio hoy; requiere K≥8.
3. **Q-ReAlign Lite-4B** — mejor número absoluto reportado en AGIQA (0,829/0,871), pero contrato de scoring por logits y compatibilidad GGUF sin verificar.

*(Q-Hawkeye entra en el podio si liberan pesos y el A/B local lo confirma.)*

### Mejor para prompt adherence

1. **Checklist QA descompuesta + VLM** (patrón WeGenBench). No es un modelo: es descomponer el prompt en preguntas Sí/No con pesos y agregar. La ventaja clave es alta estabilidad e interpretabilidad: fijadas las preguntas, los focos de evaluación permanecen constantes, y la verificación ítem-por-ítem de restricciones duras (existencia de entidades, colores, formas, materiales, cantidades, posiciones) hace explícita la razón de cada descuento. Su límite conocido: fragmentar el prompt en preguntas micro puede desviar la captación de la semántica global — una imagen puede puntuar alto satisfaciendo todas las restricciones individuales y aun así resultar antinatural o lógicamente defectuosa.
2. **VQAScore** — usa un modelo VQA para producir un score calculando la probabilidad de respuesta "Sí" a "¿Muestra esta figura {texto}?", y con modelos off-the-shelf produce resultados SOTA en 8 benchmarks de alineación imagen-texto. Barato, sin generación de texto, ideal para gating.
3. **Q-Eval-Score / LMM4LMM** — Q-Eval-Score es un modelo unificado que evalúa calidad visual y alignment con mejoras específicas para alineación con prompts de texto largo; LMM4LMM evalúa desde múltiples dimensiones incluyendo calidad perceptual, correspondencia texto-imagen y precisión task-specific, sobre EvalMi-50K (2.100 prompts, 20 dimensiones, 100K MOS).

**No uses CLIPScore.** Los text encoders de CLIP actúan notoriamente como bag-of-words, confundiendo "el caballo come la hierba" con "la hierba come el caballo". Para tus categorías (acciones, cantidades, atributos, ropa) esto es descalificatorio.

### Mejor para identity / reference comparison

1. **PVC-Judge** (pairwise, 1 referencia vs 1 candidato por llamada).
2. **Ensemble de embeddings region-decoupled** — el pipeline de GEditBench v2 es directamente copiable: descomponen atributos humanos en tres propiedades ortogonales —Face ID, apariencia corporal y apariencia del pelo— excluyen dinámicamente el atributo modificado, y cuantifican los atributos estacionarios con modelos expertos especializados como ArcFace para Face ID; en la región no editada imponen invarianza estricta combinando SSIM, LPIPS y Earth Mover's Distance basada en CLIP.
3. **ID-Sim / DreamSim** — ID-Sim logra el mejor balance: alta sensibilidad a la identidad y baja sensibilidad contextual; DreamSim muestra sensibilidad moderada a identidad pero sigue siendo sensible a variación de fondo e iluminación, mientras DINOv3 es más invariante a punto de vista e iluminación pero más sensible a cambios de fondo; CLIP, OpenCLIP y LPIPS muestran la sensibilidad a identidad más débil.

**Dos avisos duros aquí.** (i) Las métricas de identidad de sujeto ampliamente usadas como CLIP-I y DINOv2 correlacionan pobremente con las preferencias humanas, porque se centran casi exclusivamente en similitud semántica e ignoran cambios de apariencia introducidos por iluminación, sombras, reflejos y contexto. (ii) **ArcFace no funciona en anime.** Un benchmark reciente de generación multi-shot lo resuelve exactamente como tendrás que hacerlo tú: enrutan a extractores específicos de dominio — DeepFace para contenido realista y una variante propia de InceptionNeXt fine-tuneada sobre datasets de anime para animación — y calculan el score como distancia entre embeddings. Para tu rama Miaomiao Anima16 necesitas un extractor de identidad separado o desactivar la métrica facial y apoyarte en DINOv3 sobre crop del sujeto.

### Mejor para Img2Img preservation (Miaomiao → Lustify)

1. **EditScore-Qwen3-VL-4B con** **`num_pass=4`** (self-ensembling Avg\@4). Es el fit exacto y el 4B rinde como un 32B.
2. **PVC-Judge** para la dimensión de consistencia, corriendo pairwise contra la fuente.
3. **Métricas region-decoupled** (LPIPS/SSIM/CLIP-EMD en región no editada + Face ID / DINOv3 en el sujeto).

**El error que vas a cometer si no lo evitas explícitamente.** GEditBench v2 lo bautizó *under-editing trap*: modelos como GLM-Image y Bagel logran scores de consistencia visual artificialmente inflados (1.109 y 987) precisamente porque su capacidad de instruction following disminuida (787 y 820) les impide modificar significativamente la imagen de entrada; esto valida la necesidad del ranking multi-dimensional, ya que evaluar la consistencia visual de forma aislada es insuficiente para valorar la competencia real de edición. Traducción a ADA: **si Lustify Img2Img devuelve algo casi idéntico al source de Miaomiao, tu métrica de preservación dará 10/10 y el fallback habrá fracasado en silencio.** La preservación debe puntuarse siempre acoplada a una métrica de mejora, nunca sola.

### Mejor para ADA con 16 GB

1. **Qwen3-VL-8B-Instruct GGUF Q5\_K\_M/Q6\_K + scaffolding ArtifactLens** — un solo modelo residente, +0,48 F1 en anatomía por escalado (no por tamaño).
2. **RALI + HADM + VQAScore** — el trío no-VLM. Suma \~4 GB, latencia de milisegundos, cero swaps, y cubre calidad + anatomía + adherencia básica.
3. **EditScore-Qwen3-VL-4B (LoRA fusionado → GGUF)** — el especialista de img2img más barato con evidencia peer-reviewed.

---

## 5. Respuesta a la pregunta central: A, B, C o D

**D, con un C barato incrustado en la etapa 1.** Y descarto A y B con evidencia, no por intuición.

**Contra A (un solo VLM fuerte):** no tienes hardware para el VLM que haría falta. El mejor open-source en juicio multimodal es Qwen3-VL-32B a 64,6% de media en MMRB2, y ese modelo no cabe en 16 GB a una cuantización que preserve calidad de juicio. MJ1 demuestra que con solo 3B de parámetros activos supera sustancialmente a modelos con órdenes de magnitud más parámetros, reforzando que la receta de entrenamiento importa más que la escala del modelo para tareas de juicio — es decir, escalar tu VLM generalista es el camino de peor retorno.

**Contra B (un solo VLM especializado):** ningún modelo cubre tus siete tareas. Q-ReAlign lo declara explícitamente fuera de alcance: fuera de alcance: moderación de contenido/seguridad, juicios factuales o de identidad, y grading médico/forense; la calidad es perceptual y está condicionada por el dataset.

**Contra C puro (ensemble de VLM especialistas):** el coste es prohibitivo en tu configuración. Cada VLM especialista de 4-8B en GGUF es 3-6 GB y un swap de VRAM. Si corres EvoQuality + EditScore + PVC-Judge + un adherence-VLM en cada imagen, estás en 4 cargas/descargas por review. Con ComfyUI compitiendo por VRAM, eso domina la latencia total.

**A favor de D:** ArtifactLens da el dato decisivo sobre dónde poner el esfuerzo. Ablacionar los specialists (manteniendo ICL y optimización de texto) reduce el F1 solo 0,05 de media, por lo que los practicantes pueden intercambiar: si toleran esa pérdida, pueden cambiar a llamadas VLM únicas con optimización, ahorrando el coste de inferencia de múltiples llamadas. Ablacionar el ICL (-0,265) es mucho más significativo que ablacionar la optimización de texto (-0,022). Es decir: **el 84% de la ganancia viene de in-context learning y prompting, no de tener más modelos.** Y sus propias recomendaciones lo confirman: el baseline de VLM único es generalmente bastante fuerte y es más barato y rápido que la arquitectura multi-specialist; el in-context learning es efectivo incluso como única estrategia de optimización sobre una sola llamada VLM, y es lo más simple de implementar.

### Comparativa cuantitativa (estimaciones propias, marcadas como tales)

| Arquitectura VRAM pico Swaps/imagen Latencia est. Calidad de juicio esperada  |                   |                               |                               |                                             |
| ----------------------------------------------------------------------------- | ----------------- | ----------------------------- | ----------------------------- | ------------------------------------------- |
| A — Qwen3-VL-32B Q4                                                           | \~20 GB (offload) | 1                             | muy alta                      | \~64% MMRB2                                 |
| B — EvoQuality solo                                                           | \~9 GB            | 1                             | media                         | Bueno en calidad, ciego en 5/7 tareas       |
| C — 4 VLM especialistas                                                       | \~9 GB            | 4                             | muy alta                      | Mejor por tarea, coste 4×                   |
| **D — jerárquico (recomendado)**                                              | **\~9 GB**        | **1 (típico) / 2 (escalado)** | **baja en el \~80% de casos** | **Mejor que A en anatomía; comparable a C** |

*(Inferencia propia a partir de tamaños de modelo, throughput reportado por Doradus y la tabla de complejidad de Q-Hawkeye.)*

---

## 6. Arquitectura recomendada: ADA Visual Review vNext

### Etapa 0 — Métricas deterministas (siempre, \~0,3 s, <4 GB, residentes)

Corren en un servicio Python persistente que **nunca se descarga**. Esto es el "C barato".

| Señal Modelo Cuándo              |                                                              |                               |
| -------------------------------- | ------------------------------------------------------------ | ----------------------------- |
| `q_perceptual`                   | RALI (CLIP-based)                                            | Siempre                       |
| `anatomy_boxes`                  | HADM-L + HADM-G                                              | Solo si hay persona detectada |
| `adherence_raw`                  | VQAScore sobre checklist del prompt                          | Siempre                       |
| `id_face`, `id_body`             | ArcFace (realista) / InceptionNeXt-anime + DINOv3 sobre crop | Solo si hay referencia        |
| `preserve_bg`, `preserve_struct` | LPIPS + SSIM + CLIP-EMD en región no editada                 | Solo en rama img2img          |

Nota de dominio: RALI y HADM están calibrados sobre foto/SDXL. **Recalibra los umbrales con 200 imágenes tuyas por rama (Lustify realista vs Anima16 anime) antes de confiar en valores absolutos.** Usa percentiles de tu propia distribución, no thresholds del paper.

### Etapa 1 — Cheap Reviewer (siempre, un solo VLM residente)

**Modelo:** Qwen3-VL-8B-Instruct GGUF Q5\_K\_M en LM Studio (o EvoQuality Q8\_0 si priorizas el eje perceptual y aceptas perder adherencia).

**Contrato de prompt — cinco reglas no negociables, todas derivadas de la evidencia de §0:**

1. **Decide primero, justifica después.** Formato `Decide-Before-Reason`. Nunca CoT libre antes del veredicto.
2. **Salida binaria/ternaria por dimensión, no 0-10.** Elimina la tendencia central que produce tus 10/10.
3. **Prompting agresivo, no conservador.** Instrucción explícita del tipo *"marca el defecto aunque tu confianza sea solo del 30%; un falso negativo es un fallo crítico, un falso positivo es aceptable"*. Esto es full-spectrum prompting: con COPRO el 96% de los prompts generados eran de alta precisión y 0% de alto recall, con F1 medio 0,687; con COPRO-FullSpectrum la distribución pasó a 22% alta precisión y 74% alto recall, con F1 medio 0,780 — un 15% superior.
4. **In-context learning con demostraciones contrafactuales.** Es la palanca más grande (-0,265 F1 al quitarla). Construye un banco de \~200-400 imágenes tuyas etiquetadas PASS/FAIL, y en cada llamada inyecta \~10 ejemplos recuperados por similitud CLIP, **emparejados**: se muestran las demostraciones en pares, una con artefactos y otra sin ellos que sean visualmente muy similares — si la diferencia principal entre dos imágenes es la presencia de un artefacto, la tarea debería ser más fácil de aprender. Con solo 400 muestras de entrenamiento y 200 de validación, ArtifactLens alcanza F1 0,744, apenas un 9% por debajo del modelo más fuerte. **Cuatrocientas etiquetas. Eso es una tarde de trabajo.**
5. **Crops, no imagen completa, para defectos pequeños.** Recortan regiones de interés con GroundingDINO usando términos fijos por tipo de error —'face' para defectos faciales, 'hand' para manos, 'human' para el resto— con padding de 0,15 para 'human', 0,25 para 'face' y 0,5 para 'hands'. Las cajas de HADM de la etapa 0 te dan estos crops gratis.

### Reglas de fusión de scores

**Nunca promedies.** Usa el patrón de techo estructural de WeGenBench: desacoplan explícitamente la corrección estructural del atractivo estético — la dimensión de estructura (deformaciones anatómicas, texto ininteligible, imposibilidades físicas) tiene poder de veto — y aplican `Final = min(Structural Ceiling, Overall Quality)`; si la estructura se evalúa como inferior en cualquier nivel k, el techo se limita estrictamente a k-1. Además: ante empate entre decisiones adyacentes, el sistema adopta conservadoramente la inferior.

```
structural_ceiling = f(anatomy_boxes, VLM_anatomy_flag)   # veto
score_final = min(structural_ceiling,
                  w1·q_perceptual + w2·adherence + w3·aesthetic)

```

Pesos sugeridos: 0,35 / 0,45 / 0,20. Ajusta contra tus 400 etiquetas por regresión logística, no a ojo.

### Hard failures (FAIL inmediato, sin escalado)

- HADM-G detecta extremidad extra o faltante con confianza > umbral calibrado
- HADM-L: ≥2 defectos locales severos, o 1 en cara con área > X% del frame
- `adherence_raw` falla una restricción de cardinalidad o de presencia de entidad (los "hard constraints" del checklist)
- Rama img2img: `preserve_bg` por debajo del percentil 5 de tu distribución (el segundo renderer destruyó la escena)
- Rama img2img: **`preserve_*`** **en el percentil 99 Y** **`q_perceptual`** **sin mejora** → under-editing trap, el fallback no hizo nada útil

### Escalado a Hard Reevaluate

Escala solo cuando se cumpla alguna de estas (esperado: \~15-25% de las imágenes):

- **Zona gris:** `score_final` dentro de ±0,5σ del umbral PASS/FAIL
- **Desacuerdo entre etapas:** etapa 0 y etapa 1 discrepan en signo
- **Baja auto-consistencia:** si usas EvoQuality con K muestras y la varianza de la mediana es alta. Este es exactamente el criterio que Q-Hawkeye convierte en señal de entrenamiento: estima incertidumbre predictiva usando la varianza de los scores predichos a través de múltiples rollouts
- **Todo el pipeline de fallback:** cualquier imagen que pase por Miaomiao → Lustify Img2Img
- **Ranking A/B explícito:** cualquier decisión pairwise que vayas a persistir

### Etapa 2 — Hard Reviewer

**Composición:** dos especialistas, cargados bajo demanda, elegidos por tipo de duda.

| Tipo de duda Modelo Modo  |                                                                |                                           |
| ------------------------- | -------------------------------------------------------------- | ----------------------------------------- |
| Preservación img2img      | **EditScore-Qwen3-VL-4B**, `num_pass=4`                        | `evaluate([source, output], instruction)` |
| Identidad vs referencias  | **PVC-Judge**                                                  | N llamadas pairwise 1-vs-1, nunca 1-vs-5  |
| Calidad perceptual dudosa | **EvoQuality Q8\_0**, K=16, mediana                            | Pointwise + pairwise                      |
| Anatomía dudosa           | Etapa 1 con specialists por parte (hand/face/limb) sobre crops | Logical-OR sobre specialists              |

Para pairwise, aplica el debiasing posicional: ejecutan múltiples variantes de posición intercambiando dinámicamente izquierda y derecha, y agregan los votos válidos; si existe mayoría clara determina la decisión, y ante empate entre decisiones adyacentes se adopta conservadoramente la inferior. Sin esto, un juez de 8B prefiere sistemáticamente una posición — MJ1 lo midió: antes de la recompensa de consistencia, el modelo seleccionaba la Respuesta A aproximadamente el doble de veces que la B dentro de cada batch pese a etiquetas ground-truth balanceadas.

### Minimización de swaps de VRAM

1. **Servicio Python persistente** (RALI + HADM + VQAScore + embeddings ≈ 4 GB) que nunca se descarga. Separado de LM Studio.
2. **Un único VLM residente en LM Studio** para la etapa 1 (\~6 GB Q5\_K\_M). Total en reposo ≈ 10 GB, dejando margen.
3. **Batching por lote, no por imagen.** Genera 20 imágenes en ComfyUI → descarga ComfyUI → corre etapa 0+1 sobre las 20 → recoge las escaladas → carga *un* especialista → procesa todas las escaladas de ese tipo → siguiente especialista. Esto convierte 20 imágenes × 4 swaps en 3 swaps totales.
4. **Ordena la cola de escalado por especialista**, no por timestamp.
5. Si acabas necesitando dos VLM simultáneos, **EditScore-4B es tu segundo residente**, no PVC-Judge-8B: cuatro veces menos memoria por prácticamente el mismo rendimiento que el 32B original.

---

## 7. Qué merece un A/B test local (en este orden)

| Prioridad Test Coste Qué esperas ver  |                                                                                            |                         |                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------- | ------------------------------------------------------------------------------ |
| **1**                                 | **Prompt agresivo + ICL contrafactual vs tu prompt actual**, mismo `qwen3-vl-8b`           | \~1 día (400 etiquetas) | El mayor delta de todo el proyecto. Evidencia: +0,48 F1 en anatomía para un 7B |
| **2**                                 | **Decide-Before-Reason vs Reason-Then-Decide**, mismo modelo                               | 2 horas                 | Igual accuracy, latencia sustancialmente menor a igualdad de acierto           |
| **3**                                 | **Pairwise vs pointwise 0-10** en 100 pares tuyos con GT humana                            | 1 día                   | Acuerdo con humano notablemente superior en pairwise                           |
| **4**                                 | **EvoQuality Q8\_0 con K=1 vs K=8 vs K=16**                                                | 3 horas                 | Salto grande de K=1 a K=8; retorno decreciente después                         |
| **5**                                 | **RALI vs EvoQuality Q8\_0** en tus 400 etiquetas, ambas ramas                             | 1 día                   | Si RALI queda dentro de 0,03 SRCC, quita EvoQuality del pipeline               |
| **6**                                 | **HADM en Blackwell** (viabilidad técnica antes que calidad)                               | 1 día                   | Si el port no arranca, cae a ArtifactLens-sobre-VLM                            |
| **7**                                 | **EditScore-4B** **`num_pass=1`** **vs** **`num_pass=4`** en 50 casos Miaomiao→Lustify     | medio día               | Avg\@4 es la config recomendada por los autores                                |
| **8**                                 | **PVC-Judge vs Qwen3-VL-8B base**, mismo prompt pairwise, 100 pares de identidad           | 1 día                   | PVC-Judge supera consistentemente a su modelo base en todas las tareas         |
| **9**                                 | **Extractor de identidad anime** (DINOv3 crop vs InceptionNeXt-anime) para la rama Anima16 | 2 días                  | ArcFace debería fallar visiblemente aquí                                       |
| **10**                                | Q-ReAlign Lite-4B — **primero verifica si convierte a GGUF**, luego evalúa                 | 1 día                   | Alto riesgo de bloqueo por arquitectura `qwen3_5`                              |

---

## 8. Sobre `Q-ReAlign` vs `ReAligned-Qwen`

Confirmado: son cosas distintas y hay un tercer homónimo que contamina las búsquedas. `Q-ReAlign` es de Q-Future (autores de Q-Align/Q-Bench): la nueva versión de Q-Align, entrenada sobre VLM modernos, que obtiene el mismo rendimiento con un 50% menos de parámetros, con tres tamaños. **No confundir con "Q-realign: Piggybacking Realignment on Quantization for Safe and Efficient LLM Deployment"** (arXiv 2601.08089), que es una defensa de seguridad post-cuantización para LLM de texto y no tiene nada que ver con IQA.

---

## 9. Lo que no encontré (y deberías saberlo)

- **No existe ningún modelo público llamado** **`WeGenBench-Consistency-CoT`****.** WeGenBench es un benchmark de Weixin/Tencent con 4.000 prompts bilingües, y su métrica CoT usa un VLM fine-tuneado internamente (p. ej. Qwen-VL) sobre corpus de "expert review" anotados por humanos, con greedy decoding a temperatura 0, que emite un JSON estructurado con evaluación global, categorías de descuento con penalizaciones y un score holístico de 1 a 10. **Ese checkpoint no está liberado.** Lo valioso de WeGenBench para ti es la metodología (dual-track QA + CoT, anchor-based grading, structural ceiling), no un peso descargable. Es replicable con tu propio VLM.
- **MJ1 tiene demo pero no pesos confirmados.** Si Haize Labs los libera, Qwen3-VL-30B-A3B + LoRA con 3B activos es el candidato más interesante para tus 16 GB en el medio plazo — un MoE con offload parcial a tus 64 GB de RAM es viable donde un denso de 30B no lo es.
- **La tarea es intrínsecamente subjetiva y eso acota tu techo.** En detección de artefactos de mano, la predicción por voto mayoritario de diez anotadores humanos alcanza F1 0,701 con precisión 0,809 y recall 0,618, y la kappa de Cohen por pares es 0,639 ± 0,078, entre acuerdo "moderado" y "sustancial". No persigas un reviewer que acierte el 95%. Persigue uno que tenga recall alto y falle hacia el lado seguro, porque un FAIL falso te cuesta una regeneración y un PASS falso te cuesta una imagen publicada con tres manos.

---

### Fuentes primarias

EvoQuality: [arXiv 2509.25787](https://arxiv.org/abs/2509.25787) · [ICLR 2026 PDF](https://arxiv.org/pdf/2509.25787) · [HF ByteDance/EvoQuality](https://huggingface.co/ByteDance/EvoQuality) · [GitHub](https://github.com/bytedance/EvoQuality)
Q-ReAlign: [HF q-future/Q-ReAlign-Lite-4B](https://huggingface.co/q-future/Q-ReAlign-Lite-4B) · [Q-Align GitHub](https://github.com/Q-Future/Q-Align)
RALI (ICLR 2026 Oral): [arXiv 2510.11369](https://arxiv.org/abs/2510.11369) · [GitHub](https://github.com/xuanyuzhang21/RALI)
Q-Hawkeye: [arXiv 2601.22920](https://arxiv.org/abs/2601.22920) · [GitHub](https://github.com/aba122/Q-Hawkeye)
EditScore (ICLR 2026): [arXiv 2509.23909](https://arxiv.org/abs/2509.23909) · [GitHub](https://github.com/VectorSpaceLab/EditScore)
EditReward: [arXiv 2509.26346](https://arxiv.org/pdf/2509.26346)
GEditBench v2 / PVC-Judge: [arXiv 2603.28547](https://arxiv.org/html/2603.28547v1) · [HF GEditBench-v2/PVC-Judge](https://huggingface.co/GEditBench-v2/PVC-Judge)
ArtifactLens: [arXiv 2602.09475](https://arxiv.org/pdf/2602.09475)
HADM: [arXiv 2411.13842](https://arxiv.org/abs/2411.13842) · [GitHub](https://github.com/wangkaihong/HADM)
MagicMirror / MagicAssessor: [arXiv 2509.10260](https://arxiv.org/abs/2509.10260) · [HF wj-inf/MagicAssessor-7B](https://huggingface.co/wj-inf/MagicAssessor-7B)
MMRB2: [arXiv 2512.16899](https://arxiv.org/abs/2512.16899) · [GitHub facebookresearch/MMRB2](https://github.com/facebookresearch/MMRB2)
MJ1: [arXiv 2603.07990](https://arxiv.org/pdf/2603.07990)
WeGenBench: [arXiv 2606.20100](https://arxiv.org/html/2606.20100v1)
HPSv3 (ICCV 2025): [arXiv 2508.03789](https://arxiv.org/pdf/2508.03789) · [GitHub](https://github.com/MizzenAI/HPSv3)
Q-Eval-100K (CVPR 2025 Oral): [arXiv 2503.02357](https://arxiv.org/abs/2503.02357)
LMM4LMM (ICCV 2025): [CVF Open Access](https://openaccess.thecvf.com/content/ICCV2025/html/Wang_LMM4LMM_Benchmarking_and_Evaluating_Large-multimodal_Image_Generation_with_LMMs_ICCV_2025_paper.html)
VQAScore (ECCV 2024): [página del proyecto](https://linzhiqiu.github.io/papers/vqascore/)
ID-Sim: [arXiv 2604.05039](https://arxiv.org/html/2604.05039)
Compendio actualizado de IQA: [Awesome-Image-Quality-Assessment](https://github.com/chaofengc/Awesome-Image-Quality-Assessment)

Si quieres, puedo profundizar en cualquiera de los diez A/B tests — en particular el diseño del banco de 400 etiquetas contrafactuales, que es donde está el mayor retorno y donde es más fácil construirlo mal.