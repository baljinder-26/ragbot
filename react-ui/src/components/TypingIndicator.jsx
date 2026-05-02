import './TypingIndicator.css';

export default function TypingIndicator() {
  return (
    <div className="typing-wrapper">
      <div className="typing-avatar">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
      <div className="typing-bubble">
        <span className="dot" style={{ animationDelay: '0ms' }}></span>
        <span className="dot" style={{ animationDelay: '160ms' }}></span>
        <span className="dot" style={{ animationDelay: '320ms' }}></span>
      </div>
    </div>
  );
}
