# Archived skill: disco-multi-enzyme-pathway-design

Original path: `mlops/disco-multi-enzyme-pathway-design`

---

---
name: disco-multi-enzyme-pathway-design
category: mlops
description: Design complete multi-enzyme metabolic pathways in DISCO. Translate biochemical reaction tables into 7+ enzyme JSON configs, identify rate-limiting steps, incorporate real cofactors/metal ions/aqueous conditions, generate serial design scripts, and create comprehensive documentation (quick ref, full guide, index, delivery checklist).
triggers:
  - "Multi-enzyme cascade design (3+ enzymes)"
  - "Metabolic pathway optimization"
  - "Rate-limiting step identification and prioritization"
  - "Cofactor and metal ion integration into DISCO configs"
  - "Aqueous condition specification (pH, ionic strength, reducing agents)"
  - "Complete pathway documentation and automation"
---

## Overview

This skill translates a **biochemical reaction table** (steps, enzyme names, substrates, products, cofactors, flux rates, rate-limiting flags) into a complete DISCO multi-enzyme design framework. It handles:

- **Pathway structuring**: 7+ enzyme JSON configs from a single reaction table
- **Rate-limiting step prioritization**: Identify bottlenecks and design priority order
- **Real biochemistry**: Cofactors (SAM, ATP, NAD+, etc.), metal ions (Cu²⁺, Mg²⁺, Zn²⁺), aqueous conditions (pH, ionic strength, reducing agents)
- **Serial design automation**: Avoid GPU OOM with seed-by-seed runners
- **Multi-document guidance**: Quick reference, full guide, detailed index, delivery checklist

## Prerequisites

- DISCO repo at `/home/qiao/qiao_design/DISCO` (or any path)
- Biochemical reaction table with: step, enzyme name, substrates, products, cofactors, flux rate, rate-limiting flag
- PubChem CIDs for all small molecules (or ability to generate 3D SDF via RDKit/OpenBabel)
- NVIDIA GPU + CUDA 12.1, `uv`, HF mirror access

## 1) Input: Biochemical Reaction Table

Example (ergothioneine synthesis):

| 步骤 | 反应 | 酶名称 | 底物 | 产物 | 辅因子/金属离子 | 相对通量 | 限速 |
|------|------|--------|------|------|-----------------|---------|------|
| 1 | His + PRPP → His-tRNA | HisRS | L-His, PRPP | His-tRNA | ATP, Mg²⁺ | 8.5 | 否 |
| 2 | His-tRNA + SAM → 1-MeHis-tRNA | HisM | His-tRNA, SAM | 1-MeHis-tRNA | SAM | 7.9 | **是** |
| 3 | 1-MeHis + O₂ → 1-MeHis-SO | CuAO | 1-MeHis, O₂ | 1-MeHis-SO | Cu²⁺, O₂ | 7.3 | **是** |
| 4 | 1-MeHis-SO + Cys → EGT-precursor | MPST | 1-MeHis-SO, Cys | EGT-precursor | 硫源 | 5.8 | **是** |
| 5 | EGT-precursor → EGT-cyclic | Cyclase | EGT-precursor | EGT-cyclic | - | 5.2 | **是** |
| 6 | EGT-cyclic + Protein → EGT-Protein | PTM | EGT-cyclic, Protein | EGT-Protein | - | 3.1 | 是 |
| 7 | EGT-Protein → EGT (mature) | Proteasome | EGT-Protein | EGT | ATP | 2.5 | 是 |

Key columns:
- **Flux rate**: Relative throughput (higher = less bottleneck)
- **Rate-limiting flag**: Marks steps that constrain overall pathway flux
- **Cofactors**: SAM, ATP, NAD+, metal ions, etc.

## 2) Extract Cofactor & Aqueous Condition Matrix

Create a reference table for each enzyme:

```
| Enzyme | Cofactor | Concentration | Aqueous Condition |
|--------|----------|----------------|-------------------|
| HisRS | ATP, Mg²⁺ | 5-10 mM ATP, 2-5 mM Mg²⁺ | pH 7.5, 150 mM NaCl, 37°C |
| HisM | SAM | 1-5 mM | pH 7.5, 150 mM NaCl, 37°C |
| CuAO | Cu²⁺, O₂ | 0.1-1 mM Cu²⁺, saturated O₂ | pH 7.0, 150 mM NaCl, 37°C, **aerobic** |
| MPST | L-Cys or H₂S | 1-10 mM | pH 7.5, 150 mM NaCl, 37°C, 5-10 mM DTT |
| Cyclase | (possibly Zn²⁺) | - | pH 7.0, 150 mM NaCl, 37°C |
| PTM | - | - | pH 7.0, 150 mM NaCl, 37°C |
| Proteasome | ATP | 5-10 mM | pH 7.0, 150 mM NaCl, 37°C |
```

Standard aqueous conditions (unless enzyme-specific):
- **pH**: 7.0–7.5 (Tris-HCl or Hepes buffer)
- **Ionic strength**: 150 mM NaCl or KCl
- **Temperature**: 37°C (mammalian) or 30°C (microbial)
- **Reducing agent**: 5–10 mM DTT or TCEP (for Cys/Met protection)
- **Buffer**: 50 mM Tris-HCl or Hepes

## 3) Generate DISCO JSON Configs (One per Enzyme)

For each enzyme, create `input_jsons/step<N>_<EnzymeName>.json`:

### ⚠️ CRITICAL: Path Format (Common Pitfall)

**WRONG** (will fail with \"Bad input file\" error):
```json
{\"ligand\": {\"ligand\": \"FILE_ergothioneine/substrates/L_His.sdf\", \"count\": 1}}
```

**ALSO WRONG** (missing `input_jsons/` prefix):
```json
{\"ligand\": {\"ligand\": \"ergothioneine/substrates/L_His.sdf\", \"count\": 1}}
```

**CORRECT** (use full relative path from project root):
```json
{\"ligand\": {\"ligand\": \"input_jsons/ergothioneine/substrates/L_His.sdf\", \"count\": 1}}
```

**Key rule**: DISCO resolves paths relative to the working directory (project root), NOT relative to the JSON file location. Always use the full path from project root: `input_jsons/ergothioneine/substrates/L_His.sdf`

**Error signature**: If you see `OSError: File error: Bad input file /home/qiao/qiao_design/DISCO/ergothioneine/substrates/L_His.sdf`, it means the path format is wrong. Check that you're using the full relative path from project root.

### Example: Step 2 (HisM, rate-limiting)

```json
[
  {
    "sequences": [
      {
        "proteinChain": {
          "sequence": "-----",
          "count": 1
        }
      },
      {
        "ligand": {
          "ligand": "input_jsons/ergothioneine/substrates/1_MeHis.sdf",
          "count": 1
        }
      },
      {
        "ligand": {
          "ligand": "input_jsons/ergothioneine/cofactors/SAM.sdf",
          "count": 1
        }
      }
    ],
    "name": "length_200_HisM_1MeHis_SAM_methyltransferase"
  }
]
```

### Example: Step 3 (CuAO, rate-limiting, metal ion)

```json
[
  {
    "sequences": [
      {
        "proteinChain": {
          "sequence": "-----",
          "count": 1
        }
      },
      {
        "ligand": {
          "ligand": "input_jsons/ergothioneine/substrates/1_MeHis.sdf",
          "count": 1
        }
      },
      {
        "ligand": {
          "ligand": "input_jsons/ergothioneine/cofactors/O2.sdf",
          "count": 1
        }
      }
    ],
    "name": "length_200_CuAO_1MeHis_O2_oxidase"
  }
]
```

**Key rules**:
- Use relative paths from project root: `input_jsons/path/file.sdf`
- Do NOT use `FILE_` prefix (causes path resolution errors)
- Protein length encoded as dash string (e.g., `-----` = 200 aa)
- `count: 1` to avoid GPU OOM (serial design later)
- Name encodes enzyme, substrates, cofactors for traceability

## 4) Fetch PubChem 3D SDF Files

Create `scripts/download_<pathway>_sdfs.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/qiao/qiao_design/DISCO
mkdir -p input_jsons/ergothioneine/{substrates,cofactors,products}

echo "Downloading substrate SDF files..."
curl -s -o input_jsons/ergothioneine/substrates/L_His.sdf \
  'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/6274/SDF?record_type=3d'

curl -s -o input_jsons/ergothioneine/substrates/1_MeHis.sdf \
  'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/439235/SDF?record_type=3d'

# ... more downloads ...

echo "Creating placeholder files for intermediates..."
cat > input_jsons/ergothioneine/substrates/His_tRNA.sdf << 'EOF'
His-tRNA intermediate
  Placeholder for His-tRNA (requires synthesis or extraction)
  
  0  0  0  0  0  0  0  0  0  0999 V2000
M  END
> <PUBCHEM_COMPOUND_CID>
(placeholder)

$$$$
EOF

echo "✓ Download complete!"
```

**PubChem CID reference** (ergothioneine example):
- L-His: 6274
- 1-MeHis: 439235
- L-Cys: 5862
- SAM: 34755
- O₂: 977
- ATP: 5957
- PRPP: 15992
- EGT: 5281718

## 5) Create Serial Design Runner Script

Create `scripts/run_<pathway>_serial_design.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/qiao/qiao_design/DISCO

export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_PROGRESS_BARS=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_HOME=/usr/local/cuda-12.1

source .venv/bin/activate

OUT_BASE="${1:-./_egt_designs}"
SEEDS="${2:-0 1 2 3 4}"
EFFORT="${3:-max}"

mkdir -p "$OUT_BASE/logs"

echo "[$(date '+%F %T')] ========== Step 2: HisM (HIGH PRIORITY - Rate-limiting) =========="
for seed in $SEEDS; do
  echo "[$(date '+%F %T')] Starting HisM seed=$seed"
  CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
    use_deepspeed_evo_attention=false \
    experiment=diverse \
    effort=$EFFORT \
    input_json_path=input_jsons/step2_HisM.json \
    seeds="[$seed]" \
    dump_dir="$OUT_BASE/step2_HisM" \
    > "$OUT_BASE/logs/step2_HisM_seed${seed}.log" 2>&1 || {
      echo "[$(date '+%F %T')] ⚠ HisM seed=$seed failed"
      continue
    }
  echo "[$(date '+%F %T')] ✓ HisM seed=$seed completed"
  sync
  sleep 2
done

# ... repeat for steps 3, 4, 5 (rate-limiting) ...
# ... then steps 1, 6, 7 (lower priority) ...

echo "[$(date '+%F %T')] ✓ All enzyme designs completed!"
```

**Key features**:
- One seed per Python invocation (avoids OOM)
- Accumulates outputs in single `dump_dir` (sample_0, sample_1, ...)
- Logs each seed separately
- Prioritizes rate-limiting steps first

## 6) Create Multi-Document Guidance

### 6.1 Quick Reference Card (`ergothioneine_quickref.md`)
- 5-minute quick start
- Pathway diagram
- Key enzyme table
- PubChem CID lookup
- Aqueous conditions
- Environment variables
- Single enzyme example
- Troubleshooting

### 6.2 Complete Project Document (`ergothioneine_synthesis_pathway.md`)
- Full pathway overview
- 7-step reaction table with flux rates
- Cofactor & metal ion matrix
- Aqueous condition specs
- DISCO JSON examples for each step
- SDF download instructions
- Serial design script walkthrough
- Output analysis
- Post-design verification steps

### 6.3 Detailed Index (`ergothioneine_index.md`)
- Navigation table
- JSON config details (one per enzyme)
- SDF file inventory (substrates, cofactors, products)
- PubChem CID reference
- Download script explanation
- File structure overview
- Quick parameter reference

### 6.4 Delivery Checklist (`README_ERGOTHIONEINE.md`)
- Project summary
- File inventory (docs, JSONs, scripts)
- Key features
- Quick start (3 steps)
- File locations
- Pathway diagram
- Aqueous conditions
- Cofactor requirements
- Documentation navigation
- Next steps

## 7) Workflow Summary

1. **Input**: Biochemical reaction table (steps, enzymes, substrates, products, cofactors, flux, rate-limiting flags)
2. **Extract**: Cofactor matrix + aqueous conditions per enzyme
3. **Generate**: 7 JSON configs (one per enzyme, `count: 1` for serial design)
4. **Download**: PubChem 3D SDF files + create placeholders for intermediates
5. **Automate**: Serial design runner script (seed-by-seed, accumulate outputs)
6. **Document**: 4 guidance documents (quick ref, full guide, index, checklist)
7. **Run**: `bash scripts/download_<pathway>_sdfs.sh && bash scripts/run_<pathway>_serial_design.sh`
8. **Verify**: Check `_<pathway>_designs/` for PDB/sequence outputs

## 8) Rate-Limiting Step Prioritization

Identify bottlenecks from the reaction table:

```
Flux rate (relative):
  Step 1: 8.5 (not rate-limiting)
  Step 2: 7.9 ⭐ RATE-LIMITING
  Step 3: 7.3 ⭐ RATE-LIMITING
  Step 4: 5.8 ⭐ RATE-LIMITING
  Step 5: 5.2 ⭐ RATE-LIMITING
  Step 6: 3.1 (rate-limiting but lower priority)
  Step 7: 2.5 (rate-limiting but lower priority)
```

**Design priority order**:
1. Steps 2, 3, 4, 5 (highest flux impact)
2. Steps 6, 7 (medium priority)
3. Step 1 (lowest priority, not rate-limiting)

Run high-priority steps first to maximize pathway throughput.

## 9) Troubleshooting

### A) "Bad input file" error on SDF files

**Problem**: 
```
OSError: File error: Bad input file /home/qiao/qiao_design/DISCO/ergothioneine/substrates/L_His.sdf
```

**Root causes**:
1. **Wrong path format**: Using `FILE_ergothioneine/...` instead of `input_jsons/ergothioneine/...`
2. **Invalid SDF structure**: Placeholder files with minimal structure fail RDKit parsing
3. **File doesn't exist**: Path typo or file not downloaded

**Solutions**:
- Use relative paths from project root: `input_jsons/ergothioneine/substrates/L_His.sdf`
- Only use real PubChem 3D SDF files (download with `record_type=3d`)
- Verify file exists: `ls -lh input_jsons/ergothioneine/substrates/L_His.sdf`
- Check JSON syntax: `python -m json.tool input_jsons/step1.json`

### B) Placeholder SDF files don't work

**Problem**: Created minimal SDF files for intermediates (His-tRNA, 1-MeHis-SO, EGT-precursor), but DISCO rejects them with \"Bad input file\" error.

**Why**: RDKit's `SDMolSupplier(sanitize=False)` still requires valid SDF format with proper atom/bond definitions. Minimal placeholders (even with M  END markers) lack this structure and fail parsing.

**Solution**: 
- **Use only real PubChem molecules** (download with `record_type=3d`)
- **Skip intermediate products** if unavailable (simplify pathway to use only available molecules)
- **Generate 3D structures computationally** if needed (RDKit, OpenBabel, MOPAC, GAMESS)
- **For tRNA/protein intermediates**: Use simplified representations or extract from PDB/literature databases

**Practical approach**: Start with available PubChem molecules, then add intermediates only if you can generate valid 3D SDF structures.

### C) Missing intermediate SDF files
**Problem**: 1-MeHis-SO, EGT-precursor not in PubChem.
**Solution**: Create placeholders with minimal SDF structure, then:
- Synthesize computationally (RDKit, OpenBabel)
- Extract from literature databases
- Use computational chemistry tools (MOPAC, GAMESS)

### B) Metal ion representation in SDF
**Problem**: Cu²⁺, Mg²⁺ not standard organic molecules.
**Solution**: 
- Create minimal SDF with metal atom + dummy ligands
- Or use PubChem metal complex CIDs (e.g., Cu(II) complexes)
- Or represent as ligand-metal complex

### C) Aqueous condition mismatch
**Problem**: Enzyme requires aerobic conditions but DISCO doesn't model O₂ explicitly.
**Solution**: Include O₂ as explicit ligand (CID 977) in JSON config.

### E) Serial Design Execution (Avoiding OOM)

**Problem**: Running all seeds in parallel causes GPU OOM.

**Solution**: Use serial design runner that launches one seed at a time:

```bash
for seed in 0 1 2 3 4; do
  CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
    use_deepspeed_evo_attention=false \
    experiment=diverse \
    effort=max \
    input_json_path=input_jsons/step2_HisM.json \
    seeds="[$seed]" \
    dump_dir=./_egt_designs/step2_HisM \
    > logs/step2_HisM_seed${seed}.log 2>&1
  sleep 2  # Allow GPU memory to clear
done
```

**Key**: Each seed runs in a separate Python process, so GPU memory is released after each completes. Outputs accumulate in the same `dump_dir` (sample_0, sample_1, ...).

### F) Iterative Debugging Workflow

When encountering errors:

1. **Check the error message carefully** - it tells you exactly what failed
2. **Verify file paths** - use `ls -lh` to confirm files exist
3. **Validate JSON syntax** - use `python -m json.tool input_jsons/step1.json`
4. **Test with a single seed first** - before running all seeds
5. **Check logs** - each seed has its own log file in `logs/` directory
6. **Simplify the config** - remove problematic ligands, test with fewer molecules
7. **Restart from scratch** - if stuck, clean output directory and re-run

**Example debugging session**:
```bash
# 1. Validate JSON
python -m json.tool input_jsons/step2_HisM.json

# 2. Check files exist
ls -lh input_jsons/ergothioneine/substrates/1_MeHis.sdf
ls -lh input_jsons/ergothioneine/cofactors/SAM.sdf

# 3. Test single seed
CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
  use_deepspeed_evo_attention=false \
  experiment=diverse \
  effort=max \
  input_json_path=input_jsons/step2_HisM.json \
  seeds='[0]' \
  dump_dir=./_egt_designs/step2_HisM_test

# 4. Check output
ls -lh _egt_designs/step2_HisM_test/pdbs/
```

## 10) Output Analysis

After running all seeds:

```bash
# Count designs per enzyme
for step in step2_HisM step3_CuAO step4_MPST step5_Cyclase; do
  count=$(find _egt_designs/$step/pdbs -name "*.pdb" 2>/dev/null | wc -l)
  echo "$step: $count designs"
done

# Check ligand binding info
cat _egt_designs/step2_HisM/*_ligands.txt

# Inspect sequence
head -c 100 _egt_designs/step2_HisM/sequences/length_200_HisM_His_tRNA_SAM_methyltransferase_sample_0.txt
```

## 11) Post-Design Verification

1. **Structure prediction**: AlphaFold2 / OmegaFold on designed sequences
2. **Molecular docking**: DiffDock for enzyme-substrate binding
3. **Dynamics simulation**: OpenMM for complex stability
4. **Experimental validation**: Express, purify, measure kinetics (Km, kcat)

## Example: Ergothioneine Synthesis

Complete working example at `/home/qiao/qiao_design/DISCO/input_jsons/`:
- 7 JSON configs (step1_HisRS.json through step7_Proteasome.json)
- 4 guidance documents (README_ERGOTHIONEINE.md, ergothioneine_synthesis_pathway.md, ergothioneine_index.md, ergothioneine_quickref.md)
- 2 automation scripts (scripts/download_egt_sdfs.sh, scripts/run_egt_serial_design.sh)
- SDF directory structure (ergothioneine/substrates/, cofactors/, products/)

Quick start:
```bash
cd /home/qiao/qiao_design/DISCO
bash scripts/download_egt_sdfs.sh
bash scripts/run_egt_serial_design.sh
```

## References

- DISCO: Protein design framework
- PubChem: 3D structure database
- AlphaFold2: Structure prediction
- DiffDock: Molecular docking
- OpenMM: Molecular dynamics
