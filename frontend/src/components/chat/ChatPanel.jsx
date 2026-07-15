import { useSelector } from "react-redux";
import { useEffect, useRef } from "react"; // Added useRef and useEffect

import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import { FaRobot } from "react-icons/fa";

const ChatPanel = () => {
  const { messages, typing } = useSelector((state) => state.chat);
  
  // 1. Create a ref for the messages container
  const messagesEndRef = useRef(null);

  // 2. Function to scroll to the bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 3. Trigger scroll whenever 'messages' or 'typing' changes
  useEffect(() => {
    scrollToBottom();
  }, [messages, typing]);

  return (
    <div className="card border-0 shadow-sm h-100 d-flex flex-column chat-panel">
      {/* Header - Fixed */}
      <div className="card-header bg-white border-bottom py-3 px-4 flex-shrink-0">
        <div className="d-flex align-items-center gap-3">
          <div className="avatar avatar--ai">
            <FaRobot size={20} />
          </div>
          <div>
            <h5 className="mb-0 fw-semibold">AI Assistant</h5>
            <small className="text-muted">Describe your interaction naturally</small>
          </div>
        </div>
      </div>

      {/* Messages - Scrollable */}
      <div className="flex-grow-1 overflow-auto p-4 chat-messages-container">
        <div className="d-flex flex-column gap-3">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {typing && <TypingIndicator />}
          
          {/* 4. The invisible div that acts as the anchor at the bottom */}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input - Fixed at bottom */}
      <div className="border-top p-3 bg-white flex-shrink-0 chat-input-container">
        <ChatInput />
      </div>
    </div>
  );
};

export default ChatPanel;