# Análisis — Worker Vision v1

## Resultado

`qwen/qwen3-vl-8b` completó 14 de 15 revisiones JSON válidas. El Worker fue cargado sin competir con el Master, se descargó al finalizar y el Master se restauró porque estaba cargado al inicio.

- Carga del Worker: 2.672 s.
- Revisión media: 2.343 s por pareja.
- Total de inferencia: 32.798 s para 14 resultados válidos.
- Veredictos: 5 PASS, 1 REVIEW, 8 REJECT; una respuesta JSON incompleta registrada como error sin reintento.

Una revisión de 100 imágenes, a este ritmo, sería aproximadamente 3.9 minutos de inferencia más carga y E/S. El rendimiento es adecuado para triage masivo local.

## Detección objetiva

- **Duplicado 2B:** `2b_duplicate_pair` fue REJECT y marcó dos sujetos. Correcto.
- **Tifa con cámara física:** `tifa_camera_and_back_drift` fue PASS y no reportó la cámara visible. Falso PASS importante.
- **2B close-up correcto:** `2b_closeup_blindfold_ok` fue REJECT por una supuesta contradicción de blindfold que no es inequívoca. Falso REJECT probable.
- **2B con blindfold removido en el prompt:** `2b_blindfold_eye_visible` fue REJECT porque el resultado mantuvo parte del blindfold. Es una detección de incoherencia prompt→imagen, pero no debe contarse como test canónico de “blindfold con ojos visibles”, porque el propio prompt pide revelarlos.
- **Anatomía/drift:** el Worker marcó varias manos, extremidades y drifts en 2B. Algunos casos son plausibles, pero su severidad es demasiado alta para aprobar rechazo automático sin segunda opinión.

## Scores subjetivos

`visual_appeal` y `viral_hook` se concentraron mayormente entre 8 y 9, incluso en REJECT. Son útiles como señal exploratoria, pero por ahora tienen poca capacidad de ordenar calidad fina. `animation_potential` debe interpretarse del mismo modo.

## Thresholds provisionales (no integrados)

- **PASS candidato:** `single_subject=true`, identidad >= 8, anatomía >= 8, sin issue crítico explícito y appeal/viral >= 7.
- **REVIEW:** cualquier contradicción de identidad/outfit/accesorio, anatomy 6–7, drift visible o scores subjetivos débiles.
- **REJECT candidato:** `single_subject=false`, identidad <= 5, anatomía <= 5 o issue crítico inequívoco (duplicado, cámara física, oclusión incompatible).

Estos thresholds sólo sirven para ordenar revisión humana. El 8B no debe disparar regeneración ni rechazo definitivo.

## Recomendación

Decisión **B**: funciona parcialmente. Hacer un benchmark comparativo pequeño 8B vs Master 27B sobre seis bordes: 2B correcto, 2B duplicado, 2B con supuesta oclusión, Tifa close-up REVIEW, Tifa dinámica REJECT y Tifa con cámara física PASS. La comparación debe medir especialmente falsos PASS y falsos REJECT antes de integrar el Worker al pipeline.
