import BudgetPie from './BudgetPie'
import GoalCard from './GoalCard';

function Dashboard() {
    return (
        <div>
        <GoalCard
        title= "My first house"
    targetDate = "May 2027"
    progress = { 10}
        />
        <h1>Budget Overview < /h1>
            < BudgetPie />
            </div>
    );
}

export default Dashboard;