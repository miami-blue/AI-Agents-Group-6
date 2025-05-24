import React from 'react';
import './SummaryWidget.css';
import GoalProgressBar from '../dashboard/GoalProgressBar';

interface SummaryWidgetProps {
  savedAmount: number;
  completedChallenges: number;
  completedGoals: number;
  mostSpendCategory: string;
  mostSpendAmount: number;
  biggestIncreaseCategory: string;
  biggestIncreaseDelta: number;
  biggestDecreaseCategory: string;
  biggestDecreaseDelta: number;
  onClose: () => void;
}

const progress = 50; // Replace with actual progress value if available

const SummaryWidget: React.FC<SummaryWidgetProps> = ({
  savedAmount,
  completedChallenges,
  completedGoals,
  mostSpendCategory,
  mostSpendAmount,
  biggestIncreaseCategory,
  biggestIncreaseDelta,
  biggestDecreaseCategory,
  biggestDecreaseDelta,
  onClose,
}) => {
  return (
    <div className="summary-widget-overlay">
      <div className="summary-widget">
        <button className="close-button" onClick={onClose}>
          &times;
        </button>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem',
            padding: '2rem',
          }}
        >
          <h1
            style={{
              margin: '0px',
              fontSize: '3rem',
            }}
          >
            🚀
          </h1>
          <h2
            style={{
              margin: '0',
            }}
          >
            Last April you’ve done amazing
          </h2>
          <p>keep going and enjoy your wrapped</p>
        </div>
        <div className="tile">
          <div className="summary-item">
            <span className="summary-value">€{savedAmount}</span>
            <span className="summary-label">Saved</span>
          </div>
          <div className="summary-item">
            <span className="summary-value2">{completedChallenges}</span>
            <span className="summary-label">Challenge Completed</span>
          </div>
        </div>
        <div className="summary-item">
          <div className="goal-overview">
            <h1 className="goal-image">🍕</h1>
            <div className="goal-details">
              <h3>Pizza oven</h3>
              <GoalProgressBar progress={progress} />
            </div>
          </div>
          <div className="goal">
            <span className="summary-label">Goals Reached:</span>
            <span className="summary-value2">{completedGoals}</span>
          </div>
        </div>
        <div className="summary-item">
          <div className="category">
            <span className="summary-label">Most Spend On:</span>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <span className="summary-value2">€{mostSpendAmount}</span>
              <p>{mostSpendCategory}</p>
            </div>
          </div>
        </div>
        <div className="summary-item">
          <div className="category">
            <span className="summary-label">Biggest Increase:</span>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <span className="summary-value3">+{biggestIncreaseDelta}€</span>
              <p>{biggestIncreaseCategory}</p>
            </div>
          </div>
        </div>
        <div className="summary-item">
          <div className="category">
            <span className="summary-label">Biggest Decrease:</span>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <span className="summary-value">
                -{Math.abs(biggestDecreaseDelta)}€
              </span>
              <p>{biggestDecreaseCategory}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryWidget;
