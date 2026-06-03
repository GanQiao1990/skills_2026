# Metabolic pathway focused-mode optimization notes

Source pattern: local interactive HTML/SVG metabolic map with multiple tabs and one mode dedicated to nitrogen assimilation control.

## What improved the figure most

1. Replace generic title/subtitle with mode-specific copy.
   - Whole-map titles are fine for overview mode.
   - Focus mode needs a dedicated headline naming the mechanism directly.

2. Add a compact focus panel for presentation use.
   - Best structure for pathway regulation:
     - input layer
     - sensing layer
     - amplification / regulatory layer
     - output / assimilation sink

3. Promote only the key nodes and edges.
   - For nitrogen assimilation, the highlighted chain was:
     - AmtB
     - NH4+
     - GlnD
     - PII
     - NtrBC
     - Gln / Glu / aKG
   - Thicker strokes + brighter labels + limited pulse on bottleneck nodes worked better than global animation.

4. Mute unrelated badges/visual families instead of fully deleting them.
   - Keeps orientation without breaking context.

5. Disable contradictory controls in focused mode.
   - In the session, the degradation overlay button was disabled in the curated nitrogen-assimilation view to prevent stacking unrelated information.

6. Use a dedicated reset camera for the focus mode.
   - Whole-network framing made the curated subpathway look too small.
   - A custom reset centered on the local mechanism made the mode immediately usable.

7. Sync all visible copy across UI regions.
   - Header title
   - subtitle
   - bottom info bar
   - button label/state
   - overlay/panel copy

## Durable lesson

For interactive scientific figures, 'optimization' often really means converting an exploratory canvas into a guided explanatory scene. The missing ingredient is usually not more data, but mode-specific narrative framing.
