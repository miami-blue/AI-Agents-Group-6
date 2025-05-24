import React from 'react';
import './card.css';
import GoalProgressBar from './GoalProgressBar';

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
        <GoalProgressBar progress={progress} />
        <div className="target-date"> {targetDate} </div>
      </div>
    </div>
  );
};

export default GoalCard;
