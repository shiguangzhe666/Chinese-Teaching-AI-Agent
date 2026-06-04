"""
语文AI教学智能体 - 配置文件
MiMo大模型 API 配置（Anthropic格式）
"""
import os

# MiMo API 配置（Anthropic格式）
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/anthropic")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2-pro")

# 生成参数
MAX_TOKENS = 4096
TEMPERATURE = 0.7
TOP_P = 0.9

# 应用配置
APP_TITLE = "语文AI教学智能体"
APP_ICON = "📚"
