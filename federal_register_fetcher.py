# federal_register_fetcher.py
import requests
import sqlite3
from datetime import date
import json

BASE_API_URL = "https://www.federalregister.gov/api/v1/documents.json"
DATABASE_NAME = "federal_register_documents.db"
START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 4, 30)

def initialize_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            document_number TEXT PRIMARY KEY,
            title TEXT,
            type TEXT,
            publication_date TEXT,
            html_url TEXT,
            pdf_url TEXT,
            agencies_json TEXT,
            citation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_documents():
    initialize_db()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    page = 1
    while True:
        params = {
            "conditions[publication_date][gte]": START_DATE.isoformat(),
            "conditions[publication_date][lte]": END_DATE.isoformat(),
            "page": page,
            "per_page": 100
        }
        
        try:
            response = requests.get(BASE_API_URL, params=params)
            data = response.json()
            
            if not data.get('results'):
                break
                
            for doc in data['results']:
                agencies_json = json.dumps(doc.get('agencies', []))
                cursor.execute('''
                    INSERT OR IGNORE INTO documents VALUES (?,?,?,?,?,?,?,?)
                ''', (
                    doc['document_number'],
                    doc['title'],
                    doc['type'],
                    doc['publication_date'],
                    doc['html_url'],
                    doc.get('pdf_url', ''),
                    agencies_json,
                    doc.get('citation', '')
                ))
                
            conn.commit()
            page += 1
            
        except Exception as e:
            print(f"Error: {e}")
            break
            
    conn.close()

if __name__ == "__main__":
    print("Fetching documents...")
    fetch_documents()