import React, { useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { useDataContext } from '../../api/DataContext';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const BudgetPie: React.FC = () => {
  const [selectedMonth, setSelectedMonth] = useState('06')

  const {budgetsResponse} = useDataContext()
  
  const budget = budgetsResponse.data.filter(item => !!item.Month && item.Month === `2025-${selectedMonth}`)
  
  const chartData = budget.map(item => ({name: item.Category, value: item.Amount})).filter(item => item.name !== 'Income')
  
  return (
    <div>

   
    <div style={{ width: '100%', height: '300px' }}>
     
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            fill="#8884d8"
            paddingAngle={5}
          >
            {chartData.map((_entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>

      </ResponsiveContainer>
    </div>

    <div style={{display: 'flex', justifyContent: 'center', width: '100%'}}>
        <table>
          <tbody>
            {/* <tr>
              <td><b>Income</b></td>
              <td><b>{budget.find(item => item.Category === 'Income')?.Amount}</b></td>
            </tr> */}
          {chartData.map((entry, index) => (
             <tr key={index}>
              <td>{entry.name}</td>
              <td>{entry.value}</td>
             </tr>
            ))}
          </tbody>
        </table>
        </div>
    </div>
  );
};

export default BudgetPie;
