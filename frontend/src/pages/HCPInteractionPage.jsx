import DashboardLayout from "../layouts/DashboardLayout";

import InteractionPanel from "../components/interaction/InteractionPanel";
import ChatPanel from "../components/chat/ChatPanel";

const HCPInteractionPage = () => {
  return (
    <DashboardLayout
      leftPanel={<InteractionPanel />}
      rightPanel={<ChatPanel />}
    />
  );
};

export default HCPInteractionPage;