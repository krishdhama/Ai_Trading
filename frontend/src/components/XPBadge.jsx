// XP display for habit-building gamification.
export default function XPBadge({ xp }) {
  return (
    <div className="panel">
      <h3>XP Badge</h3>
      <p>{xp} XP earned</p>
    </div>
  );
}
