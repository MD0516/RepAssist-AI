const InteractionField = ({ label, value, multiline = false }) => {
  const isEmpty = value === "" || value === null || value === undefined;
  const displayValue = isEmpty ? "-" : value;

  return (
    <div className="interaction-field">
      <p className="interaction-field-label">{label}</p>
      {multiline ? (
        <p className="interaction-field-value interaction-field-value--multiline">
          {displayValue}
        </p>
      ) : (
        <p
          className={`interaction-field-value ${
            isEmpty ? "interaction-field-value--empty" : ""
          }`}
        >
          {displayValue}
        </p>
      )}
    </div>
  );
};

export default InteractionField;