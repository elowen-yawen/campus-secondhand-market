#!/usr/bin/env bash
# ============================================================
# 校园二手交易平台后端 - 启动脚本 (Linux/macOS)
# 自动检测 Python 环境、创建虚拟环境、安装依赖并启动服务
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

# ---------- 辅助函数 ----------
log_info()  { echo "[INFO]  $*"; }
log_warn()  { echo "[WARN]  $*"; }
log_error() { echo "[ERROR] $*"; }

# ---------- 检测 Python ----------
detect_python() {
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver=$("$cmd" --version 2>&1 | awk '{print $2}')
            local major
            major=$(echo "$ver" | cut -d. -f1)
            if [ "$major" -ge 3 ]; then
                PYTHON_CMD="$cmd"
                log_info "检测到 Python: $cmd ($ver)"
                return 0
            fi
        fi
    done
    log_error "未找到 Python 3，请先安装 Python 3.8+"
    exit 1
}

# ---------- 创建/激活虚拟环境 ----------
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        log_info "正在创建虚拟环境 ..."
        "$PYTHON_CMD" -m venv "$VENV_DIR"
    else
        log_info "虚拟环境已存在"
    fi
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    log_info "已激活虚拟环境"
}

# ---------- 安装依赖 ----------
install_deps() {
    if [ ! -f "$REQUIREMENTS" ]; then
        log_error "缺少 $REQUIREMENTS 文件"
        exit 1
    fi
    log_info "正在安装依赖 ..."
    pip install -r "$REQUIREMENTS" -q
    log_info "依赖安装完成"
}

# ---------- 生成 .env ----------
setup_env() {
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_EXAMPLE" ]; then
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            log_info "已从 $ENV_EXAMPLE 生成 $ENV_FILE，请按需修改"
        else
            log_warn "未找到 $ENV_EXAMPLE，跳过 .env 生成"
        fi
    else
        log_info "$ENV_FILE 已存在"
    fi
}

# ---------- 启动服务 ----------
start_server() {
    log_info "正在启动服务 ..."
    python -m src.main
}

# ---------- 主流程 ----------
main() {
    log_info "===== 校园二手交易平台后端 - 启动脚本 ====="
    detect_python
    setup_venv
    install_deps
    setup_env
    start_server
}

main
