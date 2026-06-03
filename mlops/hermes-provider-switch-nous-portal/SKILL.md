---
name: hermes-provider-switch-nous-portal
title: Hermes Agent — Nous Portal 提供商切换技术指南
description: 详解 Hermes Agent 中聚合器（OpenRouter）与直接提供商（Nous Portal）的架构差异，以及如何正确完成 OAuth 设备码流程切换到 Nous。适用于 Step 3.5 Flash 限时试用的配置场景。
summary: 诊断 Hermes Agent 提供商配置，识别聚合器与直接提供商的区别，并正确切换到 Nous Portal 以使用 Step 3.5 Flash 模型
version: 1.0.0
---

## 适用场景

当需要将 Hermes Agent 的推理服务从 OpenRouter 切换到 Nous Portal（启用 Step 3.5 Flash 限时免费体验）时使用。

## 核心发现：两类提供商的本质区别

Hermes Agent 的提供商分为两种认证模型：

### 聚合器（Aggregator）
- 示例：`openrouter`, `openrouter-cn`
- 认证：单一 API Key（`OPENROUTER_API_KEY` 环境变量）
- 配置：修改 `model.provider` 即可生效
- 特点：`is_aggregator=True`，背后路由到多家模型服务

### 直接提供商（Direct Provider）
- 示例：`nous` (Nous Portal), `anthropic`, `gemini`
- 认证：OAuth 设备码流程（`oauth_device_code`）或各家 API Key
- 配置：**必须**运行 `hermes model` 交互式命令完成首次授权
- 特点：token 存储在凭据管理器（`~/.hermes/credentials.json` 或系统密钥环）

**Nous Portal 的注册信息**（`hermes_cli/auth.py`）：
```python
ProviderConfig(
    id='nous',
    name='Nous Portal',
    auth_type='oauth_device_code',
    inference_base_url='https://inference-api.nousresearch.com/v1',
    portal_base_url='https://portal.nousresearch.com',
    client_id='hermes-cli',
    scope='inference:mint_agent_key'
)
```

## 调试流程

### 步骤 1：确认当前状态

运行

    hermes --version

确认版本号 ≥ 0.10.0。

查询当前配置对象（通过任意 Hermes 命令或 Python REPL）：

```python
from hermes_cli.config import load_config
cfg = load_config()
print(f"provider={cfg['model']['provider']}, default={cfg['model']['default']}")
```

### 步骤 2：检查 Nous Portal 是否已注册

```python
from hermes_cli.auth import PROVIDER_REGISTRY
from hermes_cli.providers import HERMES_OVERLAYS

nous_cfg = PROVIDER_REGISTRY.get('nous')
print(f"auth_type={nous_cfg.auth_type}, portal={nous_cfg.portal_base_url}")

overlay = HERMES_OVERLAYS.get('nous')
print(f"is_aggregator={overlay.is_aggregator}, transport={overlay.transport}")
```

预期 `auth_type` 为 `oauth_device_code`，`is_aggregator` 为 `False`。

### 步骤 3：验证 API 连通性（可选）

```python
import requests
from hermes_cli.auth import get_provider_credentials

# 获取Nous的凭据（如果已授权）
creds = get_provider_credentials('nous')
if creds:
    r = requests.get(
        'https://inference-api.nousresearch.com/v1/models',
        headers={'Authorization': f"Bearer {creds['api_key']}"},
        timeout=10
    )
    print(r.status_code)
```

若返回 200，说明网络正常且已有有效 token。

## 切换命令

### 正确方式（交互式）

在**交互终端**运行：

```bash
hermes model
```

流程：
1. 方向键选择 `nous` (Nous Portal)
2. 选择 `stepfun/step-3.5-flash`
3. 按提示在浏览器完成 OAuth 登录
4. 选择 **Save globally** 持久化到配置文件

### 无浏览器环境

```bash
hermes model --no-browser --provider nous
```

终端显示设备码和 URL，用户在另一设备浏览器中完成验证。

## 为何不能自动化

`hermes model` 内部会检测 `sys.stdin.isatty()`，若非 TTY（如管道、脚本）直接退出：

```python
# hermes_cli/commands.py 片段
if not sys.stdin.isatty():
    print("Error: 'hermes model' requires an interactive terminal.")
    return 1
```

且 OAuth 流程必须有人工在浏览器点击授权按钮，因此**无法脚本化**。

## 切换后的验证

```python
from hermes_cli.config import load_config
cfg = load_config()
assert cfg['model']['provider'] == 'nous', "切换未生效"
```

或在终端运行：

    hermes provider
    hermes chat "测试"

## 常见误区

- ❌ 直接修改 `config.yaml` 的 `provider: nous`（会因缺少 OAuth token 而失败）
- ❌ 仅添加 `custom_providers` 条目（该字段用于自定义 endpoint，不能替代 OAuth 流程）
- ❌ 使用 `echo | hermes model ...` 管道（会被非 TTY 检测拦截）

## 代码路径参考

- `hermes_cli/commands.py` — `/model` 命令入口
- `hermes_cli/model_switch.py` — `switch_model()` 核心分辨率逻辑
- `hermes_cli/auth.py` — `PROVIDER_REGISTRY`、`get_provider_credentials()`
- `hermes_cli/providers.py` — `HERMES_OVERLAYS`（提供商元数据与覆盖）
- `gateway/run.py` — `_handle_model_command()`（网关版本）