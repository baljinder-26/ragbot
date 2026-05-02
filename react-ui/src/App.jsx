import { useState, useRef, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import { useLocalStorage } from './hooks/useLocalStorage';
import { sendChat, uploadPDF, deletePDF } from './utils/api';
import './App.css';

// Stable user-id, never regenerated
const UID_KEY = 'raggbot_uid';
const USER_ID = 'user_' + (() => {
  let id = localStorage.getItem(UID_KEY);
  if (!id) { id = Math.random().toString(36).slice(2, 10); localStorage.setItem(UID_KEY, id); }
  return id;
})();

const mkId   = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
const mkMsg  = (role, content, extra = {}) => ({ id: mkId(), role, content, timestamp: Date.now(), ...extra });
const mkSess = () => ({ id: mkId(), messages: [], createdAt: Date.now(), updatedAt: Date.now() });

// Strip any leftover 'system' / upload messages from old broken versions
function sanitizeSessions(sessions) {
  return sessions.map((s) => ({
    ...s,
    messages: s.messages.filter(
      (m) => m.role === 'user' || m.role === 'assistant'
    ),
  }));
}

export default function App() {
  const [sessions,      setSessions]      = useLocalStorage('raggbot_sessions', []);
  const [activeId,      setActiveId]      = useLocalStorage('raggbot_active',   null);
  const [uploadedFiles, setUploadedFiles] = useLocalStorage('raggbot_files',    []);

  const [isTyping,         setIsTyping]         = useState(false);
  const [uploading,        setUploading]        = useState(false);
  const [uploadProgress,   setUploadProgress]   = useState(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [error,            setError]            = useState(null);

  // Keep refs always pointing to latest values (avoids stale closures)
  const activeIdRef  = useRef(activeId);
  const sessionsRef  = useRef(sessions);
  activeIdRef.current  = activeId;
  sessionsRef.current  = sessions;

  // One-time sanitize: remove any stale upload/system messages from old versions
  useEffect(() => {
    setSessions((prev) => sanitizeSessions(prev));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const activeSession = sessions.find((s) => s.id === activeId) || null;

  // ─── Session helpers ───────────────────────────────────────────────────────
  const ensureSession = () => {
    const cur  = activeIdRef.current;
    // Use the ref so we always have the latest sessions list
    const exists = sessionsRef.current.find((s) => s.id === cur);
    if (exists) return cur;
    const s = mkSess();
    setSessions((prev) => [s, ...prev]);
    setActiveId(s.id);
    activeIdRef.current = s.id;
    return s.id;
  };

  const appendMsg = (sessionId, msg) => {
    setSessions((prev) =>
      prev.map((s) =>
        s.id === sessionId
          ? { ...s, messages: [...s.messages, msg], updatedAt: Date.now() }
          : s
      )
    );
  };

  // ─── Handlers ─────────────────────────────────────────────────────────────
  const handleNewChat = () => {
    const s = mkSess();
    setSessions((prev) => [s, ...prev]);
    setActiveId(s.id);
  };

  const handleSelectSession = (id) => setActiveId(id);

  const handleDeleteSession = (id) => {
    setSessions((prev) => prev.filter((s) => s.id !== id));
    if (activeId === id) {
      const rest = sessions.filter((s) => s.id !== id);
      setActiveId(rest[0]?.id || null);
    }
  };

  const handleSend = async (text) => {
    // Make sure there's a session BEFORE we do anything async
    const sid = ensureSession();

    const userMsg = mkMsg('user', text);
    appendMsg(sid, userMsg);

    setIsTyping(true);
    setError(null);

    try {
      const data = await sendChat(text, USER_ID);
      appendMsg(sid, mkMsg('assistant', data.response || 'No response received.'));
    } catch {
      setError('Could not reach the API — is the backend running on port 8000?');
    } finally {
      setIsTyping(false);
    }
  };

  const handleUpload = async (files) => {
    setUploading(true);
    setError(null);

    for (const file of files) {
      setUploadProgress(file.name);
      try {
        await uploadPDF(file, USER_ID);
        setUploadedFiles((prev) => (prev.includes(file.name) ? prev : [...prev, file.name]));
      } catch {
        setError(`Upload failed for "${file.name}". Check the backend.`);
      }
    }

    setUploading(false);
    setUploadProgress(null);
  };

  const handleDeleteFile = async (filename) => {
    try {
      await deletePDF(filename, USER_ID);
      setUploadedFiles((prev) => prev.filter((f) => f !== filename));
    } catch {
      setError('Could not delete the file.');
    }
  };

  return (
    <div className="app-layout">
      <Sidebar
        sessions={sessions}
        activeSession={activeId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        uploadedFiles={uploadedFiles}
        onDeleteFile={handleDeleteFile}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed((v) => !v)}
      />
      <main className="app-main">
        {error && (
          <div className="error-toast">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
              <path d="M12 8v4M12 16h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            {error}
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}
        <ChatArea
          messages={activeSession?.messages || []}
          isTyping={isTyping}
          onSend={handleSend}
          onUpload={handleUpload}
          uploading={uploading}
          uploadProgress={uploadProgress}
          uploadedFiles={uploadedFiles}
        />
      </main>
    </div>
  );
}
