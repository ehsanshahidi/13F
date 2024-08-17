import React, { useState, useEffect } from 'react';
import axios, { AxiosResponse } from 'axios';

interface Filing {
  fund: string;
  percentage: number;
  value: number;
}

const App: React.FC = () => {
  const [filings, setFilings] = useState<Filing[]>([]);

  useEffect(() => {
    axios.get<Filing[]>('http://localhost:5000/api/filings')
      .then((response: AxiosResponse<Filing[]>) => {
        setFilings(response.data);
      })
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>13F Filings</h1>
      <table>
        <thead>
          <tr>
            <th>Fund</th>
            <th>Percentage of Portfolio</th>
            <th>Fund Value</th>
          </tr>
        </thead>
        <tbody>
          {filings.map((filing, index) => (
            <tr key={index}>
              <td>{filing.fund}</td>
              <td>{filing.percentage}%</td>
              <td>${filing.value.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
