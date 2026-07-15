import React from "react";

const DashboardLayout = ({ leftPanel, rightPanel }) => {
  return (
    <div className="dashboard-layout">
      <div className="container-fluid h-100 p-0">
        <div className="row h-100 g-0">
          {/* Left Panel — Interaction Details */}
          <div className="col-12 col-xl-5 h-100 p-3">
            <div className="panel-wrapper h-100">
              {leftPanel}
            </div>
          </div>

          {/* Right Panel — AI Chat */}
          <div className="col-12 col-xl-7 h-100 p-3">
            <div className="panel-wrapper h-100">
              {rightPanel}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;