import { useRef, useEffect, useState, useCallback } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import './ChatArea.css';

const SUGGESTIONS = [
  'Summarize the uploaded document',
  'What are the key points?',
  'Explain the main concepts',
  'List all the topics covered',
];

// ─── Mic hook ─────────────────────────────────────────────────────────────────
function useSpeech(onResult) {
  const [listening, setListening] = useState(false);
  const recRef = useRef(null);

  const toggle = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) { alert('Speech recognition not supported in this browser.'); return; }

    if (listening) {
      recRef.current?.stop();
      setListening(false);
      return;
    }

    const rec = new SpeechRecognition();
    rec.lang = 'en-US';
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    rec.onresult = (e) => { onResult(e.results[0][0].transcript); };
    rec.onend = () => setListening(false);
    rec.onerror = () => setListening(false);
    recRef.current = rec;
    rec.start();
    setListening(true);
  }, [listening, onResult]);

  return { listening, toggle };
}

// ─── Upload trigger (paperclip button) ─────────────────────────────────────────
function UploadTrigger({ onUpload, uploading, uploadProgress }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFiles = (files) => {
    const pdfs = Array.from(files).filter((f) => f.type === 'application/pdf');
    if (pdfs.length) onUpload(pdfs);
  };

  return (
    <div
      className={`upload-trigger-wrap ${dragging ? 'drag-over' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => { e.preventDefault(); setDragging(false); handleFiles(e.dataTransfer.files); }}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        multiple
        hidden
        onChange={(e) => handleFiles(e.target.files)}
      />
      <button
        className={`upload-btn ${uploading ? 'uploading' : ''} ${dragging ? 'drag-over' : ''}`}
        onClick={() => !uploading && inputRef.current?.click()}
        title={uploading ? `Uploading ${uploadProgress || 'PDF'}…` : 'Upload PDF (or drag & drop)'}
        disabled={uploading}
      >
        {uploading ? (
          <span className="upload-spinner"></span>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"
              stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </button>
    </div>
  );
}

// ─── Main ChatArea ──────────────────────────────────────────────────────────────
export default function ChatArea({
  messages,
  isTyping,
  onSend,
  onUpload,
  uploading,
  uploadProgress,
  uploadedFiles,
}) {
  const [input, setInput] = useState('');
  const bottomRef   = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const submitInput = (text) => {
    const trimmed = (text || input).trim();
    if (!trimmed) return;
    onSend(trimmed);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitInput(); }
  };

  const handleTextareaChange = (e) => {
    setInput(e.target.value);
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  };

  // Mic — appends transcript to current input
  const handleSpeechResult = useCallback((transcript) => {
    setInput((prev) => (prev ? prev + ' ' + transcript : transcript));
    textareaRef.current?.focus();
  }, []);
  const { listening, toggle: toggleMic } = useSpeech(handleSpeechResult);

  const isEmpty = messages.length === 0;

  return (
    <div className="chat-area">
      {/* ── Header ── */}
      <div className="chat-header">
        <div className="chat-header-left">
          <div className="chat-status-badge">
            <span className="chat-status-dot"></span>
            RAG Assistant
          </div>
        </div>
        <div className="chat-header-right">
          {uploadedFiles.length > 0 && (
            <div className="docs-badge">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"
                  stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              {uploadedFiles.length} doc{uploadedFiles.length > 1 ? 's' : ''} loaded
            </div>
          )}
        </div>
      </div>

      {/* ── Messages ── */}
      <div className="messages-container">
        {isEmpty ? (
          <div className="welcome-screen">
            <div className="welcome-icon">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                  stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h1 className="welcome-title">Welcome to Nexus RAG</h1>
            <p className="welcome-sub">
              Upload a PDF and ask questions about its content, or start a general conversation.
            </p>
            <div className="suggestions-grid">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  className="suggestion-chip"
                  onClick={() => { setInput(s); textareaRef.current?.focus(); }}
                >
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"
                      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg) => <Message key={msg.id} {...msg} />)}
            {isTyping && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* ── Upload status bar (replaces floating modal) ── */}
      {uploading && (
        <div className="upload-status-bar">
          <span className="upload-status-spinner"></span>
          <span>
            Uploading <strong>{uploadProgress || 'PDF'}</strong> — please wait…
          </span>
        </div>
      )}

      {/* ── Input bar ── */}
      <div className="input-bar">
        <UploadTrigger onUpload={onUpload} uploading={uploading} uploadProgress={uploadProgress} />

        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            className="input-field"
            placeholder="Ask anything about your document…"
            value={input}
            onChange={handleTextareaChange}
            onKeyDown={handleKey}
            rows={1}
          />
        </div>

        {/* Mic button */}
        <button
          className={`mic-btn ${listening ? 'listening' : ''}`}
          onClick={toggleMic}
          title={listening ? 'Stop listening' : 'Speak your question'}
        >
          {listening ? (
            // Stop icon when active
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" rx="2"/>
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"
                stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"
                stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
          {listening && <span className="mic-pulse"></span>}
        </button>

        {/* Send button */}
        <button
          className="send-btn"
          onClick={() => submitInput()}
          disabled={!input.trim()}
          title="Send (Enter)"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"
              stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      <p className="input-hint">Enter to send · Shift+Enter for new line · 🎤 mic for voice</p>
    </div>
  );
}
