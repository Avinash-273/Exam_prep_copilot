# 🎓 Exam Prep Copilot

An AI-powered study assistant that turns a topic into a clear explanation, five revision flashcards, or a short practice quiz. Built with **Python**, **Streamlit**, **LangChain**, and **Groq**.

## Features

- **Topic explanations** — concise, student-friendly explanations with practical examples.
- **Flashcards** — five question-and-answer cards for active recall.
- **Practice quizzes** — short quizzes with an answer key and explanations.
- **Adjustable generation settings** — control creativity and response length.
- **Practice mode** — explore the app without configuring an API key.
- **Secret-safe configuration** — API credentials are read from environment variables or Streamlit Secrets, never hardcoded.

## Application preview

The app provides a focused study workflow: choose a topic, select an activity, generate learning material, and revise.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| User interface | Streamlit |
| LLM orchestration | LangChain |
| Model provider | Groq |
| Configuration | python-dotenv / Streamlit Secrets |

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Avinash-273/Exam_prep_copilot.git
   cd Exam_prep_copilot
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Configure your Groq API key (optional for practice mode):

   ```bash
   copy .env.example .env
   ```

   Open `.env` and replace the placeholder with your own key:

   ```env
   GROQ_API_KEY=your_actual_key_here
   ```

   Do not commit `.env` to GitHub. The `.gitignore` file excludes it.

5. Start the application:

   ```bash
   streamlit run app.py
   ```

   Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
3. Create an app and select this repository, the `main` branch, and `app.py` as the entry point.
4. Open the app's **Settings → Secrets** and add:

   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   ```

5. Deploy. Keep the key in Streamlit Secrets; do not add it to source files or commit it.

## Security notes

- `.env`, `.streamlit/secrets.toml`, virtual environments, and local logs are excluded from Git.
- Use your own API key in local environment variables or the hosting provider's secret manager.
- If a key was ever committed to a public repository, revoke it at the provider and create a replacement. Removing it from the latest commit does not remove it from Git history.
- Never share API keys in screenshots, issue reports, or public documentation.

## Project structure

```text
Exam_prep_copilot/
├── .streamlit/
│   └── config.toml
├── .env.example
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

## Future improvements

- Save study sessions and revision history.
- Add subject-wise question banks and difficulty levels.
- Support downloadable notes and spaced-repetition review.
- Add user accounts and progress analytics.

## Author

**Avinash R. A.**  
MCA Graduate | Python · Generative AI · LLM Applications

---

*An educational portfolio project. AI-generated content can contain errors; verify important information with authoritative learning materials.*
