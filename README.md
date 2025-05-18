## 📄 `README.md`

```markdown
# 🧠 Federal Register Q&A App

A Streamlit-powered web application that leverages a locally running Qwen-1.5B LLM (via Ollama) to answer user queries about U.S. Federal Register documents. It retrieves relevant entries from a local SQLite database and generates context-aware responses using natural language prompts.

---

## 🚀 Features

- 🔍 Ask natural language questions about U.S. government regulations and publications
- 🧠 Uses Ollama + Qwen-1.5B model to generate smart, relevant answers
- 📚 Searches from a local SQLite database of official Federal Register documents
- 🌐 Streamlit-based interactive UI
- 📎 Links to original publication sources included

---

## 📁 Project Structure

```

federal-register-qa-app/
├── app.py                     # Main Streamlit app
├── llm\_qa\_script.py           # Command-line version for quick testing
├── federal\_register\_fetcher.py# Script to fetch data from Federal Register API
├── README.md                  # Project documentation

````

---

## 🛠️ Getting Started

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Sravan-create/federal-register-qa-app.git
   cd federal-register-qa-app
````

2. **Install dependencies**:
   Use your preferred method (`pip`, virtual environment, etc.).

3. **Pull the LLM model via Ollama**:

   ```bash
   ollama pull qwen:1.5b
   ```

4. **Fetch the documents**:

   ```bash
   python federal_register_fetcher.py
   ```

5. **Run the app**:

   ```bash
   streamlit run app.py
   ```

---

## 🌐 Want to Deploy?

You can deploy this app using [Streamlit Cloud](https://streamlit.io/cloud). Just:

* Push your code to GitHub
* Link the repo on Streamlit Cloud
* Choose `app.py` as the main entry file
* Share your public app URL!

---

## 📘 Example Use Case

> *"What new EPA rules were announced in 2024?"*

The app will:

* Search the Federal Register database
* Summarize relevant documents
* Output a clean, readable answer with links

---

## 📄 License

MIT License — use it freely and modify as needed.
