import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ApplicationStatus.css';

function ApplicationStatus() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      // This would connect to your backend API
      const response = await axios.get('/api/applications');
      setApplications(response.data);
    } catch (err) {
      setError('Failed to fetch applications');
      console.error('Error fetching applications:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'submitted': return 'status-submitted';
      case 'screening': return 'status-screening';
      case 'approved': return 'status-approved';
      case 'rejected': return 'status-rejected';
      default: return 'status-pending';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'submitted': return '📝';
      case 'screening': return '🤖';
      case 'approved': return '✅';
      case 'rejected': return '❌';
      default: return '⏳';
    }
  };

  if (loading) {
    return (
      <div className="application-status">
        <div className="loading">Loading your applications...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="application-status">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="application-status">
      <div className="header">
        <h1>My Applications</h1>
        <p>Track your applications and view AI screening results</p>
      </div>

      {applications.length === 0 ? (
        <div className="no-applications">
          <p>You haven't submitted any applications yet.</p>
          <a href="/jobs" className="btn btn-primary">Browse Jobs</a>
        </div>
      ) : (
        <div className="applications-list">
          {applications.map((app) => (
            <div key={app.id} className="application-card">
              <div className="application-header">
                <div className="job-info">
                  <h3>{app.jobTitle}</h3>
                  <p className="company">{app.company}</p>
                  <p className="applied-date">Applied: {new Date(app.appliedDate).toLocaleDateString()}</p>
                </div>
                <div className={`status-badge ${getStatusColor(app.status)}`}>
                  <span className="status-icon">{getStatusIcon(app.status)}</span>
                  <span className="status-text">{app.status}</span>
                </div>
              </div>

              <div className="application-details">
                <div className="screening-results">
                  <h4>AI Screening Results</h4>
                  {app.screeningResults ? (
                    <div className="results-grid">
                      <div className="result-item">
                        <span className="result-label">Overall Score:</span>
                        <span className="result-value">{app.screeningResults.overallScore}/100</span>
                      </div>
                      <div className="result-item">
                        <span className="result-label">Skills Match:</span>
                        <span className="result-value">{app.screeningResults.skillsMatch}%</span>
                      </div>
                      <div className="result-item">
                        <span className="result-label">Experience Match:</span>
                        <span className="result-value">{app.screeningResults.experienceMatch}%</span>
                      </div>
                      <div className="result-item">
                        <span className="result-label">Education Match:</span>
                        <span className="result-value">{app.screeningResults.educationMatch}%</span>
                      </div>
                    </div>
                  ) : (
                    <p className="pending-results">Screening in progress...</p>
                  )}
                </div>

                <div className="blockchain-info">
                  <h4>Blockchain Verification</h4>
                  <div className="verification-details">
                    <p><strong>Transaction Hash:</strong> {app.blockchainHash || 'Pending...'}</p>
                    <p><strong>Fairness Score:</strong> {app.fairnessScore || 'Calculating...'}</p>
                    <p><strong>Bias Detection:</strong> {app.biasDetected ? '⚠️ Potential bias detected' : '✅ No bias detected'}</p>
                  </div>
                </div>

                <div className="detailed-results">
                  <button 
                    className="btn btn-secondary"
                    onClick={() => setSelectedApp(selectedApp === app.id ? null : app.id)}
                  >
                    {selectedApp === app.id ? 'Hide Details' : 'View Detailed Results'}
                  </button>
                  
                  {selectedApp === app.id && (
                    <div className="detailed-breakdown">
                      <h5>Detailed AI Analysis</h5>
                      <div className="breakdown-section">
                        <h6>Skills Analysis</h6>
                        <ul>
                          {app.screeningResults?.skillsBreakdown?.map((skill, index) => (
                            <li key={index}>
                              <span className="skill-name">{skill.name}</span>
                              <span className="skill-score">{skill.score}/10</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div className="breakdown-section">
                        <h6>Experience Analysis</h6>
                        <p>Years of relevant experience: {app.screeningResults?.experienceYears}</p>
                        <p>Industry relevance: {app.screeningResults?.industryRelevance}%</p>
                      </div>
                      <div className="breakdown-section">
                        <h6>Fairness Metrics</h6>
                        <p>Gender bias score: {app.screeningResults?.genderBiasScore || 'N/A'}</p>
                        <p>Racial bias score: {app.screeningResults?.racialBiasScore || 'N/A'}</p>
                        <p>Age bias score: {app.screeningResults?.ageBiasScore || 'N/A'}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ApplicationStatus;

