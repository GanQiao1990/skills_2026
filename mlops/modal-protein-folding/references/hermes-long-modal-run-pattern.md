# Hermes long Modal run pattern

Use this pattern when a Modal protein-folding job may exceed Hermes foreground terminal limits or spend several minutes in image build / weight download.

## Recommended execution pattern

1. Start the run in the background:
   - `terminal(background=true, notify_on_complete=true, command="modal run ...")`
2. Use `process(action="wait")` or `process(action="poll")` to monitor progress.
3. After completion, verify the local artifact explicitly:
   - file exists
   - non-zero size
   - modification time updated
   - optional checksum (`sha256sum`) for reproducibility
4. If useful, read the first lines of the mmCIF/PDB to confirm it is structurally valid text output.

## Why this matters

Modal runs can be dominated by image startup, dependency install, model weight fetch, or checkpoint shard loading before the actual fold starts. A silent few-minute interval is not necessarily a hang.

## Concrete signals worth extracting from logs

- sequence length used for folding
- `num_loops`, `num_sampling_steps`, `num_diffusion_samples`, `seed`
- confidence metrics such as mean `pLDDT`, `pTM`, `ipTM`
- exact local output path written by the entrypoint

## Example from this session class

A single-chain ESMFold2 glnD run followed this pattern successfully:
- background `modal run protein-folding/glnd_esmfold2.py`
- wait/poll until completion
- confirm local mmCIF path, size, checksum, and header text
- report actual model metrics from the run instead of assuming success from partial logs
