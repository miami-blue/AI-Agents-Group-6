import BudgetPie from './BudgetPie';
import GoalCard from './GoalCard';
import ChallengeCard from './ChallengeCard';
import StreakCard from './StreakCard';
import './dashboard.css'

function Dashboard() {
    return (
        <div className= 'dashboard' >
        <GoalCard
        title= "My first house"
    emoji = "🏡"
    targetDate = "May 2027"
    progress = { 10}
        />
        <ChallengeCard
        challenge= "Eat Wolt less than 2 times a week"
    targetDate = "May 2027" />
        <div className='small-card' >
            <GoalCard
        title= "Pizza Oven"
    emoji = "🍕"
    progress = { 50}
        />
        <StreakCard
    streakCount = { 2 }
    streakHistory = { [true, false, false, true, false, false, false]}
        />
        < /div>
        < BudgetPie />
        </div>
    );
}

export default Dashboard;