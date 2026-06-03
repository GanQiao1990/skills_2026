---
name: hyperframes-cli
description: HyperFrames CLI tool — hyperframes init, lint, preview, render, transcribe, tts, doctor, browser, info, upgrade, compositions, docs, benchmark. Use when scaffolding a project, linting or validating compositions, previewing in the studio, rendering to video, transcribing audio, generating TTS, or troubleshooting the HyperFrames environment.
---

# HyperFrames CLI

Everything runs through `npx hyperframes`. Requires Node.js >= 22 and FFmpeg.

## Workflow

1. **Scaffold** — `npx hyperframes init my-video`
2. **Write** — author HTML composition (see the `hyperframes` skill)
3. **Lint** — `npx hyperframes lint`
4. **Preview** — `npx hyperframes preview`
5. **Render** — `npx hyperframes render`

Lint before preview — catches missing `data-composition-id`, overlapping tracks, unregistered timelines.

## Scaffolding

```bash
npx hyperframes init my-video                        # interactive wizard
npx hyperframes init my-video --example warm-grain   # pick an example
npx hyperframes init my-video --video clip.mp4        # with video file
npx hyperframes init my-video --audio track.mp3       # with audio file
npx hyperframes init my-video --non-interactive       # skip prompts (CI/agents)
```

Templates: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`.

`init` creates the right file structure, copies media, transcribes audio with Whisper, and installs AI coding skills. Use it instead of creating files by hand.

## Linting

```bash
npx hyperframes lint                  # current directory
npx hyperframes lint ./my-project     # specific project
npx hyperframes lint --verbose        # info-level findings
npx hyperframes lint --json           # machine-readable
```

Lints `index.html` and all files in `compositions/`. Reports errors (must fix), warnings (should fix), and info (with `--verbose`).

## Previewing

```bash
npx hyperframes preview                   # serve current directory
npx hyperframes preview --port 4567       # custom port (default 3002)
```

Hot-reloads on file changes. Opens the studio in your browser automatically.

## Rendering

```bash
npx hyperframes render                                # standard MP4
npx hyperframes render --output final.mp4             # named output
npx hyperframes render --quality draft                # fast iteration
npx hyperframes render --fps 60 --quality high        # final delivery
npx hyperframes render --format webm                  # transparent WebM
npx hyperframes render --docker                       # byte-identical
```

| Flag           | Options               | Default                    | Notes                       |
| -------------- | --------------------- | -------------------------- | --------------------------- |
| `--output`     | path                  | renders/name_timestamp.mp4 | Output path                 |
| `--fps`        | 24, 30, 60            | 30                         | 60fps doubles render time   |
| `--quality`    | draft, standard, high | standard                   | draft for iterating         |
| `--format`     | mp4, webm             | mp4                        | WebM supports transparency  |
| `--workers`    | 1-8 or auto           | auto                       | Each spawns Chrome          |
| `--docker`     | flag                  | off                        | Reproducible output         |
| `--gpu`        | flag                  | off                        | GPU-accelerated encoding    |
| `--strict`     | flag                  | off                        | Fail on lint errors         |
| `--strict-all` | flag                  | off                        | Fail on errors AND warnings |

Worker pitfall: if you see parallel capture timeouts or repeated navigation timeouts, especially on screenshot-mode/headless fallback builds, retry immediately with `--workers 1`. High worker counts can be less stable than sequential capture even for compositions that are not obviously video-heavy.

**Quality guidance:** `draft` while iterating, `standard` for review, `high` for final delivery.

## Transcription

```bash
npx hyperframes transcribe audio.mp3
npx hyperframes transcribe video.mp4 --model medium.en --language en
npx hyperframes transcribe subtitles.srt   # import existing
npx hyperframes transcribe subtitles.vtt
npx hyperframes transcribe openai-response.json
```

## Text-to-Speech

```bash
npx hyperframes tts "Text here" --voice af_nova --output narration.wav
npx hyperframes tts script.txt --voice bf_emma
npx hyperframes tts --list  # show all voices
```

## Troubleshooting

```bash
npx hyperframes doctor       # check environment (Chrome, FFmpeg, Node, memory)
npx hyperframes browser      # manage bundled Chrome
npx hyperframes info         # version and environment details
npx hyperframes upgrade      # check for updates
```

Run `doctor` first if rendering fails. Common issues: missing FFmpeg, missing Chrome, low memory.

For stubborn render failures, use this order:
1. If parallel capture times out or navigation times out, retry with `--workers 1` before changing anything else.
2. If MP4 encoding fails with FFmpeg exit code 8, verify the FFmpeg actually used by the shell provides `libx264`. On mixed Conda/system machines, prefer the system FFmpeg for HyperFrames renders.
3. If CDN JS fetches are flaky during compile/render, vendor critical scripts locally in the project (for example `assets/gsap.min.js`) instead of relying on runtime download.
4. If you see a recurring non-blocking `404` with no explicit missing asset in the HTML, add `<link rel="icon" href="data:,">` so headless Chrome does not request a missing favicon.
5. If long sequential local capture dies mid-run with browser errors like `Protocol error (Page.captureScreenshot): Target closed`, retry with `--docker` for a more stable containerized browser.
6. When writing shell wrappers around FFmpeg checks, avoid `ffmpeg ... | grep -q ...` under `set -o pipefail`; `grep -q` can exit early, upstream FFmpeg gets SIGPIPE, and the script may falsely report failure. Capture the encoder list first, then test the string.

Encoding-specific pitfall: `doctor` verifies FFmpeg presence, not whether your active FFmpeg can encode H.264. If a render reaches encode and fails with `FFmpeg exited with code 8`, verify the actual binary on PATH and its encoders:

```bash
which ffmpeg
ffmpeg -encoders | grep libx264
```

If `libx264` is missing (common with some Conda FFmpeg builds), prepend a system FFmpeg that includes H.264 support before rendering, e.g. `export PATH=/usr/bin:/bin:$PATH && hash -r`.

Another pitfall: if `npx hyperframes` tries to fetch a newer package that requires a newer Node version than the current shell provides, it may never run the render at all. In that case, prefer a known installed `hyperframes` executable already compatible with the current environment, or run from a clean shell/deactivated env so `npx` resolves the intended toolchain.

If render reaches frame capture but fails at the final encode step with `FFmpeg exited with code 8`, verify encoder availability instead of only FFmpeg presence. A common cause is a Conda or custom `ffmpeg` earlier in `PATH` that lacks `libx264` even though `doctor` reports FFmpeg as installed.

```bash
which ffmpeg
ffmpeg -encoders | grep -E 'libx264|aac'
```

If `libx264` is missing, switch to a system FFmpeg that includes H.264 encoding and retry with fewer workers:

```bash
export PATH=/usr/bin:/bin:$PATH
hash -r
which ffmpeg
npx hyperframes render --workers 1 --output final.mp4
```

Why this matters: HyperFrames `doctor` validates FFmpeg presence, but an encode can still fail later if the selected binary cannot encode H.264 MP4s. Also, when HyperFrames warns that parallel capture timed out, prefer `--workers 1` before chasing unrelated HTML or animation issues.

## Other

```bash
npx hyperframes compositions   # list compositions in project
npx hyperframes docs           # open documentation
npx hyperframes benchmark .    # benchmark render performance
```
