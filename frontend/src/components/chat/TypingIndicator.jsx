import { FaRobot } from "react-icons/fa";

const TypingIndicator = () => {
  return (
    <div className="d-flex justify-content-start">
      <div className="typing-indicator-bubble">
        <div className="d-flex align-items-center gap-2">
          <FaRobot size={14} className="text-muted" />
          <small className="fw-semibold text-muted">AI Assistant</small>
          <div className="d-flex gap-1 typing-dots">
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;