# 📚 AI Study Assistant

A clean and secure Streamlit web application that transforms study notes and textbooks (PDFs) into structured summaries, interactive flashcards, and multiple-choice quizzes using Groq's high-performance `llama-3.1-8b-instant` model.

## 🚀 Features

- **PDF Text Extraction:** Seamlessly extracts text from uploaded PDF study materials using `pypdf`.
- **Groq-Powered Intelligence:** Uses the lightning-fast `qwen/qwen3.8-27b` model through the official Groq SDK for rapid content generation.
- **Multi-Tab Study Suite:**
  - **Summary:** Generates concise, bullet-point summaries with a one-click download option.
  - **Flashcards:** Creates expandable question-and-answer flashcards for active recall.
  - **Interactive Quiz:** Generates multiple-choice questions with instant scoring, feedback, and explanations.
- **Secure API Key Handling:** Allows users to enter their Groq API key directly into the sidebar using session storage for privacy. No `.env` file is required.

---

## 🛠️ Installation & Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

Open your terminal and execute the following commands:

```bash
git clone https://github.com/akshh-bot/AI_Study_Assistant.git
cd AI_Study_Assistant
```

### 2. Create a Virtual Environment (Recommended)

Create an isolated Python environment to manage project dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Requirements

Install all the required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ Running the Application

Once the installation is complete, follow these steps:

1. Make sure your virtual environment is activated.
2. Ensure your main Python script is named `app.py`.
3. Launch the Streamlit application:

   ```bash
   streamlit run app.py
   ```

4. Open the local URL displayed in your terminal (usually [http://localhost:8501](http://localhost:8501)) in your web browser.

---

## 💡 How to Use

1. **Get an API Key:** Obtain a Groq API key from the [Groq Console](https://console.groq.com/).
2. **Enter API Key:** Launch the application, expand the **⚙️ Settings** section in the sidebar, and paste your API key into the password field.
3. **Upload Notes:** Upload your study materials or lecture notes in PDF format using the file uploader.
4. **Generate Content:** Click the **Generate** button to create your personalized study materials.
5. **Study & Test:** Navigate between the available tabs to:
   - Read the generated summary.
   - Review and practice using flashcards.
   - Take interactive quizzes and check your performance.

---

## 📌 Tech Stack

- **Python** – Core programming language.
- **Streamlit** – Web application framework.
- **Groq API** – High-speed LLM inference.
- **Llama 3.1 8B Instant** – AI model for content generation.
- **PyPDF** – PDF text extraction.

---

## 👨‍💻 Author

**Akshh-bot**

GitHub: [@akshh-bot](https://github.com/akshh-bot)
