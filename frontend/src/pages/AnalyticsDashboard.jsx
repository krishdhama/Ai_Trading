// Behavior and performance analytics page.
import BehaviorBadge from "../components/BehaviorBadge";
import PopupFeedback from "../components/PopupFeedback";
import XPBadge from "../components/XPBadge";

export default function AnalyticsDashboard() {
  return (
    <section className="grid analytics-grid">
      <div className="panel">
        <h2>Behavior Analytics</h2>
        <BehaviorBadge label="Disciplined" />
        <BehaviorBadge label="Panic Sell" />
        <BehaviorBadge label="FOMO Buy" />
      </div>
      <PopupFeedback />
      <XPBadge xp={120} />
    </section>
  );
}
