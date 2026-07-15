import { useDispatch, useSelector } from "react-redux";

import {
    setActiveInteraction,
    setViewMode,
} from "../../redux/slices/interactionSlice";
import { formatTime } from "../../Utils";
import { FaChevronRight, FaFileAlt, FaInbox } from "react-icons/fa";

const InteractionTable = () => {
    const dispatch = useDispatch();

    const interactionList = useSelector(
        (state) => state.interaction.interactionList
    );

    const handleSelect = (interaction) => {
        dispatch(setActiveInteraction(interaction));
        dispatch(setViewMode("form"));
    };

    const capitalize = (str) => {
        if (!str) return "-";
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    };

    if (!interactionList.length) {
        return (
            <div className="card border-0 shadow-sm h-100 d-flex flex-column">
                <div className="card-body p-4 d-flex flex-column align-items-center justify-content-center text-center">
                    <FaInbox className="text-tertiary mb-3" size={48} />
                    <h5 className="fw-semibold mb-1">No Interactions Found</h5>
                    <p className="text-muted small mb-0">
                        Describe an interaction in the chat to generate a record.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="card border-0 shadow-sm h-100 d-flex flex-column">
            <div className="card-body p-0 overflow-hidden d-flex flex-column h-100">
                <div className="d-flex justify-content-between align-items-center px-4 py-3 border-bottom">
                    <div>
                        <h5 className="fw-semibold mb-0">Interaction Results</h5>
                        <p className="text-secondary mb-0 small">Click a row to open details</p>
                    </div>
                    <button
                        className="btn btn-sm mode-btn d-flex align-items-center gap-2"
                        onClick={() =>
                            dispatch(setViewMode("form"))
                        }
                    >
                        <FaFileAlt size={12} />
                        Form View
                    </button>
                </div>

                <div className="table-responsive flex-grow-1 overflow-auto">
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th>HCP Name</th>
                                <th>Date</th>
                                <th>Product</th>
                                <th>Sentiment</th>
                                <th>Follow Up</th>
                                <th className="text-end" style={{ width: "40px" }}></th>
                            </tr>
                        </thead>
                        <tbody>
                            {interactionList.map((interaction) => (
                                <tr
                                    key={interaction.id}
                                    onClick={() => handleSelect(interaction)}
                                    className="interaction-row"
                                >
                                    <td className="fw-medium">{interaction.hcpName}</td>
                                    <td>{formatTime(interaction.interactionDate)}</td>
                                    <td>{interaction.productDiscussed}</td>
                                    <td>
                                        {/* Improved Sentiment Badge */}
                                        <span
                                            className={`badge rounded px-3 ${interaction.sentiment === "positive"
                                                ? "badge-success"
                                                : interaction.sentiment === "neutral"
                                                    ? "badge-warning"
                                                    : interaction.sentiment === "negative"
                                                        ? "badge-danger"
                                                        : "badge-secondary"
                                                }`}
                                        >
                                            {capitalize(interaction.sentiment) || "-"}
                                        </span>
                                    </td>
                                    <td>
                                        {/* Improved Follow-Up Badge */}
                                        <span
                                            className={`badge rounded px-3 ${interaction.followUpRequired
                                                ? "badge-warning"
                                                : "badge-success"
                                                }`}
                                        >
                                            {interaction.followUpRequired ? "Yes" : "No"}
                                        </span>
                                    </td>
                                    <td className="text-end">
                                        <FaChevronRight className="text-tertiary" size={14} />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default InteractionTable;