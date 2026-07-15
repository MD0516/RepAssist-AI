import { createRoot } from 'react-dom/client'
import "@fontsource/inter";
import "bootstrap/dist/css/bootstrap.min.css"
import './global.css'
import { Provider } from 'react-redux'
import HCPInteractionPage from './pages/HCPInteractionPage.jsx'
import { store } from './redux/store.js';

createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <HCPInteractionPage />
  </Provider>,
)
