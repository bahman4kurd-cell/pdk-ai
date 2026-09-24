import json
import os
import streamlit as st

# هەوڵدانی هێنانی لایبرارییەی Google Generative AI
try:
  import google.generativeai as genai

  AI_AVAILABLE = True
except ImportError:
  AI_AVAILABLE = False

# ڕێکخستنی پەڕە
st.set_page_config(
    page_title="PDK AI - پلاتفۆرمی زیرەکی پارتی", page_icon="🟢", layout="centered"
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

      st.sidebar.subheader("➕ زیادکردنی زانیاری بۆ بنکەی زانیاری AI")
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

  st.sidebar.markdown("---")
  st.sidebar.title("زانیاری بەکارهێنەر")
  st.sidebar.write("👤 بەخێر هاتیت:")
  st.sidebar.code(st.session_state.user_email)

  if st.sidebar.button("دەرچوون (Logout)"):
    st.session_state.logged_in = False
    st.rerun()

  st.markdown(
      '<p class="main-title">PDK AI Assistant</p>', unsafe_allow_html=True
  )
  st.markdown(
      '<p class="subtitle">سیستەمی زیرەکی دەستکردی پێشکەوتوو بۆ لێکۆڵینەوە و'
      " وەڵامدانەوە</p>",
      unsafe_allow_html=True,
  )

  if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"سڵاو {st.session_state.user_email.split('@')[0]}! من PDK"
                " AIـم. هەر پرسیارێکت هەبێت لەسەر ئەو زانیاری و فایلانەی کە"
                " ئەپلۆد کراون، دەتوانیت بە ئازادی بینوسیت و من لێکدانەوەی"
                " بۆ دەکەم."
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
      with st.spinner("زیرەکی دەستکرد خەریکی شیکردنەوە و گەڕانە..."):
        custom_data = load_data()
        response = ""

        # ئەگەر لایبرارییەکە هەبوو و API Keyـیش بوونی هەبوو
        if AI_AVAILABLE and custom_data:
          context_text = ""
          for idx, item in enumerate(custom_data, 1):
            context_text += (
                f"\n--- سەرچاوە [{idx}]: {item.get('title')} ---\n"
                f"{item.get('content')}\n"
            )

          system_instruction = (
              "تۆ زیرەکی دەستکردێکی پسپۆڕی. ئەرکی تۆ ئەوەیە کە وەڵامی پرسیاری"
              " بەکارهێنەر بدەیتەوە تەنها و تەنها لەسەر بنەمای ئەو سەرچاوە و"
              " زانیارییانەی خوارەوە کە لەلایەن بەڕێوەبەرەوە ئەپلۆد کراون. ئەگەر"
              " وەڵامەکە لە ناو زانیارییەکاندا نەبوو، بە ڕوونی پێی بڵێ کە لە"
              " داتاکاندا بوونی نییە، وەڵامەکانت بە زمانی کوردی سۆرانی پوخت"
              " بنووسە.\n\n"
              f"زانیاری و فایلە ئەپلۆدکراوەکان:\n{context_text}"
          )

          try:
            # ئەگەر مۆدێلەکەی کار پێکرد
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction,
            )
            chat = model.start_chat(history=[])
            ai_response = chat.send_message(prompt)
            response = ai_response.text
          except Exception:
            response = ""

        # ئەگەر AI بەردەست نەبوو یان API Key نەبوو، گەڕانی زیرەک بەکاربهێنە وەکو فۆڵباک
        if not response:
          matched = False
          if custom_data:
            prompt_lower = prompt.lower()
            for item in custom_data:
              # گەڕانی سادەی ورد لەناو دەقەکاندا بۆ دڵنیابوون لە وەڵام
              if any(
                  w in item.get("content", "").lower()
                  for w in prompt_lower.split()
                  if len(w) > 2
              ):
                response = (
                    f"📌 **{item.get('title')}**\n\n{item.get('content')}"
                )
                matched = True
                break

          if not matched:
            response = (
                "سوپاس بۆ پرسیارەکەت. لەناو داتاکاندا زانیاری پێویست نەدۆزراوەتەوە"
                " یان پێویستە فایلی `requirements.txt` ڕێکبخەیت بۆ کارپێکردنی"
                " تەواوی AI."
            )

      st.markdown(response)
      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )