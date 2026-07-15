import { useDispatch, useSelector } from "react-redux";

import InteractionField from "./InteractionField";
import MaterialsList from "./MaterialsList";
import SentimentBadge from "./SentimentBadge";
import CallPrepCard from "./CallPrepCard";
import InteractionTable from "./InteractionTable";
import { formatTime } from "../../Utils";
import { FaClock, FaFileAlt, FaTable } from "react-icons/fa";
import { setViewMode } from "../../redux/slices/interactionSlice";

const InteractionPanel = () => {
  const dispatch = useDispatch()
  const { viewMode, activeInteraction, lastUpdated, interactionList } = useSelector(
    (state) => state.interaction
  );

  if (viewMode === "table") {
    return <InteractionTable />;
  }


  const interaction = activeInteraction || {};

  return (
    <div className="card border-0 shadow-sm h-100 d-flex flex-column interaction-panel">
      <div className="card-body p-4 overflow-auto interaction-panel-body">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-start mb-4">
          <div>
            <h4 className="fw-semibold mb-1 d-flex align-items-center gap-2">
              <FaFileAlt className="text-primary" size={18} />
              Interaction Details
            </h4>
            <p className="text-secondary mb-0 small">AI-generated summary</p>
          </div>

          <div className="d-flex align-items-center gap-2">
            {interactionList?.length > 0 && (
              <button
                className="btn btn-sm mode-btn d-flex align-items-center gap-2"
                onClick={() =>
                  dispatch(setViewMode("table"))
                }
              >
                <FaTable size={12} />
                Interactions ({interactionList.length})
              </button>
            )}
            {lastUpdated && (
              <div className="d-flex align-items-center gap-1 text-tertiary small">
                <FaClock size={12} />
                <span>Updated {formatTime(lastUpdated, { showTime: true })}</span>
              </div>
            )}
          </div>
        </div>

        {/* Fields */}
        <div className="d-flex flex-column gap-3">
          <InteractionField label="HCP Name" value={interaction.hcpName} />

          <InteractionField
            label="Interaction Date"
            value={formatTime(interaction.interactionDate, { showTime: true })}
          />

          <InteractionField
            label="Interaction Type"
            value={interaction.interactionType}
          />

          <InteractionField
            label="Product Discussed"
            value={interaction.productDiscussed}
          />

          <div>
            <p className="text-tertiary small fw-semibold mb-2">Sentiment</p>
            <SentimentBadge sentiment={interaction.sentiment} />
          </div>

          <div>
            <p className="text-tertiary small fw-semibold mb-2">Materials Shared</p>
            <MaterialsList materials={interaction.materialsShared} />
          </div>

          <InteractionField
            label="Key Discussion Points"
            value={interaction.keyDiscussionPoints}
            multiline
          />

          <InteractionField
            label="Follow-up Required"
            value={
              interaction.followUpRequired === null ||
                interaction.followUpRequired === undefined
                ? "-"
                : interaction.followUpRequired
                  ? "Yes"
                  : "No"
            }
          />

          <InteractionField
            label="Follow-up Notes"
            value={interaction.followUpNotes}
            multiline
          />

          <CallPrepCard interaction={interaction} />
        </div>
      </div>
    </div>
  );
};

export default InteractionPanel;