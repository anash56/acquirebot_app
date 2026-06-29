# 🏦 SBI AcquireBot

<div align="center">

![SBI AcquireBot](https://img.shields.io/badge/SBI-AcquireBot-F5A623?style=for-the-badge&logo=robot&logoColor=white)
![Hackathon](https://img.shields.io/badge/SBI_Hackathon-2026-0D2137?style=for-the-badge)
![Theme](https://img.shields.io/badge/Agentic_AI_%26_Emerging_Tech-1A3550?style=for-the-badge)
![Problem](https://img.shields.io/badge/Customer_Acquisition-02C39A?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq_+_Llama_3-F55036?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge)

### AI-Powered Conversational Customer Onboarding Agent for SBI

*Identify · Qualify · Convert — through intelligent conversation*

[▶ Watch Demo](#-demo) · [🚀 Quick Start](#-quick-start) · [📐 Architecture](#-architecture)

</div>

---

## 🎯 Problem Statement

Despite SBI's massive reach of **500M+ customers**, customer acquisition suffers from critical gaps:

| Problem | Business Impact |
|---|---|
| Static web forms — no personalisation | High drop-off before account opening |
| Branch-dependent onboarding | High cost per acquisition, limited hours |
| No intelligent product matching | Wrong product recommendations, low satisfaction |
| Language barrier for rural users | Underbanked population stays unbanked |

> **Core insight:** A new customer doesn't know which SBI product suits them. Nobody guides them. AcquireBot fills that gap — 24×7, in their language, in under 5 minutes.

---

## 💡 Solution — SBI AcquireBot

AcquireBot is an AI-powered conversational agent that replaces the static onboarding form with an intelligent chat experience. It asks the right questions, understands the customer's financial profile, recommends the best-fit SBI product, and guides them through KYC — all through natural conversation.

**Live conversation example:**

```
User:  "Hi, mujhe SBI mein account kholna hai"

Bot:   "Namaste! Main SBI AcquireBot hoon 😊
        Aapka naam kya hai?"

User:  "Rohan"

Bot:   "Nice to meet you Rohan! Aap savings account
        chahte hain ya kuch aur — loan, investment?"

User:  "Savings account, salary 28000 hai"

Bot:   "Perfect! SBI Salary Account aapke liye
        best choice hai — zero minimum balance,
        free YONO access, aur instant KYC.
        Kya aap aage badhna chahenge? 🏦"
```

**Result:** Rohan goes from curious visitor → qualified lead → product recommendation in under 3 minutes, without visiting a branch.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Smart Profiling** | Asks 3–5 contextual questions to build the user's financial profile |
| 🎯 **Product Matching** | Recommends the best-fit SBI product from 10+ options |
| 🌐 **Multilingual** | Handles English, Hindi, and Hinglish naturally |
| ⚡ **Sub-second Response** | Groq inference delivers replies in under 1 second |
| 📊 **Visual Progress** | Real-time onboarding progress bar (Start → KYC → Done) |
| 🔁 **Agent Handoff** | Complex cases escalate to human agents with full context |
| 📱 **WhatsApp-Ready** | Architecture designed for WhatsApp Business API deployment |

---

## 🛠 Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **LLM** | Groq API — Llama 3 (8B) | Natural language understanding & generation |
| **Conversation** | Groq Python SDK | Multi-turn chat history management |
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python 3.9+ | Business logic & conversation flow |
| **Interface (prod)** | WhatsApp Business API | Customer-facing channel |
| **Deployment** | Streamlit Cloud / Google Cloud Run | Scalable serverless hosting |

---

## 📐 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      User Interface                       │
│           WhatsApp · YONO App · Streamlit Demo            │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    AcquireBot Engine                      │
│                                                           │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │   Intent     │──▶│   Profile    │──▶│   Product   │  │
│  │  Detection   │   │   Builder    │   │   Matcher   │  │
│  └──────────────┘   └──────────────┘   └─────────────┘  │
│                            │                             │
│                            ▼                             │
│                 ┌─────────────────────┐                  │
│                 │   Groq + Llama 3    │                  │
│                 │    (LLM Backend)    │                  │
│                 └─────────────────────┘                  │
└────────────────────────┬─────────────────────────────────┘
                         │
             ┌───────────┴────────────┐
             ▼                        ▼
    ┌─────────────────┐    ┌─────────────────────┐
    │  KYC Onboarding │    │  Human Agent Handoff │
    │  (simple cases) │    │  (complex cases)     │
    └─────────────────┘    └─────────────────────┘
```

---

## 🔄 Conversation Flow

```
1. GREET       →  Warm welcome, collect user's name
2. INTENT      →  Identify financial need (account / loan / investment / insurance)
3. QUALIFY     →  3–4 smart questions to build financial profile
4. RECOMMEND   →  Best-fit SBI product with clear benefits explained
5. ONBOARD     →  Documents required, KYC steps explained conversationally
6. CONFIRM     →  Application reference number issued
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Free Groq API key from [console.groq.com](https://console.groq.com) — no credit card needed

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sbi-acquirebot.git
cd sbi-acquirebot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
mkdir -p .streamlit
```

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

```bash
# 4. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser 🎉

---

## 📦 SBI Products Supported

| Category | Products |
|---|---|
| **Accounts** | Regular Savings, Salary Account, Basic Savings |
| **Deposits** | Fixed Deposit (FD), Recurring Deposit (RD) |
| **Loans** | Home Loan, Car Loan, Personal Loan, Education Loan |
| **Investments** | SBI SIP, Mutual Funds (via SBI MF) |
| **Insurance** | SBI Life, SBI General Insurance |
| **Cards** | SimplySAVE Credit Card, SimplyCLICK Credit Card |
| **Digital** | YONO SBI Super App |

---

## 📁 Project Structure

```
sbi-acquirebot/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Protects API key from being uploaded

```

---

## 🗺 Roadmap

- [x] Core conversational onboarding engine
- [x] Intelligent product recommendation
- [x] Multilingual support — English, Hindi, Hinglish
- [x] Visual progress tracking
- [x] Groq + Llama 3 integration
- [ ] WhatsApp Business API deployment
- [ ] Live KYC document verification
- [ ] SBI agent dashboard with conversation analytics
- [ ] Voice input support for low-literacy users

---

<div align="center">

**SBI Hackathon 2026 · Agentic AI & Emerging Tech · Problem: Customer Acquisition**

</div>
