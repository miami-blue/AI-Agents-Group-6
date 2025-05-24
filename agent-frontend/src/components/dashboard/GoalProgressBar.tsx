import React from 'react';
import './card.css';

type GoalProgressBarProps = {
  progress: number;
};

const GoalProgressBar: React.FC<GoalProgressBarProps> = ({ progress }) => (
  <div className="progress-bar">
    <div className="progress-fill-goal" style={{ width: `${progress}%` }}>
      {' '}
    </div>
  </div>
);

export default GoalProgressBar;
