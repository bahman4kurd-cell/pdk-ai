import json
import os
import streamlit as st

# ڕێکخستنی پەڕە
st.set_page_config(
    page_title="PDK AI - پلاتفۆرمی زیرەکی پارتی", page_icon="🟢", layout="centered"
)

# ناوی فایلی پاشەکەوتکردنی زانیارییەکان
DATA_FILE = "pdk_knowledge.json"


# خوێندنەوەی داتاکان
def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


# پاشەکەوتکردنی داتای نوێ لەلایەن ئەدەمینەوە
def save_data(data_list):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)


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

# سیستەمی چوونەژوورەوەی سادە بۆ پاراستنی ئەپەکە
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
  # پەنڵی ئەدەمین لە Sidebar
  st.sidebar.title("🎛️ کۆنترۆڵی ئەدەمین")
  admin_mode = st.sidebar.checkbox("دۆخی بەڕێوەبەر (Admin Mode)")

  if admin_mode:
    admin_pass = st.sidebar.text_input("پاسوۆردی ئەدەمین:", type="password")
    if admin_pass == "1234":  # لێرە دەتوانیت پاسوۆردی خۆت بگۆڕیت
      st.sidebar.success("بە سەرکەوتوویی چوویە ژوورەوە وەک ئەدەمین!")

      st.sidebar.subheader(
          "➕ زیادکردنی زانیاری بۆ بنکەی زانیاری PDK AI"
      )
      with st.sidebar.form("add_knowledge_form"):
        title = st.text_input(
            "عنوان یان بابەتی زانیاریەکە (بۆ نموونە: کۆنگرەی یەکەم):"
        )
        content = st.text_area("دەق یان زانیاری ورد لەسەر بابەتەکە:")
        submitted = st.form_submit_button("زانیاریەکە پاشەکەوت بکە")

        if submitted and title and content:
          data = load_data()
          data.append({"title": title, "content": content})
          save_data(data)
          st.sidebar.success(
              "زانیاریەکە بە سەرکەوتوویی زیاد کرا بۆ بنکەی زانیاری!"
          )
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

    # وەڵامدانی زیرەکانە و گەڕان لە ناو داتای زیادکراوی ئەدەمین
    with st.chat_message("assistant"):
      prompt_lower = prompt.lower()
      custom_data = load_data()

      # پشکنین ئایا پرسیارەکە پەیوەندی بەو زانیارییانەوە هەیە کە تۆ وەک ئەدەمین زیادیکردوون
      matched_content = None
      for item in custom_data:
        if (
            item["title"].lower() in prompt_lower
            or prompt_lower in item["title"].lower()
        ):
          matched_content = item["content"]
          break

      if matched_content:
        response = (
            f"**زانیاری فەرمی لە بنکەی زانیاری ئەدەمینەوە:**\n\n"
            f"{matched_content}"
        )
      elif "مێژوو" in prompt_lower or "دامەزراندن" in prompt_lower:
        response = (
            "پارتی دیموکراتی کوردستان لە 16ـی ئابی 1946 بە سەرۆکایەتی نەمر مەلا"
            " مستەفا بارزانی دامەزرا، وەک یەکەم حیزبی نیشتمانی خاوەن خەبات"
            " لە مێژووی هاوچەرخی کوردستاندا."
        )
      elif "مەکتەبی سیاسی" in prompt_lower:
        response = (
            "مەکتەبی سیاسی یەکێکە لە ئۆرگانە باڵاکانی سەرکردایەتی پارتیدا کە لە"
            " نێوان دوو کۆنگرەدا بەرپرسیارە لە جێبەجێکردنی بڕیارە سیاسی و"
            " سازمانداییەکان."
        )
      else:
        response = (
            f"سوپاس بۆ پرسیارەکەت دەربارەی ({prompt}). ئەی ئایەکەی ئێمە لە"
            " هەوڵی بەردەوامدایە بۆ پێشکەشکردنی وردترین زانیاری مێژوویی و"
            " سازمانی دەربارەی پارتی."
        )

      st.markdown(response)
      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )