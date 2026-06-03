# Archived skill: hyperframes-workflow

Original path: `multimedia/hyperframes-workflow`

---

---
name: hyperframes-workflow
description: Professional workflow for HTML-to-video production using the HyperFrames framework.
tags: [video, html, gsap, ffmpeg, automation]
---

# HyperFrames Workflow

Guidelines for creating and rendering HTML-based video compositions using the `hyperframes` CLI tool.

## Trigger Conditions
- User asks to create, preview, or render a video using `hyperframes`.
- User wants to automate video production from HTML/CSS/GSAP.
- Troubleshooting render failures (FFmpeg errors, path issues).

## Core Commands
- `hyperframes init <project_name>`: Create a new project scaffold.
- `hyperframes preview`: Launch the live-sync browser studio for development.
- `hyperframes lint`: Validate compositions (ALWAYS run before rendering).
- `hyperframes render --output <output.mp4>`: Render the composition to video.

## Custom Timeline Registration (Non-GSAP)
If not using the standard GSAP `gsap.timeline()` object, any custom object registered to `window.__timelines["comp-id"]` must implement the following method interface:
- `duration()`: Function returning the total length in seconds.
- `pause()`: Function (can be a dummy) that returns `this`.
- `seek(time)`: Function that handles time updates and returns `this`.

Example:
```javascript
window.__timelines = window.__timelines || {};
window.__timelines["main"] = {
  _duration: 30,
  duration: function() { return this._duration; },
  pause: function() { return this; },
  seek: function(time) { 
    // update logic here 
    return this; 
  }
};
```

## Recommended Workflow: Audio-First (High Precision)

To prevent "timing drift" where visuals finish before audio (or vice-versa), follow the "Audio-First" methodology:

1.  **Draft Voiceover**: Create `voiceover.txt` with clear, spoken-rhythm text.
2.  **Generate Audio & Transcript**: Use TTS to generate `audio.mp3` and a tool (like Whisper) to generate `transcript.json` with word-level or sentence-level timestamps (`start`, `end`).
3.  **Define Visual Identity**: Create a `DESIGN.md` specifying color palettes, fonts, and motion signatures (e.g., `expo.out`). This ensures AI-assisted coding (Claude/Hermes) maintains consistency.
4.  **Map Scenes to Timestamps**: Derive `data-start` and `data-duration` for each scene directly from the `transcript.json`. **Never hardcode arbitrary durations.**
5.  **Implement in HyperFrames**: Use the derived timestamps in `index.html` and bind the `<audio>` element to the timeline.

## Critical Pitfalls & Fixes

### 1. Path Encoding (Non-ASCII Characters)
- **Problem**: The rendering engine (Headless Chrome) often fails when the project or output path contains non-ASCII characters (e.g., Chinese characters).
- **Fix**: Move the project to a pure ASCII/English path before rendering (e.g., `/tmp/` or a dedicated temp directory).

### 2. FFmpeg License Issues (libx264)
- **Problem**: Conda/Anaconda builds of FFmpeg often exclude GPL-licensed encoders like `libx264`, causing `Encoding failed: FFmpeg exited with code 8`.
- **Fix**: Force the use of the system-level FFmpeg (usually at `/usr/bin/ffmpeg`) which typically has full codec support.
- **Command**: `export PATH=/usr/bin:$PATH && hyperframes render ...`

### 3. Timeline Registration (The \"duration()\" Pitfall)
- **Problem**: Runtime error `e.getTimeline(...)?.duration is not a function`.
- **Fix**: The runtime expects a GSAP-compatible interface where `duration()` is a method, not a property.
- **Correct Pattern**:
  ```javascript
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = {
    _duration: 30,
    duration: function() { return this._duration; },
    pause: function() { return this; },
    seek: function(time) { 
      /* update DOM */
      return this; 
    }
  };
  ```

### 4. Visibility vs Display (The Black Screen Trap)
- **Problem**: Elements appearing as black or invisible in the final render.
- **Cause**: Setting `visibility: hidden` or `opacity: 0` on the `.clip` container in CSS, but only animating the *children* with GSAP. The container remains invisible.
- **Fix**: Either don't set hiding styles in CSS (let the framework handle it via `data-start`) or ensure GSAP explicitly animates the container's opacity/visibility (e.g., `tl.to("#id", { opacity: 1 })`).

### 5. Visual Verification (Agent Workflow)
- **Problem**: As a CLI agent, you cannot "see" the video output to confirm success.
- **Approach**: Extract a specific frame using FFmpeg and analyze it with vision tools.
- **Command**: `ffmpeg -ss 00:00:05 -i output.mp4 -frames:v 1 debug.png`
- **Follow-up**: Use `vision_analyze` on `debug.png` to confirm text visibility and color accuracy.

### 6. Root Element Requirements
- **Problem**: Linter errors (`root_missing_composition_id`) despite attributes being present.
- **Fix**: The composition root should be the first direct child of `<body>` or have a clear class like `.composition-root`. Ensure no nested wrappers intercept the ID check.


### 6. Track Management
- **Problem**: Clips overlapping or visibility not toggling correctly.
- **Fix**: Always include `data-track-index="0"` (or other numeric index) on every `class="clip"` element. The rendering engine uses track indices to manage the Z-index and visibility buffer.

### 7. Workflow Fallback: Manual Timing
If TTS tools (like `hermes tts` or `kokoro`) are unavailable:
1. **Mock Transcript**: Create a manual `transcript.json` or a table of scene durations.
2. **Visual-First Implementation**: Build the GSAP timeline using estimated durations.
3. **Audio Injection**: Once audio is available, update the `data-start` and `data-duration` attributes. Since the timeline is programmable, the visuals will automatically re-align.

### 8. Output Path Interpretation
- **Problem**: Passing a filename directly to `-o` can sometimes be misinterpreted as a directory by the tool.
- **Fix**: Use the full flag `--output` and ensure the target directory (e.g., `renders/`) exists.

### 8. TTS (Text-to-Speech) Dependencies
- **Problem**: `hyperframes tts` fails if `kokoro-onnx` and `soundfile` are not installed.
- **Fix**: Install required Python packages.
- **Command**: `pip install kokoro-onnx soundfile`
### 4. TTS (Text-to-Speech) Dependencies
- **Problem**: `hyperframes tts` fails if `kokoro-onnx` and `soundfile` are not installed.
- **Fix**: Install required Python packages.
- **Command**: `pip install kokoro-onnx soundfile`

### 5. JS Timeline Bridge (Advanced)
- **Problem**: Runtime error `e.getTimeline(...)?.duration is not a function` or `e.pause is not a function`.
- **Cause**: The rendering engine expects a GSAP-compatible interface (with methods, not just properties).
- **Fix**: Define the timeline with method functions.
- **Code**:
  ```javascript
  window.__timelines["main"] = {
    _duration: 60,
    duration: function() { return this._duration; },
    pause: function() { return this; },
    seek: function(t) {
      // Your logic here
      return this;
    }
  };
  ```

### 6. Frame Stability
- **Problem**: Elements flickering or missing during parallel capture.
- **Fix**: Use `visibility: hidden` and `opacity: 0` instead of `display: none` for scene transitions. `display: none` can cause layout thrashing that interferes with frame-accurate capture.
- **Commercial Quality**: For production-grade videos, use `--quality high` and ensure fonts are loaded via Google Fonts or locally to avoid layout shifts.
- **GPU Acceleration**: If a compatible NVIDIA GPU is available, add `--gpu` to significantly speed up the encoding phase.
- **Fallback Format**: If MP4 encoding fails due to codec issues, attempt a WebM render (`--format webm`) as it often uses `libvpx` which has wider availability in limited FFmpeg builds.
- **Model Weights**: TTS models are downloaded automatically. If network issues occur, manually download Kokoro weights to `~/.cache/kokoro/` using `hf download` or `curl` from a mirror.
- **Visibility**: Every timed element must have `class=\"clip\"` to be managed by the runtime.
- **Animations**: Use GSAP for all timelines. Ensure timelines are paused and registered to `window.__timelines["comp-id"]`.
- **Parallelism**: Use `--workers auto` for faster renders, but monitor RAM (approx. 256MB per worker).
- **Cleanup**: If rendering fails, check `hyperframes doctor` to verify environment dependencies.
