# Chinese-Teaching-AI-Agent
本项目面向中小学语文教师，打造大模型驱动的智能备课助手，覆盖小初高全学段统编语文教材，搭建课文解读、教案生成、课堂互动模拟、分层作业设计、读写专项指导五大核心功能。项目定制系统化结构化 Prompt 模板，依托角色定义、输出格式限制、分步生成策略规范大模型返回内容，支持内容流式输出，结果可一键导出 Markdown、Word 两种文档格式。前端采用 Streamlit 搭建可视化交互页面，自定义页面主题，提供学段、年级、篇目、授课风格、学生学情多维度自定义配置，贴合新课标语文核心素养培养标准。
# 📚 语文AI教学智能体

> 统编教材 · 新课标 · MiMo大模型驱动
> 中小学语文教师智能备课助手

基于 **Streamlit + MiMo 大模型**，覆盖小学、初中、高中全学段统编语文教材，提供课文解读、教案生成、课堂互动、分层作业、读写指导五大核心功能。

---

## ✨ 功能一览

| 功能 | 说明 |
|------|------|
| 📖 **课文深度解读** | 梳理知识点、重难点、教学切入点，深度剖析课文 |
| 📝 **自动生成教案** | 生成标准语文教案，含教学目标、课堂流程、提问设计、板书 |
| 💬 **课堂互动模拟** | 生成课堂话术、提问设计、学生回答预设与点评 |
| 📋 **分层作业设计** | 基础/提高/拓展三层作业，含阅读练习 |
| ✍️ **读写指导** | 阅读练习生成、作文审题指导、写作提纲 |

## 🎓 覆盖学段

- **小学**：一年级上册 ~ 六年级下册（共12册）
- **初中**：七年级上册 ~ 九年级下册（共6册）
- **高中**：高一必修 ~ 高三选择性必修（共6册）

## 🛠️ 技术栈

- **前端**：[Streamlit](https://streamlit.io/)
- **大模型**：[MiMo](https://mimo.xiaomi.com/)（基于 Anthropic SDK）
- **文档导出**：python-docx（Word）、Markdown

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/shiguangzhe666/语文AI教学智能体.git
cd 语文AI教学智能体
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

> 需要 Python 3.8+

### 3. 配置 API

首次启动后，在应用侧边栏填写 API 配置信息即可使用。

### 4. 启动应用

```bash
streamlit run app.py
```

或直接双击 `start.bat`（Windows）。

启动后访问：**http://localhost:8501**

---

## 📁 项目结构

```
语文AI教学智能体/
├── app.py              # 主应用（Streamlit 界面）
├── config.py           # 配置文件
├── mimo_client.py      # MiMo 大模型客户端
├── prompts.py          # 提示词模板
├── export.py           # 教案导出（Markdown / Word）
├── requirements.txt    # Python 依赖
├── start.bat           # Windows 一键启动脚本
└── data/
    └── textbooks.py    # 统编教材课文数据
```

---

## 📖 使用说明

1. **侧边栏配置**：选择学段、年级、课文、教学风格
2. **选择功能**：点击顶部 Tab 切换不同功能模块
3. **生成内容**：点击按钮，AI 实时流式输出结果
4. **导出教案**：支持导出为 Markdown 或 Word 文档

---

## ⚙️ 教学风格

支持多种教学风格，适配不同课堂需求：

- 严谨学术型
- 活泼互动型
- 启发探究型
- 传统讲授型

---

## 📄 License

MIT License

---

## 🙏 致谢

- [Streamlit](https://streamlit.io/) — 快速构建数据应用
- [MiMo](https://mimo.xiaomi.com/) — 小米大模型
- [Anthropic SDK](https://docs.anthropic.com/) — API 调用
