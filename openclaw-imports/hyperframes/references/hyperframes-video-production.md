# Archived skill: hyperframes-video-production

Original path: `multimedia/hyperframes-video-production`

---

---
name: hyperframes-video-production
description: Create and render high-quality HTML/CSS/JS video compositions using the HyperFrames CLI (v0.4.2+).
---

# HyperFrames Video Production

Create and render high-quality HTML/CSS/JS video compositions using the HyperFrames CLI (v0.4.2+).

## Workflow

1.  **Initialization**: Create a new project scaffold.
    ```bash
    hyperframes init <project-name>
    ```
2.  **Composition Development**: Edit `index.html`. 
    - Every timed element MUST have `class="clip"`.
    - Use `data-start`, `data-duration`, and `data-track-index` attributes.
    - For animations, use GSAP and register the timeline:
      ```javascript
      const tl = gsap.timeline({ paused: true });
      // ... animations ...
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      ```
3.  **Verification**: Always run the linter to check for timing overlaps or missing attributes.
    ```bash
    hyperframes lint
    ```
4.  **Preview**: Open the studio to fine-tune animations.
    ```bash
    hyperframes preview
    ```
5.  **Rendering**: Export to MP4 or WebM.
    ```bash
    hyperframes render -o output.mp4
    ```

## Pitfalls & Troubleshooting

- **Path Encoding**: **CRITICAL**. The rendering engine may fail if the project is located in a directory path containing non-ASCII characters (e.g., Chinese characters like `公众号`). 
    - *Fix*: Move the project to a simple path (e.g., `~/temp-video`) before rendering.
- **Audio/Video**: Videos should be `muted` if using a separate `<audio>` track for the composition.
- **Deterministic Logic**: Avoid `Math.random()` or `Date.now()` in animations as they break frame-consistency during rendering. Use the framework's time-seeding if available.
- **System Dependencies**: If rendering fails on a fresh system, run `hyperframes doctor` to check for missing Chrome or GPU dependencies.
