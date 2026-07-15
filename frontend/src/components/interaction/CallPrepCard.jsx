import InteractionField from "./InteractionField";
import { FaClipboardList } from "react-icons/fa";

const CallPrepCard = ({ interaction }) => {
  const hasCallPrep =
    interaction?.callPrepTopics ||
    interaction?.callPrepMaterials ||
    interaction?.callPrepSentimentTrend ||
    interaction?.callPrepTalkingPoints ||
    interaction?.callPrepNextBestAction;

  if (!hasCallPrep) return null;

  return (
    <div className="call-prep-card">
      <div className="call-prep-title">
        <FaClipboardList className="call-prep-icon" size={18} />
        Call Preparation
      </div>

      <div className="d-flex flex-column gap-3">
        <InteractionField
          label="Topics Previously Discussed"
          value={interaction.callPrepTopics}
          multiline
        />

        <InteractionField
          label="Materials Already Shared"
          value={interaction.callPrepMaterials}
          multiline
        />

        <InteractionField
          label="Sentiment Trend"
          value={interaction.callPrepSentimentTrend}
        />

        <InteractionField
          label="Recommended Talking Points"
          value={interaction.callPrepTalkingPoints}
          multiline
        />

        <InteractionField
          label="Next Best Action"
          value={interaction.callPrepNextBestAction}
          multiline
        />
      </div>
    </div>
  );
};

export default CallPrepCard;