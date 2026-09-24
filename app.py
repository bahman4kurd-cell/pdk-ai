import streamlit as st

# ڕێکخستنی پەڕە
st.set_page_config(
    page_title="PDK AI - پلاتفۆرمی زیرەکی پارتی", page_icon="🟢", layout="centered"
)

# ڕووکاری سەرەکی (CSS Styling)
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #1b5e20;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 15px;
        margin-bottom: 20px;
    }
    .stChatInput {
        direction: rtl;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# سیستەمی چوونەژوورەوەی سادە (Login System بۆ پاراستنی ئەپەکە)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown(
        '<p class="main-title">بەخێر هاتن بۆ PDK AI</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">تکایە بۆ بەکارهێنانی ئەم ئینتەرفەیسە، تێپەڕە بە'
        " ئەکاونتەکەتدا</p>",
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        user_email = st.text_input(
            "ئیمەیڵ (گۆگڵ یان هۆتمایڵ):", placeholder="example@gmail.com"
        )
        user_pass = st.text_input("پاسوۆرد:", type="password")
        submit_btn = st.form_submit_button("چوونەژوورەوە (Login)")

        if submit_btn:
            if user_email and len(user_pass) > 3:
                st.session_state.logged_in = True
                st.session_state.user_email = user_email
                st.rerun()
            else:
                st.error("تکایە ئیمەیڵ و پاسوۆرد بە دروستی بنووسە!")

else:
    # بەشی سەرەکی چات دوای چوونەژوورەوە
    st.sidebar.title("زانیاری بەکارهێنەر")
    st.sidebar.write(f"👤 بەخێر هاتیت:")
    st.sidebar.code(st.session_state.user_email)

    if st.sidebar.button("دەرچوون (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown(
        '<p class="main-title">PDK AI Assistant</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">ئەم ئەی ئایە تایبەتە بە مێژوو و پێکهاتەی'
        " ڕێکخراوەیی پارتی دیموکراتی کوردستان</p>",
        unsafe_allow_html=True,
    )

    # پاشەکەوتکردنی مێژووی چات
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"سڵاو {st.session_state.user_email.split('@')[0]}! من PDK"
                    " AIـم. دەتوانیت هەر پرسیارێکت هەبێت لەسەر مێژوو،"
                    " کۆنگرەکان، یان ئۆرگانەکانی پارتی لێرە بپرسیت."
                ),
            }
        ]

    # نیشاندانی نامەکانی پێشوو
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # وەگرتنی پرسیار لە بەکارهێنەر
    if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # وەڵامدانی زیرەکانە و شیکاری مێژوویی
        with st.chat_message("assistant"):
            prompt_lower = prompt.lower()
            if "مێژوو" in prompt_lower or "دامەزراندن" in prompt_lower:
                response = (
                    "پارتی دیموکراتی کوردستان لە 16ـی ئابی 1946 بە سەرۆکایەتی"
                    " نەمر مەلا مستەفا بارزانی دامەزرا، وەک یەکەم حیزبی"
                    " نیشتمانی خاوەن خەبات لە مێژووی هاوچەرخی کوردستاندا."
                )
            elif "مەکتەبی سیاسی" in prompt_lower:
                response = (
                    "مەکتەبی سیاسی یەکێکە لە ئۆرگانە باڵاکانی سەرکردایەتی"
                    " پارتیدا کە لە نێوان دوو کۆنگرەدا بەرپرسیارە لە جێبەجێکردنی"
                    " بڕیارە سیاسی و سازمانداییەکان."
                )
            else:
                response = (
                    f"سوپاس بۆ پرسیارەکەت دەربارەی ({prompt}). ئەی ئایەکەی"
                    " ئێمە لە هەوڵی بەردەوامدایە بۆ پێشکەشکردنی وردترین"
                    " زانیاری مێژوویی و سازمانی دەربارەی پارتی."
                )

            st.markdown(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )