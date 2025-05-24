import React from 'react';
import './card.css';
import { useDataContext } from '../../api/DataContext';

const DreamCard = () => {
  const { goalsResponse } = useDataContext();

  // The largest goal is considered the "dream"
  const dream =
    goalsResponse.data.length > 0
      ? goalsResponse.data.reduce(
          (prev, current) =>
            current.target_amount > prev.target_amount ? current : prev,
          goalsResponse.data[0]
        )
      : undefined;

  const formattedDueDate = dream?.due_date
    ? new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
      }).format(new Date(dream.due_date))
    : undefined;

  return (
    <div className="card">
      <div className="dream-tag">My dream</div>
      <h1 className="dream-image">{'⭐'}</h1>
      <h2 className="title"> {dream?.goal_name}</h2>
      <div className="subtitle">{formattedDueDate}</div>

      <div className="progress-section">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${0}%` }}>
            {' '}
          </div>
        </div>
        <div className="progress-target"> {dream?.target_amount} €</div>
      </div>
    </div>
  );
};

export default DreamCard;
