# 🚀 Two-Dashboard AI Feedback System



This repository contains the source code for a dual-dashboard web application designed to collect, process, and analyze customer feedback using Large Language Models (LLMs). The system consists of a public-facing **User Dashboard** for submitting reviews and an internal **Admin Dashboard** for monitoring feedback and AI-generated insights.

**🔗 Live Demo:** (https://two-dashboard-ai-feedback-system-tq6cwbfhsrrc7hqcnptj9a.streamlit.app/)

---

## 📋 Project Overview

The goal of this project is to build a "Two-Dashboard AI Feedback System" that reads and writes from a shared data source.

### **1. User Dashboard (Public)**
* **Functionality:** Allows users to select a star rating (1-5) and write a text review.
* **AI Integration:** Upon submission, the system uses Google Gemini AI to generate a personalized, empathetic response instantly displayed to the user.
* **Data Storage:** Saves the rating, review, and AI metadata to a cloud database (Supabase).

### **2. Admin Dashboard (Internal)**
* **Functionality:** Displays a live feed of all submissions.
* **AI Insights:** For every review, the AI generates a concise **Summary** and **Recommended Action Items** for the business.
* **Analytics:** Includes metrics for Total Reviews, Average Rating, and Critical Issues count.

---

## 🛠️ Tech Stack

* **Frontend/Backend Framework:** [Streamlit](https://streamlit.io/) (Python) 
* **AI Model:** Google Gemini API (`gemini-2.5-flash`) 
* **Database:** Supabase (PostgreSQL) - *Cloud-hosted for persistence* 
* **Libraries:** `google-generativeai`, `pandas`, `psycopg2-binary`, `python-dotenv`

---

## 📂 Repository Structure

```text
fynd-feedback-app/
├── .streamlit/
│   └── secrets.toml      # (Ignored by Git) Stores API keys & DB credentials
├── pages/
│   └── Admin_Dashboard.py # The Internal Analytics Dashboard
├── utils/
│   ├── __init__.py
│   ├── db_utils.py       # Handles Supabase connection (Read/Write)
│   ├── llm_utils.py      # Handles Gemini AI Prompting & Response Parsing
├── User_Dashboard.py     # Main Entry Point (Public Form)
├── requirements.txt      # Project Dependencies
└── README.md             # Documentation
