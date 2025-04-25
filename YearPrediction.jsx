import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function YearPrediction() {
  const [year, setYear] = useState(2021);
  const [data, setData] = useState(null);

  const handleChange = e => setYear(e.target.value);

  const handlePredict = async () => {
    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ year: Number(year) })
    });
    const json = await res.json();
    // Expect json.metrics: { total, male, female, urban, rural, under18 }
    setData(json.metrics);
  };

  return (
    <>
      <div className="input-group">
        <label htmlFor="year">Enter Year: </label>
        <input
          id="year"
          type="number"
          value={year}
          min={2011}
          onChange={handleChange}
        />
        <button onClick={handlePredict}>Predict</button>
      </div>

      {data && (
        <>
          <div className="metrics">
            {['total','male','female','urban','rural','under18'].map(key => (
              <div className="metric-card" key={key}>
                <div className="metric-label">{key.charAt(0).toUpperCase() + key.slice(1)} Population</div>
                <div className="metric-value">{data[key].toLocaleString()}</div>
              </div>
            ))}
          </div>

          <div className="chart-container">
            <Line
              data={{
                labels: ['Total','Male','Female','Urban','Rural','Under 18'],
                datasets: [{
                  label: `Population Breakdown ${year}`,
                  data: ['total','male','female','urban','rural','under18'].map(k => data[k]),
                  fill: false,
                  tension: 0.1
                }]
              }}
              options={{
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
              }}
            />
          </div>
        </>
      )}
    </>
  );
}