import requests
import streamlit as st

# Set up page styling and header
st.set_page_config(page_title="Roommate Wellness Companion", page_icon="🧘")
st.title("🧘 Roommate's Wellness & Music Companion")
st.write(
    "Track sleep, calculate BMI, and get personalized music, exercise, and nutrition tips powered locally by Gemma!"
)

st.divider()

# --- INPUT SECTION ---
st.header("1. Daily Check-in")

col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox(
        "Current Mood / Energy:",
        [
            "Stressed & Overwhelmed",
            "Tired & Low Energy",
            "Anxious",
            "Focused / Studying",
            "Relaxed & Calm",
        ],
    )
    sleep_hours = st.number_input(
        "Sleep Last Night (Hours):",
        min_value=0.0,
        max_value=24.0,
        value=7.0,
        step=0.5,
    )
    sleep_quality = st.select_slider(
        "Sleep Quality:", options=["Poor", "Fair", "Good", "Great"]
    )

with col2:
    weight = st.number_input("Weight (kg):", min_value=30.0, value=70.0)
    height = st.number_input("Height (meters):", min_value=1.0, value=1.75)

    # Calculate BMI
    bmi = round(weight / (height**2), 1)
    st.metric("Calculated BMI", bmi)

st.divider()

# --- GEMMA AI GENERATION ---
st.header("2. Personalized Recommendations")

if st.button("✨ Generate AI Wellness Plan"):
    with st.spinner("Asking Gemma for personalized recommendations..."):
        # Construct prompt for Gemma
        prompt = f"""
        Act as a supportive, friendly wellness coach. Analyze this student's current status:
        - Current Mood: {mood}
        - Sleep Last Night: {sleep_hours} hours (Quality: {sleep_quality})
        - BMI: {bmi}

        Provide concise, actionable advice in 3 sections:
        1. 🎵 Music Shuffler Vibe: Suggest a specific musical vibe, genre, or mood query to listen to right now to help them relax or focus.
        2. 🧘 Quick Exercise/Relaxation Routine: Give 2 simple physical stretches or relaxation techniques tailored to their energy level and sleep status.
        3. 🥗 Nutrition Tip: Give 1 healthy snack or beverage suggestion based on their sleep recovery and BMI.
        """

        try:
            # Send prompt to local Ollama server running Gemma
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma2:2b",
                    "prompt": prompt,
                    "stream": False,
                },
            )

            result = response.json().get("response", "No response generated.")
            st.success("Plan Generated!")
            st.markdown(result)

        except Exception as e:
            st.error(
                "Could not connect to Ollama. Make sure Ollama is running in the background!"
            )