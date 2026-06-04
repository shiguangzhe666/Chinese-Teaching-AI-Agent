@echo off
chcp 65001 >nul
echo ============================================
echo   语文AI教学智能体 - 启动脚本
echo   基于MiMo大模型 · 统编教材 · 新课标
echo ============================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip install -r requirements.txt -q

echo.
echo [2/3] 依赖安装完成
echo.
echo [3/3] 启动应用...
echo.
echo 应用地址: http://localhost:8501
echo 按 Ctrl+C 停止服务
echo.

streamlit run app.py --server.port 8501 --server.headless true

pause
