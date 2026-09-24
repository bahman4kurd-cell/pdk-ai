import streamlit as st

# ڕێکخستنی پەڕەی ڕووکەش
st.set_page_config(
    page_title="PDK AI", page_icon="🟢", layout="centered"
)

# ڕووکاری سەرەکی (UI Styling)
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #2b7a0b;
        font-size: 38px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 16px;
        margin-bottom: 30px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">PDK AI Assistant</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">ئەم ئەی ئایە تایبەتە بە پێدانی زانیاری لەسەر مێژوو و'
    " پێکهاتەی پارتی دیموکراتی کوردستان</p>",
    unsafe_allow_html=True,
)

# سیستەم پرۆمپت و زانیاری سەرەتایی ئەی ئای
SYSTEM_PROMPT = (
    "تۆ زیرەکی دەستکردێکی تایبەت بە مێژوو، پێکهاتەی ڕێکخراوەیی و ئۆرگانەکانی"
    " پارتی دیموکراتی کوردستان (پارتی) ت. وەڵامەکانت بە زمانی کوردی سۆرانی"
    " ڕوون، مێژوویی، فەرمی و بێلایەن دەبن."
)

# پاشەکەوتکردنی مێژووی چات لە سێشنەکەدا
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سڵاو! من PDK AIـم. چ پرسیارێکت هەەیە لەسەر مێژوو و ئۆرگانەکانی پارتی دیموکراتی کوردستان؟"}
    ]

# نیشاندانی نامەکانی پێشوو لە ڕووکەشدا
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەگرتنی پرسیار لە بەکارهێنەر (بێ لۆگین و ڕاستەوخۆ)
if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # لێرەدا دەتوانیت APIـیەک (وەک OpenAI یان Groq) بەکاربهێنیت یان وەڵامی زیرەکانەی ناوخۆیی دادەنێیت
    # بۆ نموونە وەڵامدانەوەی سەرەتایی:
    with st.chat_message("assistant"):
        # لێرە دەتوانین دەقێکی شیکاری تێبکەین یان بەستەری بە API بکەین
        if (
            "مێژوو" in prompt
        ) or ("دامەزراندن" in prompt):
            response = "پارتی دیموکراتی کوردستان لە 16ـی ئابی 1946 بە سەرۆکایەتی مەلا مستەفا بارزانی دامەزرا..."
        else:
            response = f"سوپاس بۆ پرسیارەکەت دەربارەی ({prompt}). وەک ئەی ئایەکی تایبەت بە پارتی، لە داهاتوودا بنکەی زانیاری تەواوی تێدا دەبێت بۆ وەڵامدانی ورد."

        st.markdown(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )