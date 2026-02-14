import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Toggle Comparison")

# ========= SVG 文件路径 =========
SVG_PATH = Path("toggle_on.svg")

st.title("Toggle Comparison")

st.write("### Interactive Toggle vs SVG Toggle")

# —— 两列布局 ——
col1, col2 = st.columns(2, vertical_alignment="center")

# ========= 左侧：真实 Streamlit toggle =========
with col1:
    st.subheader("Interactive Toggle")

    toggle_value = st.toggle(
        "AI thinking mode",
        value=True
    )

    st.caption(f"Current state: {'ON' if toggle_value else 'OFF'}")

# ========= 右侧：SVG 假 toggle =========
with col2:
    st.subheader("SVG Toggle (visual only)")

    # 显示 SVG —— 尺寸匹配 toggle
    st.image(str(SVG_PATH), width=32)

    st.caption("Visual indicator only — not interactive")
