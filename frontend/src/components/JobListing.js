import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './JobListing.css';

function JobListing() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      // This would connect to your backend API
      const response = await axios.get('/api/jobs');
      setJobs(response.data);
    } catch (err) {
      setError('Failed to fetch jobs');
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="job-listing">
        <div className="loading">Loading available jobs...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="job-listing">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="job-listing">
      <div className="header">
        <h1>Available Jobs</h1>
        <p>Browse and apply to positions with provably fair AI screening</p>
      </div>

      <div className="jobs-grid">
        {jobs.length === 0 ? (
          <div className="no-jobs">
            <p>No jobs available at the moment.</p>
          </div>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="job-card">
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className="job-company">{job.company}</span>
              </div>
              <div className="job-details">
                <p className="job-location">📍 {job.location}</p>
                <p className="job-type">💼 {job.type}</p>
                <p className="job-salary">💰 {job.salary}</p>
              </div>
              <div className="job-description">
                <p>{job.description}</p>
              </div>
              <div className="job-requirements">
                <h4>Requirements:</h4>
                <ul>
                  {job.requirements.map((req, index) => (
                    <li key={index}>{req}</li>
                  ))}
                </ul>
              </div>
              <div className="job-actions">
                <button 
                  className="btn btn-primary"
                  onClick={() => window.location.href = `/apply?jobId=${job.id}`}
                >
                  Apply Now
                </button>
                <div className="fairness-badge">
                  <span>✅ Provably Fair Screening</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default JobListing;

