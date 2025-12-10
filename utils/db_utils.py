import psycopg2
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local dev)
load_dotenv()

def get_connection():
    """
    Connects to the database using os.getenv variables.
    """
    try:
        connection = psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname")
        )
        return connection
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

def insert_review(rating, review_text, ai_response, ai_summary, ai_actions):
    """Inserts a new review into the database."""
    conn = get_connection()
    if conn is None: return

    try:
        cur = conn.cursor()
        query = """
            INSERT INTO reviews (rating, review_text, ai_response, ai_summary, ai_actions)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (rating, review_text, ai_response, ai_summary, ai_actions))
        conn.commit()
        cur.close()
    except Exception as e:
        st.error(f"❌ Failed to save review: {e}")
    finally:
        conn.close()

def fetch_all_reviews():
    """Fetches all reviews from the database."""
    conn = get_connection()
    if conn is None: return pd.DataFrame()

    try:
        cur = conn.cursor()
        query = "SELECT * FROM reviews ORDER BY created_at DESC"
        cur.execute(query)
        
        # Manually create DataFrame to avoid warnings
        data = cur.fetchall()
        if data:
            colnames = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=colnames)
        else:
            df = pd.DataFrame()
            
        cur.close()
        return df
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()