import streamlit as st
from utils.llm_utils import process_review_with_ai
from utils.db_utils import insert_review

# 1. Page Config
st.set_page_config(page_title="Feedback Portal", page_icon="⭐", layout="centered")

# 2. Adaptive CSS (Dark/Light Mode Support)
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
    /* Increase star size */
    button[kind="secondary"] {
        font-size: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="main-header"><h1>✨ Customer Experience Portal</h1><p>We value your voice. Help us improve!</p></div>', unsafe_allow_html=True)

# 4. The Form Card
with st.form("feedback_form"):
    st.subheader("✍️ Leave a Review")
    
    # --- CHANGED: SLIDER TO CLICKABLE STARS ---
    st.write("**How would you rate your experience?**")
    
    # st.feedback returns: 0 (1 star), 1 (2 stars) ... 4 (5 stars)
    # It returns None if the user hasn't clicked yet
    selected_stars = st.feedback("stars")
    
    st.markdown("---") # Visual separator
    
    review_text = st.text_area("Your Feedback", placeholder="Tell us what you liked or how we can improve...", height=150)
    
    # Submit Button
    submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)

# 5. Logic & Response
if submitted:
    # Validation: Check if stars are selected AND text is written
    if selected_stars is None:
        st.warning("⚠️ Please select a star rating to proceed.")
    elif not review_text.strip():
        st.warning("⚠️ Please write a short review.")
    else:
        # CONVERSION: Convert 0-index to 1-5 scale
        final_rating = selected_stars + 1
        
        with st.spinner("🤖 AI is analyzing your sentiment..."):
            # Process & Save
            user_reply, summary, actions = process_review_with_ai(final_rating, review_text)
            insert_review(final_rating, review_text, user_reply, summary, actions)
            
            # Success Animation
            st.balloons()
            
            # Styled AI Response
            st.markdown(f"""
                <div class="ai-box">
                    <h3>📨 Our Response</h3>
                    <p style="font-size: 1.1rem; font-style: italic;">"{user_reply}"</p>
                </div>
            """, unsafe_allow_html=True)
