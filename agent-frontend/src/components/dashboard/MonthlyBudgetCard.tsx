import React, { useState } from 'react';
import './monthlyBudgetCard.css'; // for styling

import SummaryWidget from '../summary/SummaryWidget';
import { useDataContext } from '../../api/DataContext';

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

  const [showSummary, setShowSummary] = useState(false);
  const { goalsResponse } = useDataContext();

  // Since i don't have the real data I created  Mock data for current and previous month expenses by category
  const currentMonthExpenses = [
    { name: 'Groceries', value: 500 },
    { name: 'Travels', value: 250 },
    { name: 'Shopping', value: 200 },
    { name: 'Dinners', value: 300 },
  ];
  const previousMonthExpenses = [
    { name: 'Groceries', value: 400 },
    { name: 'Travels', value: 100 },
    { name: 'Shopping', value: 300 },
    { name: 'Dinners', value: 350 },
  ];

  // Most spend on
  const mostSpend = currentMonthExpenses.reduce((max, curr) =>
    curr.value > max.value ? curr : max
  );

  const deltas = currentMonthExpenses.map((curr) => {
    const prev = previousMonthExpenses.find((p) => p.name === curr.name);
    return {
      name: curr.name,
      delta: prev ? curr.value - prev.value : curr.value,
      current: curr.value,
      previous: prev ? prev.value : 0,
    };
  });

  const biggestIncrease = deltas.reduce((max, curr) =>
    curr.delta > max.delta ? curr : max
  );
  const biggestDecrease = deltas.reduce((min, curr) =>
    curr.delta < min.delta ? curr : min
  );

  const savedAmount = budgetLimit - expensesTotal;
  // Count completed challenges (mock: 1 if challenge exists and is completed)
  const completedChallenges = 1;
  // Count completed goals (progress === 100)
  const completedGoals = goalsResponse.data.filter(
    (goal: any) => goal.progress === 100
  ).length;

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

      <button className="wrap-up-button" onClick={() => setShowSummary(true)}>
        📊 View April Wrap Up
      </button>

      {showSummary && (
        <SummaryWidget
          savedAmount={savedAmount}
          completedChallenges={completedChallenges}
          completedGoals={completedGoals}
          mostSpendCategory={mostSpend.name}
          mostSpendAmount={mostSpend.value}
          biggestIncreaseCategory={biggestIncrease.name}
          biggestIncreaseDelta={biggestIncrease.delta}
          biggestDecreaseCategory={biggestDecrease.name}
          biggestDecreaseDelta={biggestDecrease.delta}
          onClose={() => setShowSummary(false)}
        />
      )}
    </div>
  );
};

export default MonthlyBudgetCard;
