---
name: md-display
description: Use when turning molecular-dynamics results into publication figures or an animated trajectory, especially when a membrane-protein view must keep the lipid layer fixed while protein motion remains visible.
version: 1.0.0
author: Gan Qiao
license: MIT
metadata:
  hermes:
    tags: [molecular-dynamics, chimerax, trajectory, membrane, visualization]
    related_skills: [molecular-dynamics, chimerax-render]
---

# Molecular-dynamics figure recipe (verified on this project)

The conventional MD figure = **one snapshot + two conventional QC plots**.
Implemented in `final_submission/scripts/prep_figures.py::build_fig3_md`
(POPC 50 ns membrane MD, EMPA–NDUFB4). Do not reinvent the layout.

## Data expected

From an MD analysis directory, per-frame CSVs:

| File | Columns | Use |
|------|---------|-----|
| `protein_ca_rmsd.csv` | `time_ns,rmsd_A` | Panel: whole-protein Cα-RMSD |
| `region_rmsd.csv` | `time_ns,tm_rmsd_A,cyto_rmsd_A` | Split TM vs soluble region — a small protein's whole-chain RMSD is inflated by loop swing (here: whole ~20 Å, TM ~7.4 Å). Always show the TM/stable-region line or reviewers read the trajectory as "unstable" |
| `ligand_analysis.csv` | `time_ns,lig_rmsd_A,min_dist_A,arg72_dist_A` | Ligand RMSD + min protein–ligand distance, dual-axis |
| `protein_ca_rmsf.csv` | `resid,resname,rmsf_A` | Optional per-residue flexibility panel |
| `contact_occupancy.csv` | `residue,occupancy_pct,frames` | Optional pocket-contact bar chart |

Plus a full-system PDB for the snapshot (e.g. `bilayer_complex_popc.pdb`).

## Snapshot render (ChimeraX, headless)

Requires the `chimerax-render` env fix (`LD_LIBRARY_PATH` → bundled Qt6).
For a POPC bilayer box (this build had 124k atoms — renders fine, ~3 min):

```cxc
open bilayer_complex_popc.pdb
set bgColor white
lighting soft shadows true intensity 0.6
graphics silhouettes true
hide atoms
cartoon protein
color protein #4A7FB5 target c
select :POPC                      # lipid tails: thin, translucent
style sel stick
color sel #E0D5BC target a
transparency sel 55 target a
show sel
select :POPC@P31                  # headgroup P atoms: spheres mark leaflets
style sel sphere
color sel #C9B08A target a
transparency sel 30 target a
select :UNK                       # ligand resname varies — CHECK the file
delete :UNK & H
style sel sphere
color sel #C0392B target a
show sel
select clear                      # always clear before save (green outline otherwise)
turn x -90                        # put bilayer normal on screen-up (membrane slab edge-on)
view protein
zoom 1.35
windowsize 2560 1920
save out.png supersample 2        # supersample 2 is enough for 100k+ atom systems
```

**System-specific gotchas (check before scripting):**
- Ligand resname is unpredictable: `UNK` here; `LIG`/`UNL` elsewhere. Verify with
  `awk '{print substr($0,18,4)}' file.pdb | sort -u`.
- Receptor .pdbqt/.pdb files may contain an embedded docked ligand as `ATOM`
  records — strip `LIG|UNL|EMP` resnames when building clean complexes.
- Inspect residue and atom names before selecting lipid headgroups. A PDB
  writer may truncate `POPC` to `POP`; the phosphate atom may be named `P`,
  not `P31`. Whole-lipid sticks at full opacity are unreadable; use
  headgroup-only spheres to mark the slab.
- Big solvated systems: delete/hide `WAT`, `Na+`, `Cl-`; render only
  protein + lipids + ligand.
- `windowsize 2560 1920` minimum (≥2K) per project requirement.

## Animated trajectory with a fixed membrane view

Use this when the goal is to see protein changes against a stable lipid-layer
reference. The camera and the membrane coordinate frame must both stay fixed.

1. Inspect the trajectory before choosing a reader. A multi-`MODEL` PDB often
   opens as separate models (`#1.1`, `#1.2`, …), not as coordinate sets. Use
   `coordset` only if ChimeraX successfully loads it as one topology with
   coordinate sets. For separate models, `hide #1 models` / `show #1.1 models`
   reliably switches visible frames; `modeldisplay` is not a ChimeraX command.
2. Unwrap each frame around a stable protein anchor. Derive a membrane normal
   from lipid-phosphate positions and an in-plane axis by projecting a unit-cell
   vector into the membrane plane. Align this full membrane basis and its
   phosphate centroid to frame 1, applying the same rigid transform to every
   atom. **Do not Kabsch-fit the protein or align only the membrane normal**:
   protein fitting moves the membrane with the protein, while normal-only
   alignment can introduce a changing in-plane twist.
3. Set the ChimeraX camera once using frame 1, then switch models without
   another `view`, `turn`, or `zoom` command. Hide all models, show frame 1,
   orient and frame the scene, then save each frame while only changing model
   visibility. Draw the protein as cartoon, the ligand as ball-and-stick, and
   only lipid `P` atoms as translucent spheres.
4. Encode the rendered PNGs as a looping GIF with one palette shared across
   frames. Markdown can display it directly:

   ```markdown
   ![MD trajectory](relative/path/md_trajectory.gif)
   ```

5. Validate the final GIF after decoding/compositing: frame count, dimensions,
   frame delay, loop flag, and pixel differences across frames. A file can have
   many encoded frames and still be visually static. For Markdown-to-PDF
   exports, confirm that the target viewer supports animation; if it does not,
   provide the GIF as a sidecar or render an MP4 for video playback.

For this project, `assets/fig_src/md_gif/extract_frames.py` performs the
membrane-referenced coordinate transform, `movie3.cxc` renders each model with
a fixed camera, and `build_gif.py` creates the Markdown-ready GIF.

## Figure layout (matplotlib)

Conventional three-panel: snapshot left, two plots right.

```
A  membrane-embedded complex (snapshot)   |  B  protein Cα-RMSD vs time
   (imshow, axis off)                     |      whole / TM / cytosolic lines
                                          |  C  ligand RMSD + min distance
                                          |      dual y-axis
```

- `savefig(dpi=600)` for all three outputs (png/svg/pdf) — embedded rasters
  then land at ~600 dpi effective.
- Keep the caveat footer: MD poses/contacts are model predictions, not
  binding evidence.
- Rebuild a single figure without running the whole prep script via the
  `exec(header + function-body)` slice pattern used in
  `scripts/_rebuild_fig1.py`.

## Conventional plot choices

- RMSD: plot raw frame series (thin lines), label median in legend or text if
  needed. Whole-protein RMSD >15 Å on a small protein is usually loop motion —
  add the TM/region line rather than hiding it.
- Ligand: RMSD (left axis, one color) + min distance (right axis, second
  color). Occupancy % is a separate bar-chart panel if needed.
- RMSF: per-residue line; mark pocket residues with arrows only if asked.
