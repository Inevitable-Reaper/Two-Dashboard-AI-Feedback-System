import streamlit as st
from utils.llm_utils import process_review_with_ai
from utils.db_utils import insert_review

st.set_page_config(page_title="Feedback Portal", page_icon="⭐", layout="centered")

# Adaptive CSS (Dark/Light Mode Support)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stForm {
        background-color: var(--secondary-background-color);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .ai-box {
        background-color: rgba(33, 150, 243, 0.1);
        border-left: 5px solid #2196f3;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
    }
    .ai-box h3, .ai-box p {
        color: var(--text-color);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>✨ Customer Experience Portal</h1><p>We value your voice. Help us improve!</p></div>', unsafe_allow_html=True)

with st.form("feedback_form"):
    st.subheader("✍️ Leave a Review")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("**Rate us:**")
    with col2:
        rating = st.slider("Stars", 1, 5, 5, label_visibility="collapsed")

    review_text = st.text_area("Your Feedback", placeholder="Tell us about your experience...", height=150)
    
    submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)

if submitted:
    if not review_text.strip():
        st.warning("⚠️ Please write a review before submitting.")
    else:
        with st.spinner("🤖 AI is analyzing your sentiment..."):
            user_reply, summary, actions = process_review_with_ai(rating, review_text)
            
            # This now saves to CSV
            insert_review(rating, review_text, user_reply, summary, actions)
            
            st.balloons()
            st.markdown(f"""
                <div class="ai-box">
                    <h3>📨 Our Response</h3>
                    <p style="font-size: 1.1rem; font-style: italic;">"{user_reply}"</p>
                </div>
            """, unsafe_allow_html=True)