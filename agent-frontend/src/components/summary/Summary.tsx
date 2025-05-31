import { useEffect, useState } from 'react';
import { generateMonthlySummary } from '../../api/endpoints';

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
    handleGenerateSummary(month)
  }, [month])

  if (responseLoading) {
    return <div>Generating monthly summary...</div>;
  }
  return (
    <div style={{padding: 16}}>
      {responseLoading ? (
        <div>Generating monthly summary...</div>
      ) : (
        <div>
          <div>Month: {month}</div>
          <input onChange={(e) => setInput(e.target.value)}></input>
          <button onClick={() => setMonth(input)}>Generate summary</button>

          <div>{JSON.stringify(summary)}</div>
        </div>
      )}
    </div>
  );
};

export default Summary;
