import { FaUser, FaRobot } from "react-icons/fa";

const ChatMessage = ({ message }) => {
  const isUser = message.role === "user";

  return (
    <div
      className={`d-flex ${
        isUser ? "justify-content-end" : "justify-content-start"
      }`}
    >
      <div
        className={`chat-message-bubble ${
          isUser
            ? "chat-message-bubble--user"
            : "chat-message-bubble--assistant"
        }`}
      >
        <div className="d-flex align-items-center gap-2 mb-1">
          <span className="chat-sender">
            {isUser ? (
              <>
                <FaUser size={12} className="me-1" /> You
              </>
            ) : (
              <>
                <FaRobot size={12} className="me-1" /> AI Assistant
              </>
            )}
          </span>

          <span className="chat-timestamp">
            {new Date(message.timestamp).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>

        <p className="mb-0" style={{ whiteSpace: "pre-wrap" }}>
          {message.content}
        </p>

        {/* Metadata section kept commented out as in original */}
      </div>
    </div>
  );
};

export default ChatMessage;