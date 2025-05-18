import React from 'react';
import './card.css';

type ChallengeCardProps = {
    challenge: string;
    targetDate: string;
};

const ChallengeCard: React.FC<ChallengeCardProps> = ({ challenge, targetDate }) => {
    return (
        <div className= "card" >
        <div className="challenge-tag" > Challenge < /div>
            < h2 className = "goal-title" > { challenge } < /h2>
                < /div>
    );
};

export default ChallengeCard;