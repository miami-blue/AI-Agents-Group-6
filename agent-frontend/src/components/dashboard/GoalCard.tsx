import React from 'react';
import './card.css';

type GoalCardProps = {
    title: string;
    targetDate: string;
    progress: number;
};

const GoalCard: React.FC<GoalCardProps> = ({ title, targetDate, progress, imageUrl }) => {
    return (
        <div className= "goal-card" >
        <div className="goal-tag" > My final goal < /div>
            < h1 className = "goal-image" > 🏡 </h1>
                < h2 className = "goal-title" > { title } < /h2>
                    < div className = "progress-section" >
                        <div className="progress-bar" >
                            <div
            className="progress-fill"
    style = {{ width: `${progress}%` }
}
          > </div>
    < /div>
    < div className = "target-date" > { targetDate } < /div>
        < /div>
        < /div>
  );
};

export default GoalCard;

