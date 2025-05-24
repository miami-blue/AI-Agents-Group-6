import React from 'react';
import './monthlyBudgetCard.css'; // for styling

type MonthlyBudgetCardProps = {
  budgetLimit: number;
  expensesTotal: number;
  daysLeft?: number; // optional for flexibility
};

const MonthlyBudgetCard: React.FC<MonthlyBudgetCardProps> = ({
  budgetLimit,
  expensesTotal,
  daysLeft = 30, // fallback
}) => {
  const progress = (expensesTotal / budgetLimit) * 100;
  const remainingBudget = budgetLimit - expensesTotal;
  const dailyBudget =
    daysLeft > 0 ? (remainingBudget / daysLeft).toFixed(2) : '0.00';

  return (
    <div className="budget-card">
      <div className="card-header">
        <h2>Monthly Budget </h2>
        <span className="budget-tag">
          €{expensesTotal} /{budgetLimit}
        </span>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <p className="daily-budget-text">
        You can spend<strong>€{dailyBudget} </strong>/day for {daysLeft} days
      </p>

      <button className="wrap-up-button">📊 View April Wrap Up</button>
    </div>
  );
};

export default MonthlyBudgetCard;
