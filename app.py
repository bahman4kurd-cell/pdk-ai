import os
import streamlit as st
from groq import Groq

# تێستکردنی ڕاستەوخۆی کلیل
try:
  api_key = st.secrets["GROQ_API_KEY"]
  client = Groq(api_key=api_key)

  # داواکاری تێست
  chat_completion = client.chat.completions.create(
      messages=[{"role": "user", "content": "Hi"}],
      model="llama-3.1-8b-instant",
  )
  st.success("✅ کلیلەکەت کار دەکات و کێشەی نییە!")
  st.write(chat_completion.choices[0].message.content)

except Exception as e:
  st.error(f"❌ کێشەی ڕاستەقینە ئەمەیە: {e}")