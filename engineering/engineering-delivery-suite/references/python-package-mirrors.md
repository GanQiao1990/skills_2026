# Python package mirrors for uv/pip

Durable notes from a robin session where default PyPI timed out and the fix was to switch to China-friendly mirrors.

## Project-local uv config

Use a project-local `uv.toml` when you want the change scoped to one repo.

Example:

```toml
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
extra-index-url = ["https://mirrors.aliyun.com/pypi/simple"]
index-strategy = "unsafe-best-match"
```

Important:
- In `uv.toml`, top-level `default-index` is invalid and will be rejected by uv's config parser.
- Use `index-url` and `extra-index-url` instead.

## User-level pip config

Path:
- `~/.config/pip/pip.conf`

Example:

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url =
    https://mirrors.aliyun.com/pypi/simple
trusted-host =
    pypi.tuna.tsinghua.edu.cn
    mirrors.aliyun.com
```

## User-level uv config

Path:
- `~/.config/uv/uv.toml`

Example:

```toml
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
extra-index-url = ["https://mirrors.aliyun.com/pypi/simple"]
index-strategy = "unsafe-best-match"
```

## Verification pattern

Prefer a dry-run install of a package that is not already installed in the target environment:

```bash
uv pip install --python .venv/bin/python --dry-run choix==0.3.6 -v
```

This confirms that:
- uv parsed the mirror config
- the mirror is reachable
- uv can resolve transitive dependencies
- wheel URLs are being selected from the configured mirror(s)

## Import-name mismatch pitfall

Do not assume the package installation name equals the Python import name.

Observed mappings:
- `fhaviary` -> import as `aviary`
- `fhlmi` -> import as `lmi`

Verification method:

```python
import importlib.metadata as md
print(md.distribution('fhaviary').read_text('top_level.txt'))
print(md.distribution('fhlmi').read_text('top_level.txt'))
```

This is the right follow-up when `uv pip install ...` succeeded but `import <distribution_name>` still fails.
