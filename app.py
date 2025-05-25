import streamlit as st
import ollama
import datetime
import pandas as pd

st.set_page_config(page_title="WellBeing", page_icon=":robot_face:", layout="wide")

background_image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(50, 50, 50, 0.8);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);

        }}
    </style>
""", unsafe_allow_html=True)

st.session_state.setdefault('messages_history', [])
st.session_state.setdefault('mood_log', [])

def responses(user_input):
    st.session_state['messages_history'].append({"role": "user", "content": user_input})


    response = ollama.chat(model="llama3", messages=st.session_state['messages_history'])

    ai_reply = response['message']['content']

    st.session_state['messages_history'].append({"role": "assistant", "content": ai_reply})
    return ai_reply

def affirmations():
    prompt = "Generate a random positive affirmation for mental well-being, someone stressed or overwhelmed."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def meditation():
    prompt = "Generate a random meditation script for relaxation and stress relief."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


st.title("WellBeing")
st.markdown("Hi! I'm **WellBeing**, your personal mental health assistant")

if st.checkbox("Show instructions"):
    st.info("""
    - Type your health questions and press Enter  
    - Or use the buttons for quick affirmations and meditation  
    - Powered by a local AI model for privacy and speed  
    """)

for message in st.session_state['messages_history']:
    role = "You" if message['role'] == 'user' else "WellBeing"
    st.markdown(f"**{role}:** {message['content']}")


user_text = st.text_input("How can I help you today?")
if user_text:
    with st.spinner("Waiting for WellBeing..."):
        ai_reply = responses(user_text)
        st.markdown(f"**WellBeing:** {ai_reply}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Positive Affirmations"):
        with st.spinner("Curating positive affirmations..."):
            affirmation = affirmations()
            st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Meditate"):
        with st.spinner("Designing meditation routine..."):
            meditation_script = meditation()
            st.markdown(f"**Meditation Script:** {meditation_script}")

col3, col4 = st.columns(2)

with col3:
    if st.button("Mental Health Tips"):
        with st.spinner("Gathering mental health tips..."):
            tips = responses("Give me practical tips for maintaining good mental health.")
            st.markdown(f"**Mental Health Tips:** {tips}")

with col4:
    if st.button("Stress & Anxiety Help"):
        with st.spinner("Providing advice on stress and anxiety..."):
            advice = responses("How can someone manage stress and anxiety effectively?")
            st.markdown(f"**Stress & Anxiety Help:** {advice}")

st.subheader("Daily Mood Tracker")
mood_today = st.slider("How are you feeling today?", 0, 10, 5)
if st.button("Log Mood"):
    st.session_state['mood_log'].append({"date": datetime.date.today(), "mood": mood_today})
    st.success("Mood logged!")

if st.session_state['mood_log']:
    mood_df = pd.DataFrame(st.session_state['mood_log'])
    mood_df = mood_df.drop_duplicates(subset="date", keep="last")
    mood_df.set_index("date", inplace=True)
    st.line_chart(mood_df)

st.subheader("Mental Health Resources")
st.markdown("""
- [Mind (UK)](https://www.mind.org.uk/)
- [Mental Health America](https://www.mhanational.org/)
- [WHO Mental Health](https://www.who.int/mental_health/en/)
- [NHS Every Mind Matters](https://www.nhs.uk/every-mind-matters/)
""")