import streamlit as st
import speech_recognition as sr

import uuid


# Generate unique user session ID
if "user_id" not in st.session_state:

    st.session_state.user_id = str(uuid.uuid4())

from api_client import (
    send_message,
    upload_pdf,
    list_pdfs,
    delete_pdf,
    delete_all_pdfs,
    clear_database
)

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus · RAG Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@400;500;700;800;900&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
    --bg:          #07090f;
    --bg1:         #0c0f1a;
    --bg2:         #111420;
    --surface:     #171c2e;
    --surface2:    #1f2540;
    --border:      #252c45;
    --border2:     #2e3858;
    --accent:      #5b8df6;
    --accent-glow: rgba(91,141,246,.18);
    --violet:      #8b5cf6;
    --teal:        #14d9b0;
    --teal-glow:   rgba(20,217,176,.15);
    --rose:        #f87171;
    --text:        #f0f2f8;
    --text2:       #9aa3be;
    --text3:       #4b5578;
    --text4:       #2e3858;
    --r:           16px;
    --r-sm:        10px;
    --hf:          'Cabinet Grotesk', sans-serif;
    --bf:          'Instrument Sans', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
.stApp, .stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"],
.main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--bf) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"] { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: var(--bg1) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 280px !important;
    max-width: 280px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    background: transparent !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: var(--r) !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p { color: var(--text2) !important; font-size: 13px !important; }

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--bf) !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 9px 18px !important;
    transition: all .18s ease !important;
}
.stButton > button:hover {
    background: var(--surface2) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(91,141,246,.2) !important;
}

.btn-upload .stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--violet)) !important;
    border: none !important;
    color: #fff !important;
    width: 100% !important;
    border-radius: var(--r) !important;
    box-shadow: 0 4px 20px rgba(91,141,246,.3) !important;
}
.btn-upload .stButton > button:hover {
    box-shadow: 0 6px 28px rgba(91,141,246,.5) !important;
    transform: translateY(-2px) !important;
}

.btn-danger .stButton > button {
    background: rgba(248,113,113,.07) !important;
    border-color: rgba(248,113,113,.2) !important;
    color: var(--rose) !important;
}
.btn-danger .stButton > button:hover {
    background: var(--rose) !important;
    border-color: var(--rose) !important;
    color: #fff !important;
}

/* ═══ MIC FIXED ═══ */
div[data-testid="stElementContainer"]:has(.mic-anchor) + div[data-testid="stElementContainer"] {
    position: fixed !important;
    bottom: 16px !important;
    right: 16px !important;
    z-index: 9999 !important;
    width: auto !important;
}

div[data-testid="stElementContainer"]:has(.mic-anchor) + div[data-testid="stElementContainer"] button {
    width: 52px !important;
    height: 52px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, var(--teal), #00b896) !important;
    border: none !important;
    color: #fff !important;
    font-size: 22px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 20px rgba(20,217,176,.35), 0 0 0 0 rgba(20,217,176,.2) !important;
    animation: micPulse 2.8s ease-in-out infinite !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stElementContainer"]:has(.mic-anchor) + div[data-testid="stElementContainer"] button:hover {
    animation: none !important;
    box-shadow: 0 6px 30px rgba(20,217,176,.55) !important;
    transform: scale(1.1) !important;
    background: linear-gradient(135deg, var(--teal), #00b896) !important;
}

@keyframes micPulse {
    0%,100% { box-shadow: 0 4px 20px rgba(20,217,176,.35), 0 0 0 0 rgba(20,217,176,.25); }
    60%      { box-shadow: 0 4px 24px rgba(20,217,176,.35), 0 0 0 10px rgba(20,217,176,.02); }
}

/* ═══ CHAT INPUT ═══ */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 280px !important;
    right: 84px !important;
    z-index: 8888 !important;
    background: linear-gradient(to top, var(--bg) 75%, transparent) !important;
    padding: 16px 20px 20px !important;
}
[data-testid="stChatInput"] > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 50px !important;
    padding: 5px 10px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: var(--bf) !important;
    font-size: 15px !important;
    caret-color: var(--accent) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--text3) !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent), var(--violet)) !important;
    border: none !important;
    border-radius: 50% !important;
    color: #fff !important;
    box-shadow: 0 2px 12px rgba(91,141,246,.35) !important;
    transition: transform .15s, box-shadow .15s !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.12) !important;
    box-shadow: 0 4px 22px rgba(91,141,246,.55) !important;
}

/* ═══ CHAT MESSAGES ═══ */
.topbar {
    position: sticky; top: 0; z-index: 500;
    background: rgba(7,9,15,.93);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--border);
    padding: 15px 28px;
    display: flex; align-items: center; justify-content: space-between;
}
.topbar-title {
    font-family: var(--hf); font-size: 17px; font-weight: 800;
    color: var(--text); letter-spacing: -.01em;
    display: flex; align-items: center; gap: 10px;
}
.live-pill {
    display: flex; align-items: center; gap: 5px;
    background: rgba(20,217,176,.1); border: 1px solid rgba(20,217,176,.2);
    border-radius: 20px; padding: 3px 9px;
    font-size: 10.5px; font-weight: 700;
    color: var(--teal); letter-spacing: .07em; text-transform: uppercase;
}
.live-dot { width:6px;height:6px;border-radius:50%;background:var(--teal);animation:ldot 1.8s infinite; }
@keyframes ldot { 0%,100%{opacity:1} 50%{opacity:.25} }
.topbar-hint { font-size: 13px; color: var(--text3); font-style: italic; }

.chat-area {
    padding: 10px 32px 110px;
    min-height: auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 20px;
}

.empty-wrap {
    display:flex; flex-direction:column; align-items:center;
    justify-content:flex-start; gap:18px;
    padding:30px 24px 0px; text-align:center;
}
.empty-icon {
    width:76px;height:76px;border-radius:22px;
    background:linear-gradient(135deg,var(--surface2),var(--surface));
    border:1px solid var(--border2);
    display:flex;align-items:center;justify-content:center;
    font-size:32px;
    box-shadow:0 8px 32px rgba(0,0,0,.5);
    animation:floatUp 3.5s ease-in-out infinite;
}
@keyframes floatUp {
    0%,100%{transform:translateY(0)} 50%{transform:translateY(-9px)}
}
.empty-title {
    font-family:var(--hf);font-size:26px;font-weight:900;
    color:var(--text);letter-spacing:-.02em;
}
.empty-sub { font-size:14.5px;color:var(--text2);max-width:320px;line-height:1.7; }
.chips { display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:4px; }
.chip {
    background:var(--surface);border:1px solid var(--border2);
    border-radius:20px;padding:7px 15px;
    font-size:13px;color:var(--text2);
    transition:all .18s;
}
.chip:hover { border-color:var(--accent);color:var(--accent); }

/* ─── FIX: bubble text renders cleanly, no word-break on chars ─── */
.msg-row {
    display:flex;gap:11px;align-items:flex-end;
    animation:msgIn .38s cubic-bezier(.22,1,.36,1) both;
    max-width:800px;margin:0 auto;width:100%;
}
.msg-row.user { flex-direction:row-reverse; }
@keyframes msgIn {
    from{opacity:0;transform:translateY(18px) scale(.97)}
    to{opacity:1;transform:none}
}
.av {
    width:36px;height:36px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:14px;font-weight:900;font-family:var(--hf);
    box-shadow:0 2px 8px rgba(0,0,0,.4);
}
.av-bot { background:linear-gradient(135deg,var(--accent),var(--violet));color:#fff; }
.av-usr { background:linear-gradient(135deg,var(--teal),#00a882);color:#fff;font-size:15px; }

.msg-col { display:flex;flex-direction:column;max-width:calc(100% - 50px); }
.msg-col.user { align-items:flex-end;max-width:calc(100% - 50px); }

.bubble {
    padding:13px 18px;
    border-radius:20px;
    font-size:14.5px;
    line-height:1.7;
    overflow-wrap: break-word;
    word-break: break-word;
    white-space: normal;
    color: var(--text) !important;
}
.bubble.bot {
    background:var(--surface);
    color:var(--text) !important;
    border:1px solid var(--border2);
    border-bottom-left-radius:5px;
    box-shadow:0 2px 8px rgba(0,0,0,.35);
    max-width: 680px;
    width: 100%;
}
.bubble.user {
    background:linear-gradient(135deg,var(--accent),var(--violet));
    color:#ffffff !important;
    border-bottom-right-radius:5px;
    box-shadow:0 4px 20px rgba(91,141,246,.3);
    max-width: 400px;
    width: auto;
    display: inline-block;
}
.ts { font-size:11px;color:var(--text4);margin-top:4px;padding:0 3px; }

/* ─── SIDEBAR CONVERSATION HISTORY ─── */
.conv-item {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 12px;
    border-radius: var(--r-sm);
    border: 1px solid var(--border);
    background: var(--surface);
    margin-bottom: 6px;
    cursor: pointer;
    transition: all .18s ease;
    text-decoration: none;
}
.conv-item:hover {
    border-color: var(--accent);
    background: var(--surface2);
    transform: translateX(2px);
}
.conv-item-ico {
    font-size: 13px;
    flex-shrink: 0;
    opacity: 0.7;
}
.conv-item-text {
    font-size: 12.5px;
    color: var(--text2) !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    font-weight: 500;
}
.conv-item-idx {
    font-size: 10px;
    color: var(--text4) !important;
    flex-shrink: 0;
}

/* Sidebar layout pieces */
.sb-brand {
    padding:20px 20px 16px;
    border-bottom:1px solid var(--border);
    display:flex;align-items:center;gap:12px;
    background:linear-gradient(135deg,rgba(91,141,246,.06),transparent);
}
.sb-logo {
    width:42px;height:42px;border-radius:12px;
    background:linear-gradient(135deg,var(--accent),var(--violet));
    display:flex;align-items:center;justify-content:center;
    font-family:var(--hf);font-weight:900;font-size:19px;color:#fff;
    box-shadow:0 4px 16px rgba(91,141,246,.35);flex-shrink:0;
}
.sb-name { font-family:var(--hf);font-weight:800;font-size:17px;color:var(--text);letter-spacing:-.01em;line-height:1.1; }
.sb-tag  { font-size:10px;color:var(--accent);font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-top:2px; }

.sb-body { padding:18px 18px 0; }

.sb-stats { display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:18px; }
.sb-stat {
    background:var(--surface);border:1px solid var(--border);
    border-radius:var(--r-sm);padding:12px;text-align:center;
}
.sb-stat-num { font-family:var(--hf);font-size:24px;font-weight:900;color:var(--accent);line-height:1; }
.sb-stat-lbl { font-size:10px;color:var(--text3);margin-top:4px;text-transform:uppercase;letter-spacing:.08em;font-weight:700; }

.sec-lbl {
    font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
    color:var(--text3);margin-bottom:10px;
    display:flex;align-items:center;gap:8px;
}
.sec-lbl::after { content:'';flex:1;height:1px;background:var(--border); }

.file-card {
    display:flex;align-items:center;gap:10px;
    background:var(--surface);border:1px solid var(--border);
    border-radius:var(--r-sm);padding:9px 11px;margin-bottom:7px;
    transition:border-color .15s,background .15s;
}
.file-card:hover { border-color:var(--border2);background:var(--surface2); }
.file-ico { font-size:15px;flex-shrink:0; }
.file-nm { flex:1;font-size:12.5px;color:var(--text2) !important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis; }

.no-files {
    text-align:center;padding:18px 10px;color:var(--text3);
    font-size:13px;line-height:1.6;
    background:var(--surface);border:1.5px dashed var(--border);border-radius:var(--r);
}

.sb-footer {
    padding:12px 18px;border-top:1px solid var(--border);
    text-align:center;font-size:11px;color:var(--text4);margin-top:16px;
}

[data-testid="stSpinner"] > div { border-color:var(--accent) transparent transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "messages"         not in st.session_state: st.session_state.messages = []
if "files"            not in st.session_state:
    try:    st.session_state.files = list_pdfs()
    except: st.session_state.files = []
if "uploaded_files"   not in st.session_state: st.session_state.uploaded_files = []
if "voice_input"      not in st.session_state: st.session_state.voice_input = ""
if "jump_to_msg"      not in st.session_state: st.session_state.jump_to_msg = None

# ─────────────────────────────────────────────
# Voice
# ─────────────────────────────────────────────
def get_voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as src:
            st.toast("🎙️ Listening — speak now…", icon="🎤")
            r.adjust_for_ambient_noise(src, duration=0.8)
            audio = r.listen(src, timeout=7, phrase_time_limit=14)
        text = r.recognize_google(audio, language="en-IN")
        st.session_state.voice_input = text
        st.toast(f"Captured: {text[:55]}{'…' if len(text)>55 else ''}", icon="✅")
    except sr.WaitTimeoutError:  st.toast("Timed out — try again", icon="⏱️")
    except sr.UnknownValueError: st.toast("Couldn't understand — try again", icon="❌")
    except sr.RequestError:      st.toast("Speech service unavailable", icon="🚫")
    except Exception as e:       st.toast(f"Mic error: {e}", icon="⚠️")

# ─────────────────────────────────────────────
# Helper: get last N user questions
# ─────────────────────────────────────────────
def get_recent_questions(n=5):
    """Return last n user messages with their index in messages list."""
    user_msgs = [
        (i, msg["content"])
        for i, msg in enumerate(st.session_state.messages)
        if msg["role"] == "user" and msg["content"] != "Thinking… ⏳"
    ]
    return user_msgs[-n:]  # last 5

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    n_docs = len(st.session_state.files)
    n_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])

    st.markdown(f"""
    <div class="sb-brand">
        <div class="sb-logo">N</div>
        <div>
            <div class="sb-name">Nexus AI</div>
            <div class="sb-tag">RAG Assistant</div>
        </div>
    </div>
    <div class="sb-body">
        <div class="sb-stats">
            <div class="sb-stat">
                <div class="sb-stat-num">{n_docs}</div>
                <div class="sb-stat-lbl">Documents</div>
            </div>
            <div class="sb-stat">
                <div class="sb-stat-num">{n_msgs}</div>
                <div class="sb-stat-lbl">Queries</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 18px">', unsafe_allow_html=True)

    # ── Recent Conversations ──
    recent_qs = get_recent_questions(3)
    if recent_qs:
        st.markdown('<div class="sec-lbl">Recent Queries</div>', unsafe_allow_html=True)
        for msg_idx, question in reversed(recent_qs):
            short_q = question[:32] + "…" if len(question) > 34 else question
            # Use a button styled as a conversation item
            if st.button(f"💬  {short_q}", key=f"conv_{msg_idx}", use_container_width=True):
                st.session_state.jump_to_msg = msg_idx
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Upload PDF ──
    st.markdown('<div class="sec-lbl">Upload PDF</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    if uploaded_file and uploaded_file.name not in st.session_state.uploaded_files:
        st.markdown('<div class="btn-upload">', unsafe_allow_html=True)
        if st.button("📤  Add to Knowledge Base", use_container_width=True):
            with st.spinner("Indexing…"):
                result = upload_pdf(uploaded_file)
            st.toast(result.get("message", "Uploaded ✓"), icon="📄")
            st.session_state.uploaded_files.append(uploaded_file.name)
            st.session_state.files = list_pdfs()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Knowledge Base ──
    st.markdown('<div class="sec-lbl">Knowledge Base</div>', unsafe_allow_html=True)

    files = st.session_state.files
    if files:
        for idx, file in enumerate(files):
            c1, c2 = st.columns([5, 1])
            with c1:
                short = file[:25] + "…" if len(file) > 27 else file
                st.markdown(
                    f'<div class="file-card">'
                    f'<span class="file-ico">📄</span>'
                    f'<span class="file-nm" title="{file}">{short}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with c2:
                if st.button("✕", key=f"del_{idx}", help="Remove"):
                    delete_pdf(file)
                    st.session_state.files = list_pdfs()
                    st.toast("Removed", icon="🗑️")
                    st.rerun()
    else:
        st.markdown(
            '<div class="no-files">📭 No documents yet<br>'
            '<span style="font-size:12px">Upload a PDF to begin</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Danger Zone ──
    st.markdown('<div class="sec-lbl">Danger Zone</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("🧹 Clear PDFs", use_container_width=True):
            delete_all_pdfs()
            st.session_state.files = []
            st.session_state.uploaded_files = []
            st.toast("All PDFs removed", icon="🧹")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("⚠ Reset DB", use_container_width=True):
            clear_database()
            st.session_state.files = []
            st.session_state.uploaded_files = []
            st.toast("Database reset", icon="⚠️")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # padding div
    st.markdown('<div class="sb-footer">✦ Nexus AI · 2025 · Powered by RAG</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-title">
        ✦ Chat with your Documents
        <div class="live-pill"><div class="live-dot"></div>Live</div>
    </div>
    <div class="topbar-hint">Ask anything — I'll find it in your PDFs</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-wrap">
        <div class="empty-icon">✦</div>
        <div class="empty-title">Ready to Explore</div>
        <div class="empty-sub">Upload a PDF in the sidebar, then ask anything. I'll retrieve precise answers from your documents.</div>
        <div class="chips">
            <div class="chip">📊 Summarize documents</div>
            <div class="chip">🔍 Find specific data</div>
            <div class="chip">💬 Follow-up questions</div>
            <div class="chip">📋 Extract key points</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    import datetime
    now = datetime.datetime.now().strftime("%I:%M %p")

    # Determine which messages to display (jump to specific or show all)
    highlight_idx = st.session_state.jump_to_msg

    for i, msg in enumerate(st.session_state.messages):
        role    = msg["role"]
        raw = msg["content"]
        content = raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Highlight the jumped-to message
        extra_style = ""
        if highlight_idx is not None and i == highlight_idx:
            extra_style = "outline: 2px solid var(--accent); outline-offset: 3px;"
            st.session_state.jump_to_msg = None  # reset after highlighting

        if role == "user":
            st.markdown(f"""
            <div class="msg-row user" id="msg-{i}">
                <div class="av av-usr">🧑</div>
                <div class="msg-col user">
                    <div class="bubble user" style="{extra_style}">{content}</div>
                    <div class="ts">{now}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row bot" id="msg-{i}">
                <div class="av av-bot">N</div>
                <div class="msg-col">
                    <div class="bubble bot" style="{extra_style}">{content}</div>
                    <div class="ts">{now}</div>
                </div>
            </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Mic fixed bottom-right ──
st.markdown('<span class="mic-anchor"></span>', unsafe_allow_html=True)
if st.button("🎙️", key="mic_btn", help="Voice input"):
    get_voice_input()
    st.rerun()

# ── Chat input ──
user_input = st.chat_input("Ask anything about your documents…")

# ── Handle input ──
final_input = None
if user_input:
    final_input = user_input
elif st.session_state.voice_input:
    final_input = st.session_state.voice_input
    st.session_state.voice_input = ""

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    st.session_state.messages.append({"role": "assistant", "content": "Thinking… ⏳"})
    st.rerun()

# AFTER rerun — process thinking placeholder
if (
    st.session_state.messages
    and st.session_state.messages[-1]["content"] == "Thinking… ⏳"
):
    last_user_msg = st.session_state.messages[-2]["content"]
    response = send_message(last_user_msg)
    st.session_state.messages[-1] = {"role": "assistant", "content": response}
    st.rerun()