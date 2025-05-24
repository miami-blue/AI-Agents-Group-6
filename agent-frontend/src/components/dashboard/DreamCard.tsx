import React from 'react';
import './card.css';

type DreamCardProps = {
  title: string;
  emoji: string;
  targetDate: string;
  progress: number;
};

const DreamCard: React.FC<DreamCardProps> = ({
  title,
  emoji,
  targetDate,
  progress,
}) => {
  return (
    <div className="card">
      <div className="dream-tag"> My dream </div>
      <h1 className="dream-image">{emoji} </h1>
      <h2 className="title"> {title} </h2>
      <div className="progress-section">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}>
            {' '}
          </div>
        </div>
        <div className="target-date"> {targetDate} </div>
      </div>
    </div>
  );
};

export default DreamCard;
