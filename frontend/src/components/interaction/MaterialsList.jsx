import { FaFile } from "react-icons/fa";

const MaterialsList = ({ materials = [] }) => {
  if (!materials.length) {
    return (
      <div className="interaction-field bg-white text-muted">
        <span className="interaction-field-value--empty">-</span>
      </div>
    );
  }

  return (
    <div className="materials-list">
      {materials.map((material, index) => (
        <span
          key={`${material}-${index}`}
          className="material-tag"
        >
          <FaFile className="material-icon" size={12} />
          {material}
        </span>
      ))}
    </div>
  );
};

export default MaterialsList;