import React from 'react';
import './streakCard.css'; // external CSS

type StreakCardProps = {
    streakCount: number;
    streakHistory: boolean[];
};

const StreakCard: React.FC<StreakCardProps> = ({ streakCount, streakHistory }) => {
    return (
        <div className= "streak-card" >
        <div className="icon-circle" >
            <h2 className = "rocket-icon" > 🚀 </h2>
                < /div>
                < div className = "streak-text" >
                    <h2><strong>{ streakCount } < /strong> months</h2 >
                    <p>in a row! < /p>
                        < /div>
                        < div className = "dots-row" >
                            {
                                streakHistory.map((filled, index) => (
                                    <span
            key= { index }
            className = {`dot ${filled ? 'filled' : 'empty'}`}
                            />
        ))}
</div>
    < /div>
  );
};

export default StreakCard;
