"""
小航 · 郑州航院校园信息查询AI助手 - Streamlit Web版本
主程序入口
"""
import sys
from pathlib import Path
# 把项目根目录加入Python路径，解决找不到src包的问题
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.prompts import load_school_info, get_system_prompt
from src.api import ask_ai
from src.config import PRESET_QUESTIONS


# ========== 页面配置 ==========
st.set_page_config(
    page_title="小航 · 郑州航院校园信息助手",
    page_icon="✈️",
    layout="wide",
)

# 隐藏右上角整个工具栏（Deploy按钮、菜单等全部隐藏）
hide_menu_style = """
<style>
/* 隐藏整个顶部工具栏 */
div[data-testid="stToolbar"] {
    display: none !important;
}
/* 隐藏底部Streamlit页脚 */
footer {
    visibility: hidden !important;
}
/* 隐藏右上角设置弹窗入口 */
button[title="Settings"] {
    display: none !important;
}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ========== 初始化：历史对话 + 资料缓存（页面加载只读一次，不用每次提问都读文件） ==========
if "history" not in st.session_state:
    st.session_state.history = []

if "school_info" not in st.session_state:
    # 页面打开时一次性加载所有校园资料，缓存起来
    st.session_state.school_info = load_school_info()


# ========== AI回答缓存（相同身份+相同问题30分钟内不重复调API） ==========
@st.cache_data(ttl=1800, show_spinner=False)
def cached_ask_ai(role: str, question: str) -> str:
    """带缓存的AI调用，ttl=1800秒(30分钟)"""
    school_info = st.session_state.school_info
    system_prompt = get_system_prompt(role, school_info)
    return ask_ai(system_prompt, question)

# ========== 主体两列：左侧历史对话，右侧主内容（直接显示，不用找侧边栏） ==========
history_col, _, main_col, _ = st.columns([1, 0.2, 3, 0.2])

# ---- 左侧：历史对话（直接显示，不用折叠） ----
with history_col:
    st.subheader("⚙️ 设置")
    # 身份选择移到左边
    role = st.selectbox(
        "选择身份：",
        ["新生", "在校生", "教师"],
        index=0,
    )
    st.divider()

    st.subheader("📋 历史")
    col_clear1, col_clear2 = st.columns(2)
    with col_clear1:
        if st.button("🗑️ 清空记录", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    with col_clear2:
        if st.button("🧹 清空缓存", use_container_width=True):
            cached_ask_ai.clear()
            st.rerun()
    st.divider()

    if not st.session_state.history:
        st.caption("暂无记录")
    else:
        # 倒序：最新的在最上面
        for idx, chat in enumerate(reversed(st.session_state.history)):
            q_short = chat["用户问题"][:10] + "..." if len(chat["用户问题"]) > 10 else chat["用户问题"]
            with st.expander(q_short, expanded=False):
                st.markdown("**问：**")
                st.write(chat["用户问题"])
                st.markdown("**答：**")
                st.write(chat["AI回答"])

# ========== 右侧主区域：标题 + 身份 + 推荐问题 + 输入 + 回答 ==========
with main_col:
    # ========== 标题 ==========
    st.title("✈️ 小航 · 郑州航院校园信息助手")
    st.caption("郑州航空工业管理学院 · 人工智能专业认知实习项目")
    st.divider()

    # ========== 推荐问题按钮 ==========
    st.markdown("**💡 试试这些问题：**")
    questions = PRESET_QUESTIONS.get(role, [])
    cols = st.columns(4)
    for i, q in enumerate(questions):
        with cols[i % 4]:
            if st.button(q, key=f"btn_q_{i}", use_container_width=True):
                st.session_state["question_input"] = q
                st.rerun()

    st.divider()

    # ========== 问题输入 ==========
    default_question = st.session_state.get("question_input", "")
    question = st.text_input(
        "有啥想问的？直接输入：",
        value=default_question,
        placeholder="比如：报到流程是什么？校园卡丢了怎么办？",
    )

    # ========== 回答区（核心逻辑完全不动，保证稳定） ==========
    if question and question.strip():
        # 先检查数据文件是否存在
        data_files = list(Path("data").glob("*.md"))
        if not data_files:
            st.warning("⚠️ 数据文件缺失，请确认data/目录下有4个Markdown资料文件")
        else:
            with st.spinner("小航正在思考..."):
                # 使用缓存：相同身份+相同问题30分钟内直接返回缓存结果
                answer = cached_ask_ai(role, question)

                # 根据返回结果分类显示
                if answer.startswith("[ERROR_401]"):
                    st.error("❌ API Key失效，请检查config.py里的硅基流动API Key是否正确")
                elif answer.startswith("[ERROR_TIMEOUT]"):
                    st.error("⏰ AI响应超时，请稍后再试")
                elif answer.startswith("[ERROR_NETWORK]"):
                    st.error("🌐 网络连接失败，请检查你的网络")
                elif answer.startswith("[ERROR_"):
                    st.error(f"❌ {answer}")
                else:
                    st.success("✅ 小航回答：")
                    st.write(answer)
                    # 回答成功，加入左侧历史记录（只存不影响回答）
                    st.session_state.history.append({
                        "用户问题": question,
                        "AI回答": answer
                    })
                    # 最多保留10条历史
                    if len(st.session_state.history) > 10:
                        st.session_state.history.pop(0)

        # 清空推荐问题标记
        if "question_input" in st.session_state:
            del st.session_state["question_input"]

    st.divider()

    # ========== 电话黄页静态页（兜底，不依赖API） ==========
    st.header("📞 学校各部门常用联系电话")
    st.caption("AI答不上来、网络不好的时候，直接查这里，永远能用")

    yellow_page = """
    | 部门 | 电话 |
    |------|------|
    | 校园110（保卫处24小时） | 0371-61916110 ⚠ 以官方为准 |
    | 学校总值班室（24小时） | 0371-61911000 ⚠ 以官方为准 |
    | 后勤管理处 | 0371-61912800 ⚠ 以官方为准 |
    | 后勤服务热线/物业报修 | 0371-61913110 ⚠ 以官方为准 |
    | 校医院急诊（24小时） | 0371-61912730 ⚠ 以官方为准 |
    | 招生办公室 | 0371-61916161 ⚠ 以官方为准 |
    | 信息管理中心（网信中心） | 0371-61912718 ⚠ 以官方为准 |
    | 心理健康教育中心 | 0371-6191xxxx ⚠ 以官方为准 |
    | 学生处资助中心 | 0371-6191xxxx ⚠ 以官方为准 |
    """
    st.markdown(yellow_page)

    st.divider()

    # ========== 底部边界声明 ==========
    st.caption("📌 边界说明：")
    st.caption("• 仅能回答郑州航院校园相关问题，不接入学校教务/一卡通系统")
    st.caption("• 所有信息仅供参考，如有变动请以学校官方通知为准")
    st.caption("• 紧急情况请直接拨打校园110：0371-61916110")