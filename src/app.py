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
    layout="centered",
)

# ========== 标题 ==========
st.title("✈️ 小航 · 郑州航院校园信息助手")
st.caption("郑州航空工业管理学院 · 人工智能专业认知实习项目")
st.divider()

# ========== 身份选择 ==========
role = st.selectbox(
    "请选择你的身份：",
    ["新生", "在校生", "教师"],
    index=0,
)

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

# ========== 回答区 ==========
if question and question.strip():
    # 先检查数据文件是否存在
    data_files = list(Path("data").glob("*.md"))
    if not data_files:
        st.warning("⚠️ 数据文件缺失，请确认data/目录下有4个Markdown资料文件")
    else:
        with st.spinner("小航正在思考..."):
            # 加载学校资料，组装Prompt
            school_info = load_school_info()
            system_prompt = get_system_prompt(role, school_info)
            # 调用API
            answer = ask_ai(system_prompt, question)

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

st.divider()

# ========== 电话黄页静态页（兜底，不依赖API） ==========
st.header("📞 电话黄页（静态兜底）")
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
