import { useState, useRef } from "react"; // Added useRef
import { useDispatch, useSelector } from "react-redux";
import { addMessage, setTyping } from "../../redux/slices/chatSlice";
import {
  setActiveInteraction,
  setInteractionList,
  setViewMode,
} from "../../redux/slices/interactionSlice";
import api from "../../services/api";
import { FaPaperPlane } from "react-icons/fa";

const ChatInput = () => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef(null);

  const dispatch = useDispatch();
  const activeInteraction = useSelector(
    (state) => state.interaction.activeInteraction
  );

  const autoGrowTextarea = (element) => {
    if (element) {
      element.style.height = "auto";
      element.style.height = `${element.scrollHeight}px`;
    }
  };

  const handleSend = async () => {
    if (!message.trim()) return;

    const text = message.trim();

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: new Date().toISOString(),
    };

    dispatch(addMessage(userMessage));
    setMessage("");
    dispatch(setTyping(true));

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    try {
      const response = await api.post("/chat", {
        message: text,
        interactionId: activeInteraction?.id || null,
      });

      const data = response.data;

      dispatch(
        addMessage({
          ...data.message,
          metadata: data.metadata || null,
        })
      );

      if (data.interaction) {
        dispatch(setActiveInteraction(data.interaction));
        dispatch(setViewMode("form"));
      }

      if (data.metadata?.interactionList) {
        dispatch(setInteractionList(data.metadata.interactionList));
        dispatch(setViewMode("table"));
      }
    } catch (error) {
      dispatch(
        addMessage({
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Unable to contact AI service. Please try again.",
          timestamp: new Date().toISOString(),
        })
      );
      console.error(error);
    } finally {
      dispatch(setTyping(false));
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input-wrapper">
      <div className="d-flex gap-2 align-items-end chat-input-container">
        <textarea
          ref={textareaRef}
          className="form-control chat-textarea"
          rows={1}
          placeholder="Describe your interaction with the HCP..."
          value={message}
          onChange={(e) => {
            setMessage(e.target.value);
            autoGrowTextarea(e.target);
          }}
          onKeyDown={handleKeyDown}
        />

        <button
          className="btn btn-primary send-button"
          onClick={handleSend}
          disabled={!message.trim()}
          aria-label="Send message"
        >
          <FaPaperPlane size={16} />
          <span className="send-text">Send</span>
        </button>
      </div>
    </div>
  );
};

export default ChatInput;