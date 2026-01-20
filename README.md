🌱 Student Wellness Companion



An empathetic, AI-powered Streamlit application designed to support students' mental health and productivity. The app combines LLaMA 3-8B intelligence with mood tracking, journaling, and a reward system to help students navigate academic stress.
✨ Key Features
🎭 Dynamic Mood Tracking: A sidebar emoji-based tracker that adapts the AI's personality and recommendations based on how the student feels.
💬 Empathetic Chatbot: Powered by Meta-Llama-3-8B, the bot uses reflective listening and grounding techniques to provide support.
📝 Private Journaling: A dedicated space for students to reflect on their day and store thoughts locally within the session.
🌟 Gamified Goals: A "Wellness Goals" progress bar that rewards students with stars for checking in and journaling.
💡 Smart Resource Library: Context-aware recommendations that suggest specific videos (Grounding, Burnout, Focus) based on chat keywords.
✨ Daily Mantras: Automated, mood-specific "I am" affirmations generated via AI.


🚀 Tech Stack
Frontend: Streamlit
AI Model: Meta-Llama-3-8B-Instruct (via Hugging Face Inference API)
Language: Python 3.x
Libraries: huggingface_hub, re, os
🛠️ Setup Instructions
1. Prerequisites
A Hugging Face account and an Access Token.
Python installed on your machine.
2. Installation
Clone the repository and install the requirements
it clone https://github.com/yourusername/wellness-companion.git
cd wellness-companion
pip install streamlit huggingface_hub
3. Configuration
Create a .streamlit/secrets.toml file in your project root to store your API key:
HF_TOKEN = "your_hugging_face_token_here"
4. Run the App
 streamlit run app.py

🧠 System Logic
Safety First: The app includes a check_safety helper function to identify distressed keywords and ensure a safe environment.
Prompt Engineering: Custom system prompts ensure the AI uses bolding for encouragement and always ends with a supportive question
