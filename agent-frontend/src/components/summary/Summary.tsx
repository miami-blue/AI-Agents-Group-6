import { useEffect, useState } from 'react';
import { generateMonthlySummary } from '../../api/endpoints';
import './summary.css';

const Summary = () => {
  const [responseLoading, setResponseLoading] = useState(false);
  const [input, setInput] = useState<string>('');
  const [month, setMonth] = useState<string>();
  const [summary, setSummary] = useState<Record<string, any>>({});

  const handleGenerateSummary = async (monthKey: string) => {
    setResponseLoading(true);
    try {
      const response = await generateMonthlySummary(monthKey);
      setResponseLoading(false);
      setSummary(response); // Update summary with the agent's response
    } catch (error) {
      setResponseLoading(false);
      console.error('Error sending prompt:', error);
    }
  };

  useEffect(() => {
    if (!month || month.length !== 7) {
      return;
    }
    handleGenerateSummary(month);
  }, [month]);

  if (responseLoading) {
    return <div>Generating monthly summary...</div>;
  }
  return (
    <div className="summary-container">
      {responseLoading ? (
        <div>Generating monthly summary...</div>
      ) : (
        <div>
           <button className="wrap-up-button" onClick={() => {setMonth('2025-05')}}>📊 View May Wrap Up</button>
          {/* <div>Month: {month}</div>
          <input onChange={(e) => setInput(e.target.value)}></input>
          <button onClick={() => setMonth(input)}>Generate summary</button> */}

          {Object.entries(summary).length > 0 && (
            <div>
              <div>{summary.explanation}</div>
              </div>
          )}
          {/* <div>{JSON.stringify(summary)}</div> */}
        </div>
      )}
    </div>
  );
};

export default Summary;
