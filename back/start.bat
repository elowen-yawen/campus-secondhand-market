@echo off
REM ============================================================
REM 校园二手交易平台后端 - 启动脚本 (Windows)
REM 自动检测 Python 环境、创建虚拟环境、安装依赖并启动服务
REM ============================================================
setlocal enabledelayedexpansion

cd /d "%~dp0"

set VENV_DIR=.venv
set REQUIREMENTS=requirements.txt
set ENV_FILE=.env
set ENV_EXAMPLE=.env.example

REM ---------- 检测 Python ----------
set PYTHON_CMD=
for %%c in (python python3) do (
    where %%c >nul 2>nul
    if !errorlevel! equ 0 (
        for /f "tokens=2 delims= " %%v in ('%%c --version 2^>^&1') do (
            set PYTHON_VER=%%v
        )
        set MAJOR=!PYTHON_VER:~0,1!
        if !MAJOR! geq 3 (
            set PYTHON_CMD=%%c
            echo [INFO]  检测到 Python: %%c ^(!PYTHON_VER!^)
            goto :found_python
        )
    )
)
echo [ERROR] 未找到 Python 3，请先安装 Python 3.8+
exit /b 1

:found_python

REM ---------- 创建/激活虚拟环境 ----------
if not exist "%VENV_DIR%" (
    echo [INFO]  正在创建虚拟环境 ...
    %PYTHON_CMD% -m venv %VENV_DIR%
) else (
    echo [INFO]  虚拟环境已存在
)
call "%VENV_DIR%\Scripts\activate.bat"
echo [INFO]  已激活虚拟环境

REM ---------- 安装依赖 ----------
if not exist "%REQUIREMENTS%" (
    echo [ERROR] 缺少 %REQUIREMENTS% 文件
    exit /b 1
)
echo [INFO]  正在安装依赖 ...
pip install -r %REQUIREMENTS% -q
echo [INFO]  依赖安装完成

REM ---------- 生成 .env ----------
if not exist "%ENV_FILE%" (
    if exist "%ENV_EXAMPLE%" (
        copy "%ENV_EXAMPLE%" "%ENV_FILE%" >nul
        echo [INFO]  已从 %ENV_EXAMPLE% 生成 %ENV_FILE%，请按需修改
    ) else (
        echo [WARN]  未找到 %ENV_EXAMPLE%，跳过 .env 生成
    )
) else (
    echo [INFO]  %ENV_FILE% 已存在
)

REM ---------- 启动服务 ----------
echo [INFO]  正在启动服务 ...
python -m src.main

endlocal
