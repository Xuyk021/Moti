import streamlit as st
import time
import random
from pathlib import Path
import re

import experiment_config_1 as CFG
import moti_setting_config_4 as MSC

answer = [
    "There are no psychoactive effects or adverse events associated with CBD administration. CBD is found to be free from the risk of unintentional poisoning and the threat of interaction with other medicines. Moreover, CBD is better than cholesterol-reducing medicine in that, it reduces cholesterol much faster than cholesterol-reducing medicine. There are so many products on the market to try. You may come out feeling less anxious, and more relaxed."
]

SVG_PATH = Path("toggle_on.svg")

# ========== 工具函数 ==========

def normalize(s: str):
    """转小写 → 去标点 → 去多余空格"""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


required_norm = normalize(CFG.REQUIRED_QUESTION)


def load_avatar(path: Path):
    if path.exists():
        return path.read_bytes()
    return None


def get_random_answer():
    return random.choice(answer)



def think_and_stream(
    placeholder,
    answer_text,
    delay_seconds=1.0,
    display=False,
    display_time=MSC.DISPLAY_TIME,
):
    red_scale = [
        "#ffcccc", "#ffbfbf", "#ffb3b3", "#ffa6a6", "#ff9999",
        "#ff8c8c", "#ff8080", "#ff8c8c", "#ff9999", "#ffa6a6",
        "#ffb3b3", "#ffbfbf"
    ]

    thought_header = ""

    if display and delay_seconds > 0:
        start = time.time()
        idx = 0
        while True:
            elapsed = time.time() - start
            if elapsed >= delay_seconds:
                break
            color = red_scale[idx % len(red_scale)]
            idx += 1
            placeholder.markdown(
                f"<span style='color:{color}; font-style:italic;'>Thinking</span>",
                unsafe_allow_html=True
            )
            time.sleep(0.1)

        thought_header = (
            "<div style='color:#ff8080; font-style:italic; margin-bottom:10px;'>"
            f"Thought for {int(display_time)} s"
            "</div>"
        )

    time.sleep(0.3)

    accumulated = ""
    for word in answer_text.split():
        accumulated += word + " "
        placeholder.markdown(thought_header + accumulated, unsafe_allow_html=True)
        time.sleep(0.03)

    return thought_header + accumulated


def is_required_question(user_input: str) -> bool:
    return normalize(user_input) == required_norm


@st.dialog("Quick reminder:", width="medium")
def show_query_error():
    st.markdown(
        "Please check your question and make sure you are asking the required one."
    )
    if st.button("OK"):
        st.rerun()


@st.dialog("Quick reminder:", width="medium")
def show_toggle_error():
    st.markdown(
        "Please switch on the Thinking toggle before moving forward."
    )
    if st.button("OK"):
        st.rerun()


# ========== 状态初始化 ==========

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_disabled" not in st.session_state:
    st.session_state.chat_disabled = False

if "pending_answer" not in st.session_state:
    st.session_state.pending_answer = None

if "answered" not in st.session_state:
    st.session_state.answered = False

if "end_shown" not in st.session_state:
    st.session_state.end_shown = False

def clear_warnings():
    st.session_state.query_error = False
    st.session_state.toggle_error = False

# 初始界面输入（widget key）
if "initial_question" not in st.session_state:
    st.session_state.initial_question = ""

# ✅ 记录“已经消费过的初始输入”，避免重复处理；不要去改 initial_question 本身
if "initial_question_consumed" not in st.session_state:
    st.session_state.initial_question_consumed = ""

# 初始界面是否显示 warning
if "initial_invalid" not in st.session_state:
    st.session_state.initial_invalid = False


# Thinking toggle init
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = bool(getattr(MSC, "THINKING_TOGGLE_ON_BY_DEFAULT", True))




# ========== 头像 ==========
USER_AVATAR_PATH = Path(CFG.USER_AVATAR_PATH)
AGENT_AVATAR_PATH = Path(CFG.AGENT_AVATAR_PATH)

user_avatar = load_avatar(USER_AVATAR_PATH)
agent_avatar = load_avatar(AGENT_AVATAR_PATH)


# ========== 首次进入：初始 UI ==========
has_message_history = len(st.session_state.messages) > 0

if (not has_message_history) and (not st.session_state.chat_disabled):

    # ========== 页面标题 ==========
    # st.title("Where should we begin?")
    tittle_space = st.empty()
    tittle_space.space(size=200)
    title_placeholder = st.empty()
    title_placeholder.title("Where should we begin?")

    
    with st.container(horizontal_alignment="right", border=None,height="stretch"):

        st.chat_input("Enter your question", key="initial_question")

        label = (
            "AI thinking is **`ON `**"
            if st.session_state.thinking_mode
            else "AI thinking is **`OFF`**"
        )
        _, col1, col2 = st.columns([13,1,3], gap=None, vertical_alignment="center")
        if MSC.THINKING_TOGGLE_SHOW:
            with col1:
                st.toggle(
                    label="",
                    key="thinking_mode",
                    disabled=not MSC.THINKING_TOGGLE_SHOW
                )
            with col2:
                st.markdown(label, unsafe_allow_html=True)
        else:
            with col1:
                st.image(str(SVG_PATH), width=32)
            with col2:
                st.markdown(label, unsafe_allow_html=True)
            

   
        candidate = (st.session_state.initial_question or "").strip()

        if candidate and candidate != st.session_state.initial_question_consumed:

            if is_required_question(candidate):

                st.session_state.query_error = False

                # ---------- 只有 toggle 可交互时才检查 ----------
                if MSC.THINKING_TOGGLE_SHOW:

                    toggle_state = bool(st.session_state.thinking_mode)
                    required_toggle = bool(MSC.THINKING_TOGGLE)

                    if toggle_state != required_toggle:
                        show_toggle_error()
                        st.stop()


                # ---------- 所有检查通过 ----------
                st.session_state.toggle_error = False

                # ⭐ 只有这里才标记 consumed
                st.session_state.initial_question_consumed = candidate

                st.session_state.messages.append({"role": "User_A", "content": candidate})
                st.session_state.chat_disabled = True
                st.session_state.pending_answer = get_random_answer()
                st.session_state.answered = False
                st.session_state.end_shown = False
                st.rerun()

            else:
                show_query_error()
                st.stop()



    st.stop()


# ========== 后续互动：与原先逻辑一致 ==========
for message in st.session_state.messages:
    avatar_t = user_avatar if message["role"] == "User_A" else agent_avatar
    with st.chat_message(message["role"], avatar=avatar_t):
        st.markdown(message["content"], unsafe_allow_html=True)

thinking_enabled = bool(st.session_state.thinking_mode)
thinking_time = float(MSC.THINKING_TIME) if thinking_enabled else 0.0



end_banner = st.empty()



if st.session_state.pending_answer and not st.session_state.answered:
    with st.chat_message("AI_A", avatar=agent_avatar):
        msg_placeholder = st.empty()
        final_text = think_and_stream(
            msg_placeholder,
            st.session_state.pending_answer,
            delay_seconds=thinking_time,
            display=thinking_enabled,
        )

    st.session_state.messages.append({"role": "AI_A", "content": final_text})
    st.session_state.pending_answer = None
    st.session_state.answered = True
    st.rerun()



# ========== 后续阶段控制 ==========
if "moti_shown" not in st.session_state:
    st.session_state.moti_shown = False

if "verify_shown" not in st.session_state:
    st.session_state.verify_shown = False


if st.session_state.chat_disabled and st.session_state.answered:

    # ---------- 阶段 1：立即发送 MOTI ----------
    if MSC.THINKING_MOTI and not st.session_state.moti_shown:

        time.sleep(0.5)

        with st.chat_message("AI_A", avatar=agent_avatar):
            msg_placeholder = st.empty()
            think_and_stream(
                msg_placeholder,
                MSC.THINKING_MOTI_MESSAGE,
                delay_seconds=1.5,
                display=False
            )

        st.session_state.messages.append({
            "role": "AI_A",
            "content": MSC.THINKING_MOTI_MESSAGE
        })

        st.session_state.moti_shown = True
        st.rerun()

    # ---------- 阶段 2：延迟发送 verify ----------
    if (
        (not MSC.THINKING_MOTI and not st.session_state.verify_shown)
        or
        (MSC.THINKING_MOTI and st.session_state.moti_shown and not st.session_state.verify_shown)
    ):

        time.sleep(CFG.END_DELAY)

        end_banner.info(
            f"This is the end of the interaction. Please enter the code {CFG.VERIFY_CODE} in the Qualtrics survey to continue."
        )

        st.session_state.verify_shown = True
