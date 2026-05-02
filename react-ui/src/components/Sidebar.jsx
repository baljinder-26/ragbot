import { useState } from 'react';
import './Sidebar.css';

export default function Sidebar({
  sessions,
  activeSession,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  uploadedFiles,
  onDeleteFile,
  collapsed,
  onToggleCollapse,
}) {
  const [hoveredSession, setHoveredSession] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);

  const formatTime = (ts) => {
    const d = new Date(ts);
    const now = new Date();
    const diffMs = now - d;
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const getSessionPreview = (session) => {
    const msgs = session.messages.filter((m) => m.role === 'user');
    if (msgs.length === 0) return 'New conversation';
    return msgs[0].content.slice(0, 45) + (msgs[0].content.length > 45 ? '…' : '');
  };

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (confirmDelete === id) {
      onDeleteSession(id);
      setConfirmDelete(null);
    } else {
      setConfirmDelete(id);
      setTimeout(() => setConfirmDelete(null), 2500);
    }
  };

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Header */}
      <div className="sidebar-header">
        {!collapsed && (
          <div className="sidebar-brand">
            <div className="brand-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span className="brand-name">Nexus RAG</span>
          </div>
        )}
        <button className="collapse-btn" onClick={onToggleCollapse} title={collapsed ? 'Expand' : 'Collapse'}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            {collapsed
              ? <path d="M9 18l6-6-6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              : <path d="M15 18l-6-6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            }
          </svg>
        </button>
      </div>

      {/* New Chat Button */}
      <div className="sidebar-new">
        <button className="new-chat-btn" onClick={onNewChat}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
          </svg>
          {!collapsed && <span>New Chat</span>}
        </button>
      </div>

      {/* Sessions */}
      {!collapsed && (
        <div className="sidebar-section">
          <div className="section-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Recent Chats
          </div>
          <div className="sessions-list">
            {sessions.length === 0 && (
              <div className="empty-sessions">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <p>No chats yet</p>
              </div>
            )}
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`session-item ${activeSession === session.id ? 'active' : ''}`}
                onClick={() => onSelectSession(session.id)}
                onMouseEnter={() => setHoveredSession(session.id)}
                onMouseLeave={() => setHoveredSession(null)}
              >
                <div className="session-icon">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div className="session-content">
                  <div className="session-preview">{getSessionPreview(session)}</div>
                  <div className="session-meta">
                    <span className="session-time">{formatTime(session.updatedAt)}</span>
                    <span className="session-count">{session.messages.length} msgs</span>
                  </div>
                </div>
                {(hoveredSession === session.id || activeSession === session.id) && (
                  <button
                    className={`session-delete ${confirmDelete === session.id ? 'confirm' : ''}`}
                    onClick={(e) => handleDelete(e, session.id)}
                    title={confirmDelete === session.id ? 'Click again to confirm' : 'Delete chat'}
                  >
                    {confirmDelete === session.id
                      ? <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
                      : <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg>
                    }
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Uploaded PDFs */}
      {!collapsed && uploadedFiles.length > 0 && (
        <div className="sidebar-section sidebar-files">
          <div className="section-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Uploaded PDFs
            <span className="file-count">{uploadedFiles.length}</span>
          </div>
          <div className="files-list">
            {uploadedFiles.map((f, i) => (
              <div key={i} className="file-item">
                <div className="file-icon">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <span className="file-name" title={f}>{f}</span>
                <button className="file-delete" onClick={() => onDeleteFile(f)} title="Remove">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      {!collapsed && (
        <div className="sidebar-footer">
          <div className="footer-status">
            <span className="status-dot"></span>
            <span>API Connected</span>
          </div>
        </div>
      )}
    </aside>
  );
}
