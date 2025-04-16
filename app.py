import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from deepface import DeepFace
import google.generativeai as genai
import os

# 🔑 Paste your Gemini API Key here
genai.configure(api_key="AIzaSyBAOXJx9sff6H5cISIx0Ucuf1KytPOqOZk")  # <-- Replace this line

st.set_page_config(page_title="Emoji GIF Generator")
st.title("🎭 Photo + Mood → Emoji GIF")

# 🧠 Get emoji using Gemini AI
def get_prompt_emoji(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"Give only ONE emoji that fits this mood: '{prompt}'. Respond with just the emoji."
        )
        return response.text.strip()
    except:
        return "🙂"

# 😊 Detect facial emotion from photo
def get_face_emotion(path):
    try:
        analysis = DeepFace.analyze(img_path=path, actions=['emotion'], enforce_detection=False)
        return analysis[0]['dominant_emotion']
    except:
        return "neutral"

# 🌀 Create animated GIF from emoji
def create_gif(emoji):
    frames = []
    for i in range(6):  # simple bounce effect
        img = Image.new("RGB", (300, 300), color="white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()
        y = 90 - (i % 2) * 10
        draw.text((100, y), emoji, font=font, fill="black")
        frames.append(img)

    gif_path = "emoji.gif"
    frames[0].save(gif_path, format="GIF", save_all=True,
                   append_images=frames[1:], duration=300, loop=0)
    return gif_path

# 📥 UI Inputs
prompt = st.text_input("🗨️ What's your mood or feeling?")
uploaded_file = st.file_uploader("📸 Upload your face photo", type=["jpg", "jpeg", "png"])

# 🎬 When inputs are ready
if prompt and uploaded_file:
    with open("face.jpg", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Analyzing your vibe..."):
        emotion = get_face_emotion("face.jpg")
        combo_text = f"{prompt} while looking {emotion}"
        emoji = get_prompt_emoji(combo_text)
        gif_path = create_gif(emoji)

    st.success(f"🎉 Here's your emoji: {emoji}")
    st.image(gif_path, caption="🌀 Your Emoji GIF!", use_column_width=False)

    with open(gif_path, "rb") as gif_file:
        st.download_button("⬇ Download GIF", gif_file, file_name="emoji.gif")
