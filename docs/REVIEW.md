# Guía de review

Abrí `klein_batch_runs/<batch_id>/gallery.html` en Chrome o Edge. Cada tarjeta es Illustrious a la izquierda y Klein a la derecha.

Para cada pareja, preguntá:

- ¿Sigue siendo el mismo personaje (rostro, pelo, silueta)?
- ¿Klein preservó outfit, accesorios, pose y ángulo de cámara?
- ¿Hay anatomía rota, imagen incompleta o salida corrupta?
- ¿El acabado mejoró sin cambiar la composición?
- ¿Sirve como referencia de identidad o como primer frame para video?

`review_batch` puede producir `review.json`, pero es una ayuda automática: guardá la decisión creativa humana como criterio final.

## Worker Vision v1

`scripts/run_visual_review_benchmark.py` revisa sólo imágenes existentes con `qwen/qwen3-vl-8b`. Carga el Worker tras descargar los LLMs, lo descarga al terminar y restaura el Master únicamente si estaba cargado al inicio. No inicia ComfyUI ni modifica batches.

```powershell
python scripts/run_visual_review_benchmark.py --benchmark-id worker_vision_v1_001
```

Cada corrida nueva queda en `visual_review_runs/<benchmark_id>/` con `results.jsonl`, `summary.json` y `report.md`. La salida contiene un veredicto provisional y scores heurísticos; no dispara regeneración automática.

El schema v1 es: `verdict`, `identity`, `anatomy`, `single_subject`, `visual_appeal`, `viral_hook`, `animation_potential`, `identity_issues`, `visual_issues` y `reason`. `review_batch` usa el mismo schema sobre comparaciones existentes.
