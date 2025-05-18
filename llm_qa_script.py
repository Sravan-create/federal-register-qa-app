# llm_qa_script.py
import sqlite3
import ollama
import json

def simple_qa(query):
    conn = sqlite3.connect("federal_register_documents.db")
    cursor = conn.cursor()
    
    # Basic search
    cursor.execute("""
        SELECT title, agencies_json, html_url 
        FROM documents 
        WHERE title LIKE ? 
        LIMIT 5
    """, (f"%{query}%",))
    
    results = cursor.fetchall()
    context = "\n".join([f"Title: {row[0]}\nAgencies: {json.loads(row[1])}\nURL: {row[2]}" for row in results])
    
    response = ollama.chat(
        model="qwen:1.5b",
        messages=[{
            'role': 'user', 
            'content': f"Answer this query: {query}\nUsing this context:\n{context}"
        }]
    )
    
    print("Answer:", response['message']['content'])

if __name__ == "__main__":
    question = input("Enter your question: ")
    simple_qa(question)