"""
语文AI教学智能体 - 主应用程序
基于Streamlit + MiMo大模型
专为语文教师备课设计
"""
import streamlit as st
from data.textbooks import GRADE_LEVELS, TEXTBOOKS, TEACHING_STYLES, get_grades, get_textbooks
from mimo_client import get_client, reset_client
from prompts import (
    get_system_prompt, get_analysis_prompt, get_lesson_plan_prompt,
    get_interaction_prompt, get_homework_prompt,
    get_reading_prompt, get_writing_prompt
)
from export import get_download_data
from config import MIMO_BASE_URL, MIMO_API_KEY, MIMO_MODEL


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="语文AI教学智能体",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    /* ========== 暖学术配色 ========== */
    :root {
        --bg:        #FFF8F0;
        --bg-card:   #FFFCF7;
        --bg-sidebar:#FFF5EB;
        --border:    #F0E6DA;
        --border-lt: #F5EDE3;
        --text:      #5C5349;
        --text-light:#8C8278;
        --text-dark: #4A423A;
        --brown:     #8B7355;
        --brown-lt:  #B09A7C;
        --orange:    #D4915E;
        --orange-lt: #F5E0CC;
        --orange-deep:#C67D45;
        --cream:     #FFF3E4;
    }

    /* ========== 全局 ========== */
    .stApp {
        background: var(--bg);
    }

    html, body, [class*="css"] {
        font-family: 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', system-ui, sans-serif;
        color: var(--text);
    }

    /* ========== 侧边栏 ========== */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar);
        border-right: 1px solid var(--border);
    }
    .css-1d391kg {
        background: var(--bg-sidebar);
    }

    /* 侧边栏标题文字 */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stCaption {
        color: var(--text) !important;
    }

    /* 侧边栏收起/展开按钮 */
    button[data-testid="stSidebarCollapseControl"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--brown) !important;
        opacity: 1 !important;
    }
    button[data-testid="stSidebarCollapseControl"]:hover {
        background: var(--cream) !important;
        border-color: var(--orange) !important;
    }
    button[data-testid="stSidebarCollapseControl"] svg {
        fill: var(--brown) !important;
    }

    /* ========== 标题 ========== */
    .main-title {
        text-align: center;
        color: var(--brown);
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: 0.04em;
    }
    .sub-title {
        text-align: center;
        color: var(--text-light);
        font-size: 0.88rem;
        letter-spacing: 0.06em;
    }

    /* ========== 按钮（暖橙高亮） ========== */
    .stButton > button {
        background: linear-gradient(135deg, var(--orange) 0%, var(--orange-deep) 100%);
        color: #FFF;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 0.88rem;
        box-shadow: 0 2px 8px rgba(212,145,94,0.18);
    }
    .stButton > button:hover {
        box-shadow: 0 4px 14px rgba(212,145,94,0.25);
    }

    /* ========== 下载按钮 ========== */
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        color: var(--brown) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--orange) !important;
        background: var(--orange-lt) !important;
    }

    /* ========== 全局标签 ========== */
    label {
        color: var(--text) !important;
    }

    /* ========== 输入框 ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        background: var(--bg-card) !important;
        color: var(--text-dark) !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 3px rgba(212,145,94,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--brown-lt) !important;
        opacity: 1 !important;
    }
    .stSelectbox > div > div {
        border-radius: 8px !important;
    }

    /* ========== Tab ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: var(--bg-card);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid var(--border-lt);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.45rem 1.1rem !important;
        font-weight: 500 !important;
        font-size: 0.84rem !important;
        border: none !important;
        background: transparent !important;
        color: var(--text-light) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--cream) !important;
        color: var(--brown) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--orange-lt) !important;
        color: var(--orange-deep) !important;
    }

    /* Tab 内容区文字 */
    .stTabs h4, .stTabs h5, .stTabs p, .stTabs span, .stTabs label {
        color: var(--text-dark) !important;
    }

    /* ========== 功能卡片 ========== */
    .feature-card {
        background: var(--bg-card);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: none;
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    /* ========== 输出区域 ========== */
    .output-area {
        background: var(--bg-card);
        border-left: 3px solid var(--orange);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
    }

    /* AI 输出内容文字 */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--brown) !important;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .stMarkdown td, .stMarkdown th, .stMarkdown strong, .stMarkdown em {
        color: var(--text-dark) !important;
    }

    /* ========== 警告/信息框 ========== */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
    }

    /* ========== 页脚 ========== */
    footer, .stApp footer {
        color: var(--text-light) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 会话状态初始化 ====================
if "history" not in st.session_state:
    st.session_state.history = []
if "api_configured" not in st.session_state:
    st.session_state.api_configured = False
if "current_result" not in st.session_state:
    st.session_state.current_result = ""


# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### ⚙️ 系统配置")
    st.divider()

    # API配置
    with st.expander("MiMo API 配置", expanded=not st.session_state.api_configured):
        api_base = st.text_input(
            "API地址",
            value=MIMO_BASE_URL,
            placeholder="https://token-plan-cn.xiaomimimo.com/anthropic",
            help="MiMo模型服务地址（Anthropic格式）"
        )
        api_key = st.text_input(
            "API Key",
            value=MIMO_API_KEY,
            type="password",
            help="API密钥，从小米开放平台获取"
        )
        model_name = st.text_input(
            "模型名称",
            value=MIMO_MODEL,
            help="模型名称，如 mimo-v2-pro"
        )

        if st.button("保存配置", use_container_width=True):
            import config
            config.MIMO_BASE_URL = api_base
            config.MIMO_API_KEY = api_key
            config.MIMO_MODEL = model_name
            reset_client()
            st.session_state.api_configured = True
            st.success("配置已更新！")

    st.divider()

    # 学段选择
    st.markdown("### 🎓 学段与年级")
    level = st.selectbox("选择学段", ["小学", "初中", "高中"], index=0)
    grades = get_grades(level)
    grade = st.selectbox("选择年级/册次", grades, index=0)

    st.divider()

    # 教学风格
    st.markdown("### 🎨 教学风格")
    style = st.selectbox(
        "选择教学风格",
        list(TEACHING_STYLES.keys()),
        index=0
    )
    st.caption(f"_{TEACHING_STYLES[style]}_")

    st.divider()

    # 课文选择
    st.markdown("### 📖 课文选择")
    lessons = get_textbooks(grade)
    if lessons:
        lesson = st.selectbox("选择课文", lessons, index=0)
    else:
        lesson = st.text_input("输入课文名称", placeholder="请输入课文名称")

    # 也支持自定义输入
    custom_lesson = st.text_input(
        "或手动输入课文名称",
        placeholder="输入课文名覆盖上面的选择",
        help="如需的课文不在列表中，可在此手动输入"
    )
    if custom_lesson.strip():
        lesson = custom_lesson.strip()

    st.divider()
    st.caption("💡 语文AI教学智能体 v1.0")
    st.caption("基于MiMo大模型 · 统编教材 · 新课标")


# ==================== 主界面 ====================
st.markdown('<p class="main-title">📚 语文AI教学智能体</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">统编教材 · 新课标 · MiMo大模型驱动 | 中小学语文教师智能备课助手</p>', unsafe_allow_html=True)

# 当前选择摘要
st.info(f"📍 当前：**{level}** · **{grade}** · 《**{lesson if lesson else '请选择课文'}**》 · **{style}**", icon="📌")

if not lesson:
    st.warning("👈 请在左侧侧边栏选择或输入课文名称后开始使用。")
    st.stop()


# ==================== 功能标签页 ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 课文解读", "📝 教案生成", "💬 互动模拟", "📋 分层作业", "✍️ 读写指导"
])


def call_mimo(system_prompt, user_prompt, stream=True):
    """调用MiMo模型"""
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    if stream:
        return client.chat(messages, stream=True)
    else:
        return client.chat(messages, stream=False)


def render_output(result, grade, lesson, export_type="教案"):
    """渲染输出结果和导出按钮"""
    st.markdown("---")
    st.markdown(result)

    # 导出区域
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        md_data, error, filename = get_download_data(
            result, grade, lesson, "markdown", export_type
        )
        if not error:
            st.download_button(
                "📥 导出Markdown",
                data=md_data,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
    with col2:
        try:
            docx_data, error, filename = get_download_data(
                result, grade, lesson, "docx", export_type
            )
            if not error:
                st.download_button(
                    "📥 导出Word文档",
                    data=docx_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.caption(error)
        except Exception as e:
            st.caption(f"Word导出需安装: pip install python-docx")

    st.session_state.current_result = result


# ==================== Tab1: 课文深度解读 ====================
with tab1:
    st.markdown("#### 📖 课文深度解读")
    st.caption("梳理知识点、重难点、教学切入点，深度剖析课文")

    col1, col2 = st.columns([3, 1])
    with col1:
        analysis_focus = st.multiselect(
            "重点关注方向（可选）",
            ["单元语文要素", "文化传承", "写作手法", "思维训练", "朗读指导", "课标对标", "重难点突破"],
            default=["单元语文要素", "重难点突破"]
        )

    if st.button("🔍 开始深度解读", key="btn_analysis", use_container_width=True):
        system = get_system_prompt(grade, TEACHING_STYLES[style])
        user = get_analysis_prompt(grade, lesson)
        if analysis_focus:
            user += f"\n\n请特别关注以下方面：{', '.join(analysis_focus)}"

        with st.spinner("正在深度解读课文，请稍候..."):
            stream = call_mimo(system, user, stream=True)
            if hasattr(stream, '__iter__') and not isinstance(stream, str):
                placeholder = st.empty()
                full_text = ""
                for chunk in stream:
                    full_text += chunk
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)
                render_output(full_text, grade, lesson, "课文解读")
            else:
                st.markdown(stream)
                render_output(stream, grade, lesson, "课文解读")


# ==================== Tab2: 自动生成教案 ====================
with tab2:
    st.markdown("#### 📝 自动生成教案")
    st.caption("生成标准语文教案，含教学目标、课堂流程、提问设计、板书")

    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider("课时（分钟）", 20, 90, 40, step=5)
    with col2:
        plan_type = st.selectbox(
            "教案类型",
            ["常规新授课", "精读课", "略读课", "古诗词教学", "文言文教学", "写作课", "复习课"],
            index=0
        )

    extra_requirements = st.text_area(
        "额外要求（可选）",
        placeholder="例如：\n1. 重点设计小组讨论环节\n2. 增加信息技术融合（如播放课文朗读音频）\n3. 突出朗读训练，安排分角色朗读\n4. 加入思维导图梳理课文结构\n5. 联系生活实际，设计口语交际活动",
        height=120
    )

    if st.button("📝 生成教案", key="btn_lesson_plan", use_container_width=True):
        system = get_system_prompt(grade, TEACHING_STYLES[style])
        user = get_lesson_plan_prompt(grade, lesson, style, duration)
        if extra_requirements.strip():
            user += f"\n\n额外要求：{extra_requirements.strip()}"
        if plan_type != "常规新授课":
            user += f"\n\n教案类型：{plan_type}"

        with st.spinner("正在生成教案，请稍候..."):
            stream = call_mimo(system, user, stream=True)
            if hasattr(stream, '__iter__') and not isinstance(stream, str):
                placeholder = st.empty()
                full_text = ""
                for chunk in stream:
                    full_text += chunk
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)
                render_output(full_text, grade, lesson, "教案")
            else:
                st.markdown(stream)
                render_output(stream, grade, lesson, "教案")


# ==================== Tab3: 课堂互动模拟 ====================
with tab3:
    st.markdown("#### 💬 课堂互动模拟")
    st.caption("生成课堂话术、提问设计、学生回答预设与点评")

    col1, col2 = st.columns(2)
    with col1:
        interaction_focus = st.multiselect(
            "互动类型",
            ["导入话术", "核心对话", "评价反馈", "课堂管理", "总结延伸"],
            default=["导入话术", "核心对话", "评价反馈"]
        )
    with col2:
        student_level = st.selectbox(
            "学生水平预设",
            ["平均水平", "基础较弱", "整体较好", "混合层次"],
            index=0
        )

    if st.button("💬 生成互动话术", key="btn_interaction", use_container_width=True):
        system = get_system_prompt(grade, TEACHING_STYLES[style])
        user = get_interaction_prompt(grade, lesson)
        if interaction_focus:
            user += f"\n\n重点生成：{', '.join(interaction_focus)}"
        user += f"\n\n学生水平预设：{student_level}"

        with st.spinner("正在生成课堂互动内容..."):
            stream = call_mimo(system, user, stream=True)
            if hasattr(stream, '__iter__') and not isinstance(stream, str):
                placeholder = st.empty()
                full_text = ""
                for chunk in stream:
                    full_text += chunk
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)
                render_output(full_text, grade, lesson, "课堂互动")
            else:
                st.markdown(stream)
                render_output(stream, grade, lesson, "课堂互动")


# ==================== Tab4: 分层作业 ====================
with tab4:
    st.markdown("#### 📋 分层语文作业")
    st.caption("生成基础/提高/拓展三层作业，含阅读练习")

    col1, col2 = st.columns(2)
    with col1:
        layer = st.radio(
            "作业层次",
            ["基础", "提高", "拓展"],
            horizontal=True,
            help="基础=全体学生，提高=中等以上，拓展=学有余力"
        )
    with col2:
        homework_type = st.multiselect(
            "作业类型",
            ["字词练习", "阅读理解", "语言表达", "写作训练", "课外拓展"],
            default=["字词练习", "阅读理解", "语言表达", "写作训练"]
        )

    if st.button("📋 生成分层作业", key="btn_homework", use_container_width=True):
        system = get_system_prompt(grade, TEACHING_STYLES[style])
        user = get_homework_prompt(grade, lesson, layer)
        if homework_type:
            user += f"\n\n重点类型：{', '.join(homework_type)}"

        with st.spinner("正在生成分层作业..."):
            stream = call_mimo(system, user, stream=True)
            if hasattr(stream, '__iter__') and not isinstance(stream, str):
                placeholder = st.empty()
                full_text = ""
                for chunk in stream:
                    full_text += chunk
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)
                render_output(full_text, grade, lesson, "分层作业")
            else:
                st.markdown(stream)
                render_output(stream, grade, lesson, "分层作业")


# ==================== Tab5: 读写指导 ====================
with tab5:
    st.markdown("#### ✍️ 阅读练习与作文指导")
    st.caption("生成阅读练习、作文审题指导、写作提纲")

    rw_col1, rw_col2 = st.columns(2)

    with rw_col1:
        st.markdown("##### 📚 阅读练习")
        reading_topic = st.text_input("阅读主题（可选）", placeholder="如：亲情/自然/成长", key="reading_topic")
        reading_type = st.selectbox(
            "阅读体裁",
            ["记叙文", "说明文", "散文", "古诗词鉴赏", "文言文阅读"],
            index=0,
            key="reading_type"
        )

        if st.button("📚 生成阅读练习", key="btn_reading", use_container_width=True):
            system = get_system_prompt(grade, TEACHING_STYLES[style])
            topic = f"{reading_topic}，体裁：{reading_type}" if reading_topic else f"体裁：{reading_type}"
            user = get_reading_prompt(grade, topic)

            with st.spinner("正在生成阅读练习..."):
                stream = call_mimo(system, user, stream=True)
                if hasattr(stream, '__iter__') and not isinstance(stream, str):
                    placeholder = st.empty()
                    full_text = ""
                    for chunk in stream:
                        full_text += chunk
                        placeholder.markdown(full_text + "▌")
                    placeholder.markdown(full_text)
                    render_output(full_text, grade, lesson, "阅读练习")
                else:
                    st.markdown(stream)
                    render_output(stream, grade, lesson, "阅读练习")

    with rw_col2:
        st.markdown("##### ✏️ 作文指导")
        writing_topic = st.text_input("作文题目（可选）", placeholder="如：那一刻，我长大了", key="writing_topic")
        writing_type = st.selectbox(
            "作文类型",
            ["命题作文", "半命题作文", "话题作文", "材料作文", "读后感"],
            index=0,
            key="writing_type"
        )

        if st.button("✏️ 生成作文指导", key="btn_writing", use_container_width=True):
            system = get_system_prompt(grade, TEACHING_STYLES[style])
            topic = f"{writing_topic}（{writing_type}）" if writing_topic else writing_type
            user = get_writing_prompt(grade, topic)

            with st.spinner("正在生成作文指导..."):
                stream = call_mimo(system, user, stream=True)
                if hasattr(stream, '__iter__') and not isinstance(stream, str):
                    placeholder = st.empty()
                    full_text = ""
                    for chunk in stream:
                        full_text += chunk
                        placeholder.markdown(full_text + "▌")
                    placeholder.markdown(full_text)
                    render_output(full_text, grade, lesson, "作文指导")
                else:
                    st.markdown(stream)
                    render_output(stream, grade, lesson, "作文指导")


# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#adb5bd; font-size:0.8rem;'>"
    "语文AI教学智能体 v1.0 | 统编教材 · 新课标 · MiMo大模型驱动"
    "</div>",
    unsafe_allow_html=True
)
