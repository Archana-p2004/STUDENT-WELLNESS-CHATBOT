import os
import streamlit as st
from huggingface_hub import InferenceClient
HF_TOKEN = st.secrets["HF_TOKEN"]
Client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=HF_TOKEN)


# A library of helpful resources mapped to student needs
RESOURCES = {
    "anxiety": {
        "title": "5-Minute Grounding Exercise",
        "video": "https://www.youtube.com/watch?v=m3-O7gPsQK0",
        "tip": "Focus on 5 things you can see, 4 you can touch, and 3 you can hear."
    },
    "burnout": {
        "title": "The Power of Rest",
        "video": "https://www.youtube.com/watch?v=gJ5fX86-TTE",
        "tip": "Academic success is a marathon, not a sprint. It's okay to recharge."
    },
    "focus": {
        "title": "Study with Me (Pomodoro)",
        "video": "https://www.youtube.com/watch?v=tndzLznGjaU",
        "tip": "Try the 25/5 rule: Work for 25 minutes, then rest for 5."
    }
}
# --- 3. HELPER FUNCTIONS (NEW & IMPROVED) ---
def check_safety(text):
    """Checks for distressed keywords."""
    risk_keywords = ["hurt myself", "suicide", "end it all", "hopeless", "self-harm"]
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    return any(word in clean_text for word in risk_keywords)

def get_smart_recommendation(text, mood):
    """Suggests a video resource based on keywords."""
    text = text.lower()
    if "exam" in text or "anxious" in text or mood == "😟 Sad":
        return RESOURCES["anxiety"]
    elif "tired" in text or "burnout" in text or mood == "😡 Angry":
        return RESOURCES["burnout"]
    return None

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"
# --- INITIALIZE REWARDS ---
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "daily_tasks" not in st.session_state:
    st.session_state.daily_tasks = {"chat": False, "journal": False}
# Sidebar: Emoji Mood Tracker
st.sidebar.header("🗨️ Mood Tracker")
mood = st.sidebar.radio("How are you feeling today?", ["🙂 Normal", "😟 Sad", "😡 Angry", "😌 Calm", "😕 Upset", "😎 Cool"])
st.session_state.mood = mood
st.sidebar.write(f"Selected mood: {mood}")
def generate_affirmation(mood):
    # A focused prompt for a short, punchy affirmation
    prompt = f"<|system|>\nTechnical Rule: Respond with ONLY one sentence. Do not say 'Here is your affirmation'.\n<|user|>\nGenerate a powerful 'I am' affirmation for a student feeling {mood}.<|assistant|>\n"
    
    try:
        # Using the same client you already initialized
        response = Client.text_generation(prompt, max_new_tokens=50, temperature=0.6)
        return response.strip().replace('"', '')
    except:
        return "I am capable of handling whatever today brings."
    st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Wellness Goals")

# Progress calculation
completed = sum(st.session_state.daily_tasks.values())
total_tasks = len(st.session_state.daily_tasks)
progress = completed / total_tasks

st.sidebar.progress(progress)
st.sidebar.write(f"Stars Earned: {st.session_state.stars} ⭐")

if completed == total_tasks:
    st.sidebar.success("Daily Goals Complete! 🎉")
else:
    st.sidebar.info(f"Complete {total_tasks - completed} more task(s) to earn a star!")

# --- Displaying it in the UI ---
st.markdown("---")
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("✨ New Affirmation") # Clicking this refreshes the app and generates a new one
    with col2:
        current_affirmation = generate_affirmation(st.session_state.mood)
        st.info(f"**Your Daily Mantra:** \n\n *{current_affirmation}*")
        


# Tabs for Chat and Journaling
tab1, tab2 = st.tabs(["💬 Chat", "📝 Journal"])

# LLaMA response function with follow-up
def get_wellness_response(user_message, mood):
    # 1. Logic to select the strategy based on mood
    if mood in ["😡 Angry", "😟 Sad", "😕 Upset"]:
        strategy = "Focus on grounding exercises (like breathing) and physical calm. Be very gentle."
    elif mood in ["😌 Calm", "😎 Cool"]:
        strategy = "Focus on gratitude, reflection, and maintaining this positive momentum."
    else:
        strategy = "Focus on active listening. Use 'Reflective Listening' to validate their feelings."

    # 2. Build the dynamic system prompt
    system_prompt = (
    f"You are a compassionate wellness coach. The student is {mood}. "
    "Rules for interaction:\n"
    "1. Use **bolding** for encouraging words.\n"
    "2. Use bullet points if giving more than two suggestions.\n"
    "3. Keep responses under 3 paragraphs to avoid overwhelming the student.\n"
    "4. Always end with a question that starts with 'How' or 'What'."
)
    
    # 3. Formulate the prompt for Llama 3
    full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_message}\n<|assistant|>\n"
    response = Client.text_generation(full_prompt, max_new_tokens=300, temperature=0.7)
    return response.strip()

# 💬 Chat Tab
with tab1:
    st.title("🌱 Student Wellness Chatbot")
    st.markdown("Type how you're feeling. I'm here to support you with empathy and encouragement.")
    
    user_input = st.text_area("💭 What's on your mind?", placeholder="e.g., I feel anxious about my exams...")
    
    if st.button("Send", key="chat_send"):
        if user_input:
            with st.spinner("Thinking with empathy..."):
                bot_response = get_wellness_response(user_input, st.session_state.mood)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", bot_response))
                if not st.session_state.daily_tasks["chat"]:
                    st.session_state.daily_tasks["chat"] = True
                    st.session_state.stars += 1
                    st.toast("You earned a star for checking in! ⭐")
# SMART RECOMMENDATION DISPLAY (NEW)
    rec = get_smart_recommendation(user_input, st.session_state.mood)
    if rec and user_input:
        with st.expander(f"💡 Resource for you: {rec['title']}", expanded=True):
            st.write(f"*{rec['tip']}*")
            st.video(rec['video'])
# Display chat history

# Display chat history with modern chat bubbles
for sender, message in st.session_state.chat_history:
    if sender == "You":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant", avatar="🌱"):
            st.write(message)

# Journal Tab
with tab2:
    st.title("📄 Personal Journal")
    st.markdown("Write freely about your thoughts. This is just for you.")

    journal_input = st.text_area("Today's reflection", placeholder="Write anything you want to reflect on..")

    if st.button("Save Entry", key="journal_save"):
        if journal_input:
            st.session_state.journal_entries.append(journal_input)
            st.success("Journal entry saved!")

    if st.session_state.journal_entries:
        st.markdown("### 📋 Your Entries")
        for i, entry in enumerate(st.session_state.journal_entries, 1):
            st.markdown(f"*Entry {i}:* {entry}")
            if not st.session_state.daily_tasks["journal"]:
                st.session_state.daily_tasks["journal"] = True
                st.session_state.stars += 1
                st.toast("Journal goal complete! ⭐")
