import streamlit as st
from groq import Groq
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SBI AcquireBot",
    page_icon="🏦",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; }
    .header-banner {
        background: linear-gradient(135deg, #0D2137 0%, #1A3550 100%);
        border-radius: 14px; padding: 20px 28px; margin-bottom: 18px;
        display: flex; align-items: center; gap: 16px;
    }
    .header-title { color: #F5A623; font-size: 26px; font-weight: 700; margin: 0; }
    .header-sub   { color: #90B4CC; font-size: 13px; margin: 4px 0 0; }
    .status-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
    .chip { font-size: 11px; padding: 4px 12px; border-radius: 20px; font-weight: 500; }
    .chip-green { background: #E1F5EE; color: #085041; }
    .chip-blue  { background: #E8F0FE; color: #1A3550; }
    .chip-gold  { background: #FEF3DC; color: #7A4800; }
    .msg-user {
        background: #0D2137; color: white;
        padding: 12px 16px; border-radius: 14px 14px 4px 14px;
        margin: 6px 0 6px 60px; font-size: 14px; line-height: 1.6;
    }
    .msg-bot {
        background: white; color: #0D2137;
        padding: 12px 16px; border-radius: 14px 14px 14px 4px;
        margin: 6px 60px 6px 0; font-size: 14px; line-height: 1.6;
        border: 0.5px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .msg-label-user { text-align: right; font-size: 11px; color: #7A8FA6; margin: 0 4px 2px; }
    .msg-label-bot  { font-size: 11px; color: #7A8FA6; margin: 0 4px 2px; }
    .progress-wrap { background: #e2e8f0; border-radius: 10px; height: 6px; margin: 6px 0 14px; }
    .progress-fill { background: #F5A623; border-radius: 10px; height: 6px; }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are SBI AcquireBot — a friendly, intelligent customer onboarding assistant for State Bank of India (SBI).

Your goal: Identify, qualify, and convert potential customers by having a warm, natural conversation.

CONVERSATION FLOW (follow this order):
1. Greet the user warmly and ask their name
2. Ask what brings them to SBI today (new account, loan, investment, insurance, etc.)
3. Ask 2-3 short qualifying questions based on their goal:
   - For savings account: monthly income range, city, currently banked?
   - For loan: loan type, amount needed, employment type
   - For investment: age, risk appetite, investment amount
   - For insurance: type needed, family size
4. Based on answers, recommend the BEST SBI product with clear benefits
5. Explain the next step to proceed (documents needed / how to complete KYC)
6. End with a warm closing and reference number (make one up like SBI2026XXXXXX)

TONE RULES:
- Be warm, friendly, and conversational — not robotic
- Keep responses concise (3-5 lines max per message)
- Use simple language — avoid banking jargon
- Occasionally use relevant emojis like 😊 🏦 💰
- Support Hinglish naturally if user writes in it
- Always address the user by name once you know it

SBI PRODUCTS YOU CAN RECOMMEND:
- SBI Savings Account (Basic / Regular / Salary)
- SBI Fixed Deposit (FD), Recurring Deposit (RD)
- SBI Home Loan / Car Loan / Personal Loan / Education Loan
- SBI SIP / Mutual Funds (via SBI MF)
- SBI Life Insurance / SBI General Insurance
- SBI Credit Card (SimplySAVE / SimplyCLICK)
- YONO SBI — Digital banking super app

IMPORTANT: This is a hackathon demo. Be impressive but realistic. Never ask for real Aadhaar or PAN numbers."""

# ── Groq API setup ─────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.sidebar.text_input("🔑 Enter Groq API Key", type="password",
                                          help="Free at console.groq.com")
    if not GROQ_API_KEY:
        st.sidebar.info("👉 Get a **free** Groq API key at [console.groq.com](https://console.groq.com)")
        st.sidebar.markdown("Takes under 2 minutes — no credit card needed!")
        st.stop()

client = Groq(api_key=GROQ_API_KEY)
GROQ_MODEL = "llama-3.1-8b-instant"   # free, fast, reliable

# ── Safe chat function ─────────────────────────────────────────────────────────
def chat_with_groq(history, retries=2):
    """Send full conversation history to Groq and get a reply."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content, None
        except Exception as e:
            err = str(e)
            if "429" in err or "rate" in err.lower():
                if attempt < retries:
                    time.sleep(5)
                    continue
                return None, "quota"
            elif "401" in err or "authentication" in err.lower() or "unauthorized" in err.lower():
                return None, "apikey"
            else:
                # For debugging: print actual error
                print(f"DEBUG: Groq error: {err}")
                return None, "other"

# ── Error display ──────────────────────────────────────────────────────────────
def show_error(err_type):
    if err_type == "quota":
        st.error("⚠️ **Rate limit hit.** Groq allows 30 requests/min on free tier.")
        st.info("Wait 10–15 seconds and send your message again — it resets quickly!")
    elif err_type == "apikey":
        st.error("❌ **Invalid Groq API key.** Please check your key.")
        st.info("Get a free key at [console.groq.com](https://console.groq.com) → API Keys")
    else:
        st.error("Something went wrong. Please refresh and try again.")

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []        # display messages {"role", "text"}
if "history" not in st.session_state:
    st.session_state.history = []         # Groq-format history {"role", "content"}
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "step" not in st.session_state:
    st.session_state.step = 0

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div style="font-size:40px;">🏦</div>
    <div>
        <div class="header-title">SBI AcquireBot</div>
        <div class="header-sub">AI-Powered Customer Onboarding Assistant · Powered by Groq + Llama 3</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-row">
    <span class="chip chip-green">🟢 Online 24×7</span>
    <span class="chip chip-blue">🌐 Hindi · English · Hinglish</span>
    <span class="chip chip-gold">⚡ Avg onboarding: 5 mins</span>
</div>
""", unsafe_allow_html=True)

# Progress bar
steps = ["Start", "Intent", "Profile", "Recommend", "KYC", "Done"]
prog = min(st.session_state.step, 5)
pct  = int((prog / 5) * 100)
st.markdown(f"""
<div style="display:flex;justify-content:space-between;font-size:11px;color:#7A8FA6;margin-bottom:2px;">
    {"".join(f'<span style="color:{"#F5A623" if i <= prog else "#7A8FA6"};font-weight:{"600" if i==prog else "400"}">{s}</span>' for i, s in enumerate(steps))}
</div>
<div class="progress-wrap"><div class="progress-fill" style="width:{pct}%"></div></div>
""", unsafe_allow_html=True)

# ── Auto-greet on first load ───────────────────────────────────────────────────
if not st.session_state.greeted:
    with st.spinner("AcquireBot is starting..."):
        greeting, err = chat_with_groq([
            {"role": "user", "content": "Please start the conversation with your warm opening greeting."}
        ])
        if err:
            show_error(err)
            st.stop()
        st.session_state.messages.append({"role": "bot",  "text": greeting})
        st.session_state.history.append( {"role": "user",      "content": "Please start the conversation with your warm opening greeting."})
        st.session_state.history.append( {"role": "assistant", "content": greeting})
        st.session_state.greeted = True
        st.session_state.step = 1

# ── Chat history display ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-label-user">You</div><div class="msg-user">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-label-bot">🤖 AcquireBot</div><div class="msg-bot">{msg["text"]}</div>', unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "message", placeholder="e.g. I want to open a savings account",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send →", use_container_width=True)

def handle_input(text):
    st.session_state.messages.append({"role": "user", "text": text})
    st.session_state.history.append( {"role": "user", "content": text})
    with st.spinner("AcquireBot is typing..."):
        reply, err = chat_with_groq(st.session_state.history)
    if err:
        st.session_state.messages.pop()
        st.session_state.history.pop()
        show_error(err)
    else:
        st.session_state.messages.append({"role": "bot",       "text": reply})
        st.session_state.history.append( {"role": "assistant", "content": reply})
        count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.session_state.step = min(1 + count, 5)
        st.rerun()

if submitted and user_input.strip():
    handle_input(user_input.strip())

# ── Quick reply buttons ────────────────────────────────────────────────────────
if st.session_state.greeted:
    st.markdown("<p style='font-size:12px;color:#7A8FA6;margin:10px 0 6px;'>Quick replies:</p>", unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    if q1.button("💳 Open savings account", use_container_width=True):
        handle_input("I want to open a savings account")
    if q2.button("🏠 I need a home loan", use_container_width=True):
        handle_input("I need a home loan")
    if q3.button("📈 SIP investments", use_container_width=True):
        handle_input("Tell me about SIP investments")

# ── Reset ──────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Start New Conversation"):
    for key in ["messages", "history", "greeted", "step"]:
        st.session_state.pop(key, None)
    st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:none;border-top:0.5px solid #e2e8f0;margin-top:24px;">
<p style="text-align:center;font-size:11px;color:#B0C4D8;">
SBI AcquireBot · Built for SBI Hackathon 2026 · Theme: Agentic AI & Emerging Tech<br>
⚠️ Demo prototype only. Not an official SBI product.
</p>
""", unsafe_allow_html=True)
