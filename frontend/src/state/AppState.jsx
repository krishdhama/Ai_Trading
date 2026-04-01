// Global app state for portfolio, trades, behavior, and AI feedback.
import { createContext, useContext, useState } from "react";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [portfolio, setPortfolio] = useState({
    cash: 10000,
    holdings: {},
    total_value: 10000,
  });
  const [trades, setTrades] = useState([]);
  const [behavior, setBehavior] = useState([]);
  const [feedback, setFeedback] = useState("");

  const value = {
    portfolio,
    setPortfolio,
    trades,
    setTrades,
    behavior,
    setBehavior,
    feedback,
    setFeedback,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useAppState() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppState must be used within an AppProvider");
  }
  return context;
}
