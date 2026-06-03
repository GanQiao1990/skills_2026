# Xiaomi MiMo TTS compatibility notes

Use this when a Xiaomi MiMo endpoint is advertised as OpenAI-compatible but the task needs speech generation rather than plain text chat.

## Verified compatibility pattern

For the token-plan mirror used in session:
- Base URL: `https://token-plan-cn.xiaomimimo.com/v1`
- Model listing works at: `GET /models`
- Text chat works at: `POST /chat/completions` with `model=mimo-v2.5-pro`
- TTS also works through: `POST /chat/completions` with `model=mimo-v2.5-tts`

## Important pitfall

Do **not** assume a standard OpenAI TTS route such as:
- `/v1/audio/speech`
- `/audio/speech`
- `/v1/tts`

In the validated session these returned `404 Not Found` on the mirror endpoint.

## Required request shape for MiMo TTS

MiMo TTS accepted a chat-completions payload of this form:

```json
{
  "model": "mimo-v2.5-tts",
  "messages": [
    {"role": "assistant", "content": "你好，这是语音测试。"}
  ],
  "modalities": ["text", "audio"],
  "audio": {
    "voice": "冰糖",
    "format": "mp3"
  }
}
```

## Two easy-to-miss quirks

### 1. `messages` must contain an assistant role
If you send only a user message, MiMo can reject the request with an error equivalent to:

- `messages must contain an assistant role for TTS model`

So for direct TTS generation, place the narration text in an `assistant` message.

### 2. Voice names are provider-specific
Do not use generic voices like `female` / `male` unless the endpoint explicitly documents them.

Validated voice error returned a list of acceptable voices:
- `mimo_default`
- `冰糖`
- `茉莉`
- `苏打`
- `白桦`
- `Mia`
- `Chloe`
- `Milo`
- `Dean`

## Response handling

Successful responses return base64 audio under the chat response message payload, e.g. `choices[0].message.audio.data`. Decode and write bytes to an `.mp3` file.

## Long-form audiobook pattern

For book-scale jobs, use a project directory with these artifacts:
- cleaned full text
- `parts/` directory with chunked MP3s
- final concatenated MP3
- `state.json` progress file
- `manifest.json`
- `run.log`

Recommended flow:
1. Normalize source text first.
2. Split narration into conservative chunks (session used roughly 900 Chinese chars max per TTS call).
3. Generate one MP3 part per chunk.
4. Concatenate with `ffmpeg -f concat -safe 0 -i concat.txt -c copy final.mp3`.
5. Persist progress after each chunk so the run can be inspected or resumed.

## Header note

The session succeeded with standard bearer auth; user-supplied docs for MiMo also show an `api-key` header. When integrating a reusable client, prefer supporting both if the proxy layer is undocumented or inconsistent.
