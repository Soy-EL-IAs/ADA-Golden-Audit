# M1 — Creative Expansion Lab

Text-only, pre-`PremiseSpec` experiment. It asks ADA's configured production
27B model for exactly twelve static `ConceptProposal` objects in one structured
generation.

This directory is intentionally disconnected from ComfyUI, MiniMax, the
specialist orchestrator, run state, and production schemas. It reads the
existing character database, active prompt-guide registry, runtime instruction,
model routing config, and the isolated extreme diagnostic guide as source
material without copying or changing them.

Run from the ADA root while LM Studio is serving the configured model:

```powershell
python experimental/m1_creative_expansion_lab/run_m1.py --character 2B --version NieR:Automata
```

The runner performs a read-only preflight, first makes one non-creative native
transport smoke check (`reasoning: off` with visible content), then records the
exact request and makes one creative generation call through LM Studio's native
`/api/v1/chat` endpoint. It validates the returned JSON locally and stops on any
transport/schema failure. It never retries or calls a fallback transport.

Run the isolated unit tests with:

```powershell
python -m unittest experimental.m1_creative_expansion_lab.test_m1
```
