import React, { useState } from 'react';
import './monthlyBudgetCard.css'; // for styling
import { useDataContext } from '../../api/DataContext';

type MonthlyBudgetCardProps = {

};

const MonthlyBudgetCard= () => {
const [selectedMonth, setSelectedMonth] = useState('06')

  const {budgetsResponse} = useDataContext()
  
  const budget = budgetsResponse.data.filter(item => !!item.Month && item.Month === `2025-${selectedMonth}`)
  
  const expenses = 0
  const budgetedExpenses = budget.filter(item => item.Category !== 'Income')
  const income = (budget.find(item => item.Category === 'Income')?.Amount as number) || 0

  const budgetedTotal = budgetedExpenses.reduce((sum, item) => {
    const amount = parseFloat(item.Amount);
    return sum + (isNaN(amount) ? 0 : amount);
  }, 0);

  const daysLeft = 27


  const progress = budgetedTotal > 0 ? (expenses / budgetedTotal) * 100 : 0
  const remainingBudget = budgetedTotal - expenses;
  const dailyBudget =
    daysLeft > 0 ? (remainingBudget / daysLeft).toFixed(2) : '0.00';

  return (
    <div className="budget-card">
      <div className="card-header">
        <h2>Monthly Budget </h2>
        <span className="budget-tag">
          {expenses} / {budgetedTotal} €
        </span>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <p className="daily-budget-text">
        You can spend<strong>€{dailyBudget} </strong>/day for {daysLeft} days
      </p>

      
    </div>
  );
};

export default MonthlyBudgetCard;
