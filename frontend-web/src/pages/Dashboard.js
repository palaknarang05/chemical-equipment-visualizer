import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend, PointElement, LineElement } from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { authAPI, datasetAPI, statisticsAPI } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend, PointElement, LineElement);

function Dashboard({ setIsAuthenticated }) {
  const [user, setUser] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const navigate = useNavigate();

  useEffect(() => {
    loadUserData();
    loadDatasets();
    loadStatistics();
  }, []);

  const loadUserData = () => {
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    setUser(userData);
  };

  const loadDatasets = async () => {
    try {
      const response = await datasetAPI.list();
      setDatasets(response.data);
    } catch (error) {
      console.error('Error loading datasets:', error);
    }
  };

  const loadStatistics = async () => {
    try {
      const response = await statisticsAPI.get();
      setStatistics(response.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setIsAuthenticated(false);
      navigate('/login');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploadLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await datasetAPI.upload(formData);
      setMessage({ type: 'success', text: 'File uploaded successfully!' });
      await loadDatasets();
      await loadStatistics();
      e.target.value = '';
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Error uploading file. Please try again.'
      });
    } finally {
      setUploadLoading(false);
    }
  };

  const handleViewDataset = async (datasetId) => {
    setLoading(true);
    try {
      const response = await datasetAPI.get(datasetId);
      setSelectedDataset(response.data);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error loading dataset details.' });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteDataset = async (datasetId) => {
    if (!window.confirm('Are you sure you want to delete this dataset?')) return;

    try {
      await datasetAPI.delete(datasetId);
      setMessage({ type: 'success', text: 'Dataset deleted successfully!' });
      await loadDatasets();
      await loadStatistics();
      if (selectedDataset?.dataset?.id === datasetId) {
        setSelectedDataset(null);
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error deleting dataset.' });
    }
  };

  const handleGenerateReport = async (datasetId) => {
    try {
      const response = await datasetAPI.generateReport(datasetId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMessage({ type: 'success', text: 'Report generated successfully!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Error generating report.' });
    }
  };

  const getTypeDistributionChart = () => {
    if (!selectedDataset?.type_distribution) return null;

    const labels = Object.keys(selectedDataset.type_distribution);
    const data = Object.values(selectedDataset.type_distribution);
    const colors = [
      '#667eea', '#764ba2', '#f093fb', '#4facfe',
      '#43e97b', '#fa709a', '#feca57', '#ff6348'
    ];

    return {
      labels,
      datasets: [{
        data,
        backgroundColor: colors.slice(0, labels.length),
        borderColor: 'white',
        borderWidth: 2,
      }],
    };
  };

  const getParameterComparisonChart = () => {
    if (!selectedDataset?.dataset?.equipment) return null;

    const equipment = selectedDataset.dataset.equipment.slice(0, 10);
    const labels = equipment.map(e => e.equipment_name.substring(0, 15));

    return {
      labels,
      datasets: [
        {
          label: 'Flowrate',
          data: equipment.map(e => e.flowrate),
          backgroundColor: '#667eea',
        },
        {
          label: 'Pressure',
          data: equipment.map(e => e.pressure),
          backgroundColor: '#764ba2',
        },
        {
          label: 'Temperature',
          data: equipment.map(e => e.temperature),
          backgroundColor: '#f093fb',
        },
      ],
    };
  };

  const getAveragesChart = () => {
    if (!selectedDataset?.dataset) return null;

    const data = selectedDataset.dataset;
    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [{
        label: 'Average Values',
        data: [data.avg_flowrate, data.avg_pressure, data.avg_temperature],
        backgroundColor: ['#667eea', '#764ba2', '#f093fb'],
        borderColor: ['#5568d3', '#6a3f8f', '#e082ea'],
        borderWidth: 2,
      }],
    };
  };

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="navbar-brand">Chemical Equipment Visualizer</div>
        <div className="navbar-user">
          <span className="user-info">Welcome, {user?.username || 'User'}!</span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </nav>

      <div className="dashboard-content">
        {message.text && (
          <div className={message.type === 'error' ? 'error-message' : 'success-message'}>
            {message.text}
          </div>
        )}

        {statistics && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Datasets</h3>
              <div className="stat-value">{statistics.total_datasets}</div>
            </div>
            <div className="stat-card">
              <h3>Total Equipment</h3>
              <div className="stat-value">{statistics.total_equipment}</div>
            </div>
          </div>
        )}

        <div className="upload-section">
          <h2>Upload New Dataset</h2>
          <div className="file-upload-area">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="file-input"
              id="file-upload"
              disabled={uploadLoading}
            />
            <label htmlFor="file-upload" className="btn-upload">
              {uploadLoading ? 'Uploading...' : 'Choose CSV File'}
            </label>
            <p style={{ marginTop: '15px', color: '#718096', fontSize: '14px' }}>
              Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
            </p>
          </div>
        </div>

        <div className="datasets-section">
          <h2>Your Datasets (Last 5)</h2>

          {datasets.length === 0 ? (
            <div className="no-data">No datasets uploaded yet. Upload your first dataset above!</div>
          ) : (
            datasets.map((dataset) => (
              <div key={dataset.id} className="dataset-card">
                <div className="dataset-header">
                  <div className="dataset-title">{dataset.filename}</div>
                  <div className="dataset-actions">
                    <button
                      onClick={() => handleViewDataset(dataset.id)}
                      className="btn-view"
                    >
                      View Details
                    </button>
                    <button
                      onClick={() => handleGenerateReport(dataset.id)}
                      className="btn-report"
                    >
                      Generate PDF
                    </button>
                    <button
                      onClick={() => handleDeleteDataset(dataset.id)}
                      className="btn-delete"
                    >
                      Delete
                    </button>
                  </div>
                </div>

                <div style={{ fontSize: '13px', color: '#718096', marginBottom: '12px' }}>
                  Uploaded: {new Date(dataset.upload_date).toLocaleString()}
                </div>

                <div className="dataset-stats">
                  <div className="stat-item">
                    <div className="stat-label">Equipment</div>
                    <div className="stat-number">{dataset.total_equipment}</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-label">Avg Flowrate</div>
                    <div className="stat-number">{dataset.avg_flowrate.toFixed(1)}</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-label">Avg Pressure</div>
                    <div className="stat-number">{dataset.avg_pressure.toFixed(1)}</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-label">Avg Temp</div>
                    <div className="stat-number">{dataset.avg_temperature.toFixed(1)}</div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {selectedDataset && (
          <div className="datasets-section" style={{ marginTop: '30px' }}>
            <h2>Dataset Details: {selectedDataset.dataset.filename}</h2>

            <div className="charts-grid">
              {getTypeDistributionChart() && (
                <div className="chart-container">
                  <div className="chart-title">Equipment Type Distribution</div>
                  <Pie data={getTypeDistributionChart()} options={{ maintainAspectRatio: true }} />
                </div>
              )}

              {getAveragesChart() && (
                <div className="chart-container">
                  <div className="chart-title">Average Parameters</div>
                  <Bar data={getAveragesChart()} options={{ maintainAspectRatio: true }} />
                </div>
              )}
            </div>

            {getParameterComparisonChart() && (
              <div className="chart-container" style={{ marginTop: '20px' }}>
                <div className="chart-title">Parameter Comparison (First 10 Equipment)</div>
                <Bar
                  data={getParameterComparisonChart()}
                  options={{
                    maintainAspectRatio: true,
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }}
                />
              </div>
            )}

            <div style={{ marginTop: '30px' }}>
              <h3 style={{ marginBottom: '15px', color: '#2d3748' }}>Equipment List</h3>
              <div style={{ overflowX: 'auto' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Equipment Name</th>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedDataset.dataset.equipment.map((eq, index) => (
                      <tr key={index}>
                        <td>{eq.equipment_name}</td>
                        <td>{eq.equipment_type}</td>
                        <td>{eq.flowrate.toFixed(1)}</td>
                        <td>{eq.pressure.toFixed(1)}</td>
                        <td>{eq.temperature.toFixed(1)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;