import './Message.css';

export default function Message({ role, content, timestamp }) {
  const isUser = role === 'user';

  const formatTime = (ts) =>
    new Date(ts).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  // Simple markdown-like rendering
  const renderContent = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    const elements = [];
    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      if (line.startsWith('```')) {
        const codeLines = [];
        i++;
        while (i < lines.length && !lines[i].startsWith('```')) {
          codeLines.push(lines[i]);
          i++;
        }
        elements.push(
          <pre key={i} className="msg-code">
            <code>{codeLines.join('\n')}</code>
          </pre>
        );
      } else if (line.startsWith('### ')) {
        elements.push(<h3 key={i} className="msg-h3">{line.slice(4)}</h3>);
      } else if (line.startsWith('## ')) {
        elements.push(<h2 key={i} className="msg-h2">{line.slice(3)}</h2>);
      } else if (line.startsWith('**') && line.endsWith('**')) {
        elements.push(<p key={i} className="msg-bold">{line.slice(2, -2)}</p>);
      } else if (line.startsWith('- ') || line.startsWith('• ')) {
        elements.push(<li key={i} className="msg-li">{line.slice(2)}</li>);
      } else if (line.trim() === '') {
        elements.push(<br key={i} />);
      } else {
        // inline bold/italic
        const formatted = line
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          .replace(/\*(.*?)\*/g, '<em>$1</em>')
          .replace(/`(.*?)`/g, '<code class="msg-inline-code">$1</code>');
        elements.push(
          <p key={i} dangerouslySetInnerHTML={{ __html: formatted }} className="msg-p" />
        );
      }
      i++;
    }
    return elements;
  };

  return (
    <div className={`message-row ${isUser ? 'user' : 'ai'}`}>
      {!isUser && (
        <div className="msg-avatar ai-avatar">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      )}
      <div className="msg-wrapper">
        <div className={`msg-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
          {isUser
            ? <p className="msg-p">{content}</p>
            : <div className="msg-content">{renderContent(content)}</div>
          }
        </div>
        <div className={`msg-footer ${isUser ? 'user-footer' : ''}`}>
          <span className="msg-time">{formatTime(timestamp)}</span>
          {isUser && (
            <svg className="msg-check" width="12" height="12" viewBox="0 0 24 24" fill="none">
              <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </div>
      </div>
      {isUser && (
        <div className="msg-avatar user-avatar">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      )}
    </div>
  );
}
