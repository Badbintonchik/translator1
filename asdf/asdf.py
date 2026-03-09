import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Echo-Translate AI", page_icon="🌐")

st.title("🌐 Echo-Translate: Global Edition")

# Dil Sözlüğü (Deep Translator formatına uygun)
LANGUAGES = {
    "Turkish 🇹🇷": "tr",
    "English 🇺🇸": "en",
    "German 🇩🇪": "de",
    "French 🇫🇷": "fr",
    "Spanish 🇪🇸": "es",
    "Italian 🇮🇹": "it",
    "Russian 🇷🇺": "ru",
    "Arabic 🇸🇦": "ar",
    "Japanese 🇯🇵": "ja"
}

# Yan Menü
st.sidebar.header("⚙️ Ayarlar")
src_lang_name = st.sidebar.selectbox("Konuşacağınız Dil:", list(LANGUAGES.keys()), index=0)
target_lang_name = st.sidebar.selectbox("Hedef Dil:", list(LANGUAGES.keys()), index=1)

src_code = LANGUAGES[src_lang_name]
target_code = LANGUAGES[target_lang_name]

def translate_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"🎙️ {src_lang_name} dinleniyor...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    
    try:
        # 1. Sesi Metne Çevir (Speech to Text)
        # Google STT için dil kodları tr-TR, en-US şeklindedir
        stt_code = f"{src_code}-{src_code.upper()}" if src_code != "en" else "en-US"
        text = r.recognize_google(audio, language=stt_code)
        st.success(f"**Söylenen:** {text}")

        # 2. Tercüme Et (Deep Translator - Stabil Versiyon)
        translated_text = GoogleTranslator(source='auto', target=target_code).translate(text)
        st.info(f"**Çeviri ({target_lang_name}):** {translated_text}")

        # 3. Metni Sese Çevir (TTS)
        tts = gTTS(text=translated_text, lang=target_code)
        tts.save("output.mp3")

        # 4. Oynat
        st.audio("output.mp3", format="audio/mp3")
        
    except Exception as e:
        st.error(f"Hata oluştu: {e}")

if st.button("🎤 Çeviriye Başla", use_container_width=True):
    translate_audio()