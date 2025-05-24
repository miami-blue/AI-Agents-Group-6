import React from 'react';
import './card.css';

type GoalCardProps = {
  title: string;
  emoji: string;
  targetDate?: string;
  progress: number;
};

const GoalCard: React.FC<GoalCardProps> = ({
  title,
  emoji,
  targetDate,
  progress,
}) => {
  return (
    <div className="card">
      <div className="goal-tag"> My goal </div>
      <h1 className="goal-image">{emoji} </h1>
      <h2 className="title"> {title} </h2>
      <div className="progress-section">
        <div className="progress-bar">
          <div className="progress-fill-goal" style={{ width: `${progress}%` }}>
            {' '}
          </div>
        </div>
        <div className="target-date"> {targetDate} </div>
      </div>
    </div>
  );
};

export default GoalCard;
