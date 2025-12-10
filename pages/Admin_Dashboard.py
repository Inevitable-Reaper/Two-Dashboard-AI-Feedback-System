import streamlit as st
import pandas as pd
from utils.db_utils import fetch_all_reviews

st.set_page_config(page_title="Admin Dashboard", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .action-item {
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 5px;
        background-color: rgba(255, 193, 7, 0.15);
        color: var(--text-color);
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Executive Insights Dashboard")
st.markdown("---")

if st.button("🔄 Refresh Data"):
    st.rerun()

# This now pulls from CSV
df = fetch_all_reviews()

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", len(df))
    with col2:
        avg_rating = df['rating'].mean()
        delta_color = "normal" if avg_rating >= 4 else "inverse"
        st.metric("Average Rating", f"{avg_rating:.1f} ⭐", delta_color=delta_color)
    with col3:
        negative_reviews = len(df[df['rating'] <= 2])
        st.metric("Critical Issues", negative_reviews, delta=f"{negative_reviews} Needs Action", delta_color="inverse")
    with col4:
         # Ensure datetime is formatted for display
         latest_date = df['created_at'].iloc[0]
         st.metric("Latest", latest_date.strftime('%b %d, %H:%M'))

    st.markdown("###")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📈 Rating Distribution")
        rating_counts = df['rating'].value_counts().reindex([1,2,3,4,5], fill_value=0)
        st.bar_chart(rating_counts, color="#764ba2")
    
    with c2:
        st.subheader("⚡ Strategic Actions")
        recent_actions = df[['ai_actions']].head(3)
        for act in recent_actions['ai_actions']:
            st.markdown(f'<div class="action-item">🔹 {act}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📝 Live Feed")
    
    display_df = df[['rating', 'review_text', 'ai_summary', 'ai_actions', 'created_at']]
    
    st.dataframe(
        display_df,
        column_config={
            "rating": st.column_config.NumberColumn("Stars", format="%d ⭐"),
            "review_text": st.column_config.TextColumn("Customer Review", width="large"),
            "ai_summary": "AI Summary",
            "ai_actions": "Recommended Actions",
            "created_at": st.column_config.DatetimeColumn("Timestamp", format="D MMM, h:mm a")
        },
        width="stretch",
        hide_index=True
    )
else:
    st.info("ℹ️ No data available. Waiting for submissions...")
