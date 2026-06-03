# ESMFold2 single-sequence Modal pattern: remote GPU inference, local CIF output

Use this when adapting a Modal example so a remote GPU job returns structure text and the local entrypoint saves the result on the caller's filesystem.

## Working pattern

- Keep heavy model loading inside `@app.cls(..., gpu=...)` and `@modal.enter()`.
- Keep the inference method remote with `@modal.method()`.
- Return the mmCIF text from the remote method.
- In `@app.local_entrypoint()`, call `fold.remote(...)` and write the returned text locally with `Path(...).write_text(...)`.
- This preserves Modal GPU execution while still leaving the final `.cif` on the local machine.

## Minimal structure

```python
models_dir = "/models"
volume = modal.Volume.from_name("esmfold2-models", create_if_missing=True)

@app.cls(image=image, volumes={models_dir: volume}, gpu="H100")
class Inference:
    @modal.enter()
    def load_model(self):
        self.model = ESMFold2Model.from_pretrained(...).cuda().eval()

    @modal.method()
    def fold(self, sequence: str) -> tuple[str, float, float, float]:
        spi = StructurePredictionInput(
            sequences=[ProteinInput(id="A", sequence=sequence.strip())]
        )
        result = ESMFold2InputBuilder().fold(self.model, spi)
        return (
            result.complex.to_mmcif(),
            float(result.plddt.mean()),
            float(result.ptm),
            float(result.iptm),
        )

@app.local_entrypoint()
def main(sequence: str, output_path: str | None = None):
    output_file = Path(output_path) if output_path else Path("outputs/prediction.cif")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cif_text, plddt, ptm, iptm = Inference().fold.remote(sequence=sequence)
    output_file.write_text(cif_text)
```

## Pitfalls caught in real use

1. `volumes={models_dir: volume}` expects a string or `PurePosixPath` mount key.
   - Use `models_dir = "/models"`, not `Path("/models")`, to avoid type/lint friction.

2. In the local entrypoint, avoid reusing an `Optional[str]` variable as a `Path`.
   - Prefer:
     - `output_path: Optional[str] = None`
     - `output_file = Path(output_path) if output_path else ...`
   - This prevents `Optional[str]` / `Path` type confusion in static analysis.

3. For long first runs, expect image build + dependency resolution + model download before inference starts.
   - The first successful ESMFold2 run may spend several minutes before folding begins.

## Verified outcome pattern

A single-chain ESMFold2 run for an 890 aa protein completed successfully on Modal with:
- remote GPU execution on H100
- returned mmCIF text
- local save to `protein-folding/outputs/...cif`
- metrics printed by the local entrypoint (`pLDDT`, `pTM`, `ipTM`)

Use this as the default pattern for "run on Modal but save artifact locally" protein folding tasks.
