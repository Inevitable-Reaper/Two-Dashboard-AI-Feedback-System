import google.generativeai as genai
import streamlit as st
import json
import re

# Configure API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def process_review_with_ai(rating, review_text):
    """
    Sends review to Gemini and returns structured data.
    Includes robust error handling and safety setting overrides.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a customer experience AI. A user submitted this feedback:
    Rating: {rating}/5 Stars
    Review: "{review_text}"

    Generate a valid JSON object with exactly these three keys:
    1. "user_reply": A short, empathetic response for the user. (Apologetic for low stars, grateful for high).
    2. "admin_summary": A 1-sentence summary for the admin.
    3. "recommended_actions": A short string listing 1-2 actions the business should take.

    Output ONLY raw JSON. No markdown formatting.
    """

    # 1. Configure Safety Settings to allow negative feedback processing
    # (Without this, words like "pathetic" or "shit" trigger a block)
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    try:
        # 2. Generate Content
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        # Check if the response was blocked
        if not response.parts:
            print("❌ GEMINI BLOCKED THE RESPONSE due to safety filters.")
            return "We appreciate your feedback.", "Content blocked by safety filters.", "Review manually."

        text = response.text.strip()
        
        # 3. Robust JSON Extraction (Finds the first '{' and last '}')
        # This fixes issues where the LLM adds "Here is the JSON..."
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data.get("user_reply"), data.get("admin_summary"), data.get("recommended_actions")
        else:
            print(f"❌ JSON PARSING ERROR. Raw Text received:\n{text}")
            return "Thank you for your feedback.", "Error parsing AI response.", "Check logs."

    except Exception as e:
        # 4. Print the exact error to your VS Code terminal for debugging
        print(f"❌ SYSTEM ERROR: {str(e)}")
        return "Thank you for your feedback.", "System Error.", "Check logs."