import json
import os
import streamlit as st

try:
  from groq import Groq

  GROQ_AVAILABLE = True
except ImportError:
  GROQ_AVAILABLE = False

st.set_page_config(
    page_title="PDK AI - پلاتفۆرمی خێرای زیرەکی دەستکرد",
    page_icon="⚡",
    layout="centered",
)

DATA_FILE = "pdk_knowledge.json"


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


def save_data(data_list):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)


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
  st.sidebar.title("🎛️ کۆنترۆڵی ئەدەمین")
  admin_mode = st.sidebar.checkbox("دۆخی بەڕێوەبەر (Admin Mode)")

  if admin_mode:
    admin_pass = st.sidebar.text_input("پاسوۆردی ئەدەمین:", type="password")
    if admin_pass == "1234":
      st.sidebar.success("بە سەرکەوتوویی چوویە ژوورەوە وەک ئەدەمین!")

      st.sidebar.subheader("⚙️ هەڵبژاردنی مۆدێلی زیرەکی دەستکرد")
      selected_model = st.sidebar.selectbox(
          "مۆدێلی کارا:",
          [
              "llama-3.1-8b-instant",
              "llama-3.2-3b-preview",
              "mixtral-8x7b-32768",
          ],
      )
      st.session_state.chosen_model = selected_model

      st.sidebar.subheader("➕ زیادکردنی زانیاری خێرا")
      with st.sidebar.form("add_knowledge_form"):
        title = st.text_input("ناونیشانی بابەت (ئارەزوومەند):")
        uploaded_file = st.file_uploader(
            "فایلی دەقی ئەتاچ بکە (TXT یان MD)", type=["txt", "md"]
        )
        content_manual = st.text_area("یان دەق لێرە بنووسە:")
        submitted = st.form_submit_button("پاشەکەوتکردن لە سیستەم")

        if submitted:
          data = load_data()
          final_content = ""

          if uploaded_file is not None:
            try:
              final_content = uploaded_file.read().decode("utf-8")
              if not title:
                title = uploaded_file.name
            except Exception as e:
              st.sidebar.error(f"کێشە لە خوێندنەوەی فایلدا هەبوو: {e}")
          else:
            final_content = content_manual

          if not title and final_content:
            title = (
                final_content.split("\n")[0][:30] + "..."
                if len(final_content) > 30
                else final_content
            )

          if final_content:
            data.append({"title": title, "content": final_content})
            save_data(data)
            st.sidebar.success("زانیارییەکان بە سەرکەوتوویی پاشەکەوت کران!")
          else:
            st.sidebar.warning("تکایە ناوەڕۆکێک یان فایلێک دابین بکە.")
    else:
      st.sidebar.warning("تکایە پاسوۆردی دروست بنووسە.")

  if "chosen_model" not in st.session_state:
    st.session_state.chosen_model = "llama-3.1-8b-instant"

  st.sidebar.markdown("---")
  st.sidebar.title("زانیاری بەکارهێنەر")
  st.sidebar.write("👤 بەخێر هاتیت:")
  st.sidebar.code(st.session_state.user_email)
  st.sidebar.info(f"مۆدێلی کارا: {st.session_state.chosen_model}")

  if st.sidebar.button("دەرچوون (Logout)"):
    st.session_state.logged_in = False
    st.rerun()

  st.markdown(
      '<p class="main-title">PDK AI Assistant (Ultra Fast)</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="subtitle">سیستەمی خێرای ڕاوێژکاری بە بەکارهێنانی Llama و'
      " مۆدێلەکانی Groq</p>",
      unsafe_allow_html=True,
  )

  if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"سڵاو {st.session_state.user_email.split('@')[0]}! من"
                " ئامادەم بە خێراییەکی پێوانەیی وەڵامی پرسیارەکانت بدەمەوە"
                " لەسەر بنەمای فایله تۆمارکراوەکان."
            ),
        }
    ]

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("خەریکی وەڵامدانەوەیە بە خێراییەکی بەرز..."):
        custom_data = load_data()
        response = ""

        context_text = ""
        if custom_data:
          for idx, item in enumerate(custom_data, 1):
            context_text += (
                f"\n--- سەرچاوە [{idx}]: {item.get('title')} ---\n"
                f"{item.get('content')}\n"
            )

        system_prompt = (
            "تۆ یاریدەدەرێکی زیرەکی دەستکردی زۆر خێرای. ئەرکی تۆ ئەوەیە کە بەپێی"
            " ئەو زانیاری و فایلانەی خوارەوە، بە شێوازێکی زانستی و پوخت وەڵامی"
            " پرسیاری بەکارهێنەر بدەیتەوە بە زمانی کوردی سۆرانی. ئەگەر وەڵامەکە"
            " لە ناو داتاکاندا نەبوو، ڕاستەوخۆ پێی بڵێ کە لەو زانیارییانەدا"
            " بوونی نییە.\n\n"
            f"فایل و زانیارییە تۆمارکراوەکان:\n{context_text}"
        )

        groq_api_key = os.environ.get("GROQ_API_KEY", "")
        if "GROQ_API_KEY" in st.secrets:
          groq_api_key = st.secrets["GROQ_API_KEY"]

        if GROQ_AVAILABLE and groq_api_key:
          try:
            client = Groq(api_key=groq_api_key)
            # تاقیکردنەوەی مۆدێلی هەڵبژێردراو، خۆ ئەگەر هەڵەی هەبوو مۆدێلی تریش تاقی دەکاتەوە
            models_to_try = [
                st.session_state.chosen_model,
                "llama-3.1-8b-instant",
                "llama-3.2-3b-preview",
            ]
            success = False
            for m in models_to_try:
              try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    model=m,
                    temperature=0.3,
                    max_tokens=1024,
                )
                response = chat_completion.choices[0].message.content
                success = True
                break
              except Exception:
                continue

            if not success:
              response = (
                  "⚠️ هەڵە: هیچ کام لە مۆدێلەکانی گروق بەردەست نەبوون یان کلیلەکەت"
                  " کێشەی هەیە."
              )
          except Exception as e:
            response = f"⚠️ هەڵە لە پەیوەندیکردن بە سرڤەری خێرا: {e}"

        if not response:
          response = (
              "سوپاس بۆ پرسیارەکەت. تکایە دڵنیابە لەوەی کە `GROQ_API_KEY`"
              " لە بەشی Secretsی ستیریملیت داناوە."
          )

      st.markdown(response)
      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )