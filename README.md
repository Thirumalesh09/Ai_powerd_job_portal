# 🧠 CareerWise – AI-Powered Job Portal

CareerWise is a Django-based AI-powered job portal that helps users:
- Parse resumes automatically from PDF files 🧾  
- Get personalized career guidance based on skills 🤖  
- Discover real-time job recommendations 💼  
- Chat with an AI career assistant for interview tips and advice 💬  

---

## 🚀 Features

- 🔍 **Resume Parsing:** Extracts email, phone, LinkedIn, GitHub, skills, education, and experience from uploaded PDF resumes using `pdfplumber` and regex.
- 📈 **Resume Scoring:** Automatically calculates a score based on resume completeness.
- 🎯 **Career Guidance:** Generates personalized feedback using Together.ai LLM API.
- 💡 **Job Recommendations:** Fetches relevant jobs dynamically based on skills.
- 💬 **AI Chatbot:** Interactive AI career assistant (Mistral model via Together API).
- 🧰 **Admin Panel:** Full Django admin for managing users, resumes, and job data.

---

## 🏗️ Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Django 4.x (Python 3.10+) |
| **Frontend** | HTML, CSS, Bootstrap |
| **Database** | SQLite (default) |
| **AI / NLP** | Together.ai API (Mistral / Mixtral models) |
| **PDF Parsing** | `pdfplumber` |
| **APIs** | Custom job fetch API via `requests` |
| **Version Control** | Git & GitHub |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Thirumalesh09/Ai_powerd_job_portal.git
cd Ai_powerd_job_portal
