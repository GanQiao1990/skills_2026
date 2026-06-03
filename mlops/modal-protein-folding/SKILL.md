---
name: modal-protein-folding
description: Run protein structure prediction workloads on Modal GPUs while saving final artifacts locally. Use when adapting folding/design examples so remote inference returns mmCIF/PDB text and the local entrypoint writes verified output files.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Modal protein folding

Use this skill when:
- a user wants to run protein structure prediction on Modal
- the source pattern is a Modal example for ESMFold2 or similar folding models
- the user wants the final `.cif` / `.pdb` saved locally after remote GPU inference
- you need a reliable "remote compute, local artifact" workflow

## Core pattern

1. Keep model installation and GPU runtime definition in the Modal image/class.
2. Load the model inside `@modal.enter()` so each container warms once.
3. Perform folding in a `@modal.method()` and return structure text plus summary metrics.
4. In `@app.local_entrypoint()`, call the remote method and write the returned structure text to a local file.
5. Verify the local artifact exists and report path, size, and model metrics.

## Recommended workflow

1. Start from the existing upstream/example script instead of rewriting from scratch.
2. Replace the example sequence/complex input with the user sequence or a CLI override.
3. Keep the remote method minimal: build `StructurePredictionInput`, run inference, return `to_mmcif()` (or PDB text if needed) and confidence metrics.
4. Make the local entrypoint responsible for:
   - choosing default output path
   - creating parent directories
   - calling `.remote(...)`
   - printing pLDDT / pTM / ipTM
   - writing the text locally
5. Run the script with `modal run ...` and do not stop until the local artifact is verified.

## Pitfalls

- Mount keys in `volumes={...}` should be strings or `PurePosixPath` values. In practice, use `"/models"` rather than `Path("/models")` to avoid avoidable type/lint friction.
- Do not reuse an `Optional[str]` parameter variable as a `Path` object. Convert into a separate `output_file` variable.
- First-run latency can be dominated by image build, dependency install, and model download. Do not mistake that startup time for a hung fold job.
- For single-chain jobs adapted from multimer examples, simplify the `StructurePredictionInput` to one `ProteinInput` unless the user explicitly asks for nucleic acids/ligands.
- When running through Hermes, `terminal()` foreground execution cannot exceed the platform foreground limit. For potentially long `modal run ...` jobs, prefer Hermes background execution with `notify_on_complete=true`, then inspect logs with `process(wait|poll|log)` and verify the local output file after exit.

## Verification checklist

Before finishing, confirm all of the following:
- script file exists locally
- `modal run` completed successfully
- output `.cif` or `.pdb` exists locally
- output path is reported explicitly
- file size is non-zero
- confidence metrics are reported from the actual run

## Support files

- `references/esmfold2-local-cif-pattern.md` — concrete ESMFold2 pattern for returning mmCIF text from remote Modal inference and saving it locally.
- `references/hermes-long-modal-run-pattern.md` — how to run long Modal folding jobs through Hermes using background execution, process wait/poll, and post-run local artifact verification.

## Scope notes

This skill complements general Modal and ESM skills. Use those for broader platform/model knowledge; use this skill for the recurring delivery pattern where protein folding runs remotely but the user expects a local saved structure file.
