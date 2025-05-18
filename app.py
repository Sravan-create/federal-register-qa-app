# app.py
import streamlit as st
import sqlite3
import ollama
import json
import textwrap
import os

DATABASE_NAME = "federal_register_documents.db"
OLLAMA_MODEL = "qwen2:1.5b"
MAX_DOCS_FOR_LLM = 880000
SUMMARIZE_CONTENT_LENGTH = 500

def get_db_connection():
    if not os.path.exists(DATABASE_NAME):
        st.error(f"Database not found at: {os.path.abspath(DATABASE_NAME)}")
        return None
        
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

def fetch_relevant_documents(query):
    keywords = [word.lower() for word in query.split() if len(word) > 2]
    if not keywords:
        return []
    
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        conditions = []
        params = []
        
        for keyword in keywords:
            term = f"%{keyword}%"
            conditions.append("(title LIKE ? OR agencies_json LIKE ?)")
            params.extend([term, term])
        
        query_sql = f"""
            SELECT document_number, title, type, publication_date, 
                   html_url, agencies_json
            FROM documents
            WHERE {" OR ".join(conditions)}
            ORDER BY publication_date DESC
            LIMIT ?
        """
        cursor.execute(query_sql, params + [MAX_DOCS_FOR_LLM])
        
        documents = []
        for row in cursor.fetchall():
            doc = dict(row)
            if doc['agencies_json']:
                try:
                    doc['agencies'] = json.loads(doc['agencies_json'])
                except json.JSONDecodeError:
                    doc['agencies'] = []
            del doc['agencies_json']
            documents.append(doc)
            
        return documents
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []
    finally:
        conn.close()

def format_documents_for_llm(documents):
    if not documents:
        return "No relevant documents found."
    
    formatted = []
    for i, doc in enumerate(documents, 1):
        agencies = ", ".join([a.get('name', '') for a in doc.get('agencies', [])])
        formatted.append(f"""
--- Document {i} ---
Title: {textwrap.shorten(doc.get('title', ''), width=SUMMARIZE_CONTENT_LENGTH, placeholder='...')}
Date: {doc.get('publication_date', 'N/A')}
Agencies: {agencies if agencies else 'N/A'}
URL: {doc.get('html_url', 'N/A')}
""")
    return "\n".join(formatted)

def get_polished_answer(query, context):
    system_prompt = f"""
    Analyze these documents for: {query}
    Only use information from below documents:
    {context}
    """
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': query}
            ],
            options={'temperature': 0.1}
        )
        return response['message']['content']
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Federal Register Q&A")
st.title("Federal Register Document Q&A System")

query = st.text_input("Enter your question:", placeholder="e.g. EPA regulations")
if st.button("Search"):
    if not query:
        st.warning("Please enter a question")
    else:
        with st.spinner("Searching..."):
            docs = fetch_relevant_documents(query)
            
        if not docs:
            st.warning("No matching documents found")
        else:
            context = format_documents_for_llm(docs)
            with st.spinner("Analyzing..."):
                answer = get_polished_answer(query, context)
                
            st.subheader("Answer:")
            st.write(answer)
            with st.expander("View documents"):
                st.write(context)