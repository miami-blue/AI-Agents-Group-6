import BudgetPie from './BudgetPie';
import GoalCard from './GoalCard';
import ChallengeCard from './ChallengeCard';
import StreakCard from './StreakCard';
import MonthlyBudgetCard from './MonthlyBudgetCard';
import DreamCard from './DreamCard';
import './dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard">
      <DreamCard />

      <ChallengeCard
        challenge="Eat Wolt less than 2 times a week"
        targetDate="May 2027"
      />
      <div className="small-card">
        <GoalCard />

        <StreakCard
          streakCount={2}
          streakHistory={[true, false, false, true, false, true, true]}
        />
      </div>
      <BudgetPie />

      <MonthlyBudgetCard  />
    </div>
  );
}

export default Dashboard;
