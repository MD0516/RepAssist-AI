import { FaArrowUp, FaArrowRight, FaArrowDown } from "react-icons/fa";

const sentimentConfig = {
  positive: {
    className: "sentiment-badge--positive",
    icon: FaArrowUp,
    label: "Positive",
  },
  neutral: {
    className: "sentiment-badge--neutral",
    icon: FaArrowRight,
    label: "Neutral",
  },
  negative: {
    className: "sentiment-badge--negative",
    icon: FaArrowDown,
    label: "Negative",
  },
};

const SentimentBadge = ({ sentiment }) => {
  if (!sentiment) {
    return (
      <div className="interaction-field bg-white text-muted">
        <span className="interaction-field-value--empty">-</span>
      </div>
    );
  }

  const config = sentimentConfig[sentiment.toLowerCase()];
  
  if (!config) {
    return (
      <div className="interaction-field bg-white text-muted">
        <span className="interaction-field-value--empty">-</span>
      </div>
    );
  }

  const Icon = config.icon;

  return (
    <span className={`sentiment-badge ${config.className}`}>
      <Icon className="sentiment-icon" size={14} />
      {config.label}
    </span>
  );
};

export default SentimentBadge;