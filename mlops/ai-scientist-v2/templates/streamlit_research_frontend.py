"""
Streamlit Research Frontend Template
=====================================
Reusable template for wrapping CLI research pipelines with a no-code web UI.
Adapt the CONSTANTS, MODELS, and page logic to your project.

Usage:  streamlit run web_app.py
        bash run_web.sh
"""

import streamlit as st
import os
import sys
import json
import subprocess
import shutil
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional

st.set_page_config(page_title="Research Pipeline", page_icon="🔬", layout="wide")

PROJECT_ROOT = Path(__file__).parent
ITEMS_DIR = PROJECT_ROOT / "items"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
ENV_PATH = PROJECT_ROOT / ".env"

MODELS = ["mimo-v2.5-pro", "gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20241022"]


def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env


def save_env(env):
    lines = []
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            ls = line.strip()
            if ls and not ls.startswith("#") and "=" in ls:
                key = ls.split("=", 1)[0].strip()
                if key in env:
                    lines.append(f"{key}={env[key]}")
                    del env[key]
                else:
                    lines.append(line)
            else:
                lines.append(line)
    for k, v in env.items():
        lines.append(f"{k}={v}")
    ENV_PATH.write_text("\n".join(lines) + "\n")


def run_command_stream(cmd, cwd=None):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=cwd or str(PROJECT_ROOT),
        env={**os.environ},
    )
    for line in iter(proc.stdout.readline, ""):
        yield line
    proc.wait()
    yield f"\n[EXIT CODE: {proc.returncode}]\n"


st.sidebar.title("🔬 Research Pipeline")
page = st.sidebar.radio("导航", ["🏠 首页", "🚀 运行", "📊 结果", "⚙️ 设置"])

if page == "🏠 首页":
    st.title("🔬 研究流水线")
    env = load_env()
    st.metric("API 状态", "✅" if env.get("API_KEY") else "❌ 未配置")

elif page == "🚀 运行":
    st.title("🚀 运行实验")
    with st.form("run"):
        model = st.selectbox("模型", MODELS)
        if st.form_submit_button("🚀 开始", type="primary"):
            cmd = [sys.executable, "pipeline.py", "--model", model]
            log_area = st.empty()
            log_text = ""
            for line in run_command_stream(cmd):
                log_text += line
                log_area.code(log_text[-5000:], language="text")
            if "[EXIT CODE: 0]" in log_text:
                st.success("完成！")
                st.balloons()

elif page == "⚙️ 设置":
    st.title("⚙️ 设置")
    env = load_env()
    with st.form("keys"):
        api_key = st.text_input("API Key", value=env.get("API_KEY", ""), type="password")
        if st.form_submit_button("💾 保存"):
            env["API_KEY"] = api_key
            save_env(env)
            st.success("已保存！")
