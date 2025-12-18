# 🔍 TruthGuard AI

**TruthGuard AI** is a Streamlit-based content authenticity analysis system designed to evaluate the credibility of images and PDF documents.  
The application provides an intuitive interface, visual scoring, and risk-level indicators to help users assess whether content is likely authentic or manipulated.

---

## 🚀 Features

- 📸 **Image Authenticity Analysis**
- 📄 **PDF Document Analysis**
- 📊 Percentage-based authenticity scoring
- 🚦 Risk classification (LOW / MEDIUM / HIGH)
- 🎨 Professional and interactive UI (Streamlit)
- 🧠 Multi-factor analysis (visuals, metadata, language, logic, tone)
- ⚠️ Manual analysis fallback when AI services are unavailable

---

## 🛠️ Tech Stack

- **Frontend & UI**: Streamlit
- **Backend**: Python
- **Libraries Used**:
  - Streamlit
  - PyPDF2
  - Pillow (PIL)
  - Requests
- **AI Integration (Optional)**: Google Gemini API (disabled by default for stability)

---

## 📁 Project Structure

TruthGuard-AI/
│
├── app.py # Main Streamlit application
├── README.md # Project documentation
├── .gitignore # Git ignore file

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
git clone https://github.com/47combinator/TruthGuard-AI.git
cd TruthGuard-AI
2️⃣ Install dependencies
bash
Copy code
pip install streamlit PyPDF2 pillow requests
3️⃣ Run the application
bash
Copy code
python -m streamlit run app.py
The app will open in your browser at:

arduino
Copy code
http://localhost:8501
🧪 How It Works
User uploads an image or PDF

The system performs a multi-factor analysis

Scores are calculated using weighted indicators

Results are displayed with:

Authenticity %

Fake probability

Risk level

Visual progress bars and cards

⚠️ Disclaimer
This tool provides probabilistic analysis and should be used as a support system, not as a final authority.
Always verify critical information using trusted and independent sources.

👥 Team
This project was developed collaboratively as part of an academic initiative.

Contributors:

Pratyush Kunal Chaudhari

Team Members (Added via GitHub collaborators)

Mahin Oswal
Aasawari Khomane
Atharva Dhakne

📌 Future Enhancements
Real-time AI-powered fact verification

Text/news article analysis

Source URL credibility scoring

Deployment on Streamlit Cloud

User authentication & report history

📄 License
This project is intended for educational and academic use.

yaml
Copy code
