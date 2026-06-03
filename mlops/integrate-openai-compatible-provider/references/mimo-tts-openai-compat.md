# Xiaomi MiMo TTS via OpenAI-compatible chat endpoint

Use this note when a provider exposes a TTS-capable model in an OpenAI-compatible surface but does not actually implement OpenAI's dedicated `/audio/speech` endpoint.

## Durable findings from this session

User-supplied endpoints:
- OpenAI-compatible: `https://token-plan-cn.xiaomimimo.com/v1`
- Anthropic-compatible: `https://token-plan-cn.xiaomimimo.com/anthropic`

Verified model listing included:
- `mimo-v2.5-pro`
- `mimo-v2.5-tts`

Verified text-chat path:
- `POST /v1/chat/completions` with `model=mimo-v2.5-pro` worked normally

Verified TTS path:
- `POST /v1/chat/completions` with `model=mimo-v2.5-tts`
- request body must contain an `assistant` message whose content is the text to synthesize
- request body must include:
  - `modalities: ["text", "audio"]`
  - `audio: {"voice": "冰糖", "format": "mp3"}`
- returned audio is base64 at `choices[0].message.audio.data`

Non-working assumptions that should be avoided next time:
- `POST /v1/audio/speech` returned 404 here
- `voice: "female"` failed; provider returned the supported voice list instead
- omitting the `assistant` role failed with an explicit TTS-model validation error

## Known-good request shape

Python requests example:

```python
import base64
import requests

api_key = "..."
url = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
payload = {
    "model": "mimo-v2.5-tts",
    "messages": [
        {"role": "assistant", "content": "你好，这是语音测试。"}
    ],
    "modalities": ["text", "audio"],
    "audio": {"voice": "冰糖", "format": "mp3"}
}
headers = {
    "Authorization": f"Bearer {api_key}",
    "api-key": api_key,
    "Content-Type": "application/json",
}
resp = requests.post(url, headers=headers, json=payload, timeout=120)
resp.raise_for_status()
audio_b64 = resp.json()["choices"][0]["message"]["audio"]["data"]
mp3_bytes = base64.b64decode(audio_b64)
```

## Long-form audiobook pattern

For book-length input:
1. Read from the requested starting line.
2. Split by chapter headings if available.
3. Normalize Markdown locally first when possible; do not spend LLM calls cleaning the whole book unless the user explicitly wants stylistic rewriting.
4. Split narration into short TTS chunks.
5. Save each chunk as `parts/part_XXXX.mp3`.
6. Concatenate with ffmpeg.
7. Keep a project directory containing:
   - `run.log`
   - `state.json`
   - `manifest.json`
   - `README.md`
   - `chapters/`
   - `parts/`
   - final merged mp3

This is especially useful when the user asks to “write as a project” rather than just dropping a final output file in `./`.
