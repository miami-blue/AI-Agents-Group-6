import React, { useEffect, useState } from 'react';
import './card.css';
import { useDataContext } from '../../api/DataContext';

const GoalCard = () => {
  const { goalsResponse } = useDataContext();

  // The largest goal is considered the "dream"
  // Excluding the dream, find the goal that is due next
  const dream =
    goalsResponse.data.length > 0
      ? goalsResponse.data.reduce(
          (prev, current) =>
            current.target_amount > prev.target_amount ? current : prev,
          goalsResponse.data[0]
        )
      : undefined;

  const goalsExcludingDream = goalsResponse.data
    .filter((goal) => goal.id !== dream?.id)
    .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime());

  const nextGoal =
    goalsExcludingDream.length > 0
      ? goalsExcludingDream.reduce(
          (prev, current) =>
            current.due_date < prev.due_date ? current : prev,
          goalsExcludingDream[0]
        )
      : undefined;

      const [selectedGoal, setSelectedGoal] = useState(nextGoal)

      useEffect(() => {
        if (nextGoal) {
          setSelectedGoal(nextGoal)
        }
      }, [nextGoal?.id])

  const formattedDueDate = selectedGoal?.due_date
    ? new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
      }).format(new Date(selectedGoal.due_date))
    : undefined;


  return (
    <div className="card">
      <div className="goal-tag">My goal</div>
      <h1 className="goal-image">{'🎯'}</h1>
      <h2 className="title">{selectedGoal?.goal_name} </h2>
      <div className="subtitle">{formattedDueDate}</div>

      <div className="progress-section">
        <div className="progress-bar">
          <div className="progress-fill-goal" style={{ width: `${0}%` }}>
            {' '}
          </div>
        </div>
        <div className="progress-target">{selectedGoal?.target_amount} €</div>
      </div>

<div className='dots-row'>
      {goalsExcludingDream.map((goal, index) => (
     
            <div role='button'
             onClick={() => setSelectedGoal(goal)}
             key={index}
              className={`dot ${selectedGoal?.id === goal.id ? 'filled' : 'not-selected'}`}
            />

      ))}
</div>
    </div>
  );
};

export default GoalCard;
