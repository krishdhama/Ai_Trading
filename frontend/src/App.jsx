// Minimal app shell with simple page switching for hackathon speed.
import { useState } from "react";

import Home from "./pages/Home";
import TradingDashboard from "./pages/TradingDashboard";
import AnalyticsDashboard from "./pages/AnalyticsDashboard";
import { AppProvider } from "./state/AppState";

const pages = {
  home: Home,
  trading: TradingDashboard,
  analytics: AnalyticsDashboard,
};

export default function App() {
  const [page, setPage] = useState("home");
  const ActivePage = pages[page];

  return (
    <AppProvider>
      <div className="app-shell">
        <header className="topbar">
          <h1>AI-Powered Trading Psychology Trainer</h1>
          <nav>
            <button onClick={() => setPage("home")}>Home</button>
            <button onClick={() => setPage("trading")}>Trading Dashboard</button>
            <button onClick={() => setPage("analytics")}>Analytics Dashboard</button>
          </nav>
        </header>
        <main className="page-container">
          <ActivePage />
        </main>
      </div>
    </AppProvider>
  );
}
