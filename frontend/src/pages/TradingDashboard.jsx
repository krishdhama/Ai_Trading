// Core trading interface page.
import Chart from "../components/Chart";
import PortfolioCard from "../components/PortfolioCard";
import TradePanel from "../components/TradePanel";
import AIFeedbackCard from "../components/AIFeedbackCard";

export default function TradingDashboard() {
  return (
    <section className="grid two-column">
      <Chart />
      <TradePanel />
      <PortfolioCard />
      <AIFeedbackCard />
    </section>
  );
}
