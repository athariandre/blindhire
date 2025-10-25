import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import './JobApplication.css';

function JobApplication() {
  const [searchParams] = useSearchParams();
  const jobId = searchParams.get('jobId');
  
  const [job, setJob] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    coverLetter: ''
  });
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (jobId) {
      fetchJobDetails();
    }
  }, [jobId]);

  const fetchJobDetails = async () => {
    try {
      const response = await axios.get(`/api/jobs/${jobId}`);
      setJob(response.data);
    } catch (err) {
      setError('Failed to fetch job details');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResume(file);
      setError(null);
    } else {
      setError('Please upload a PDF file');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('phone', formData.phone);
      formDataToSend.append('coverLetter', formData.coverLetter);
      formDataToSend.append('resume', resume);
      formDataToSend.append('jobId', jobId);

      const response = await axios.post('/api/apply', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(true);
      console.log('Application submitted:', response.data);
    } catch (err) {
      setError('Failed to submit application');
      console.error('Error submitting application:', err);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="job-application">
        <div className="success-message">
          <h2>✅ Application Submitted Successfully!</h2>
          <p>Your application has been submitted for AI screening.</p>
          <p>You will receive an email with your application ID and can track your status.</p>
          <button 
            className="btn btn-primary"
            onClick={() => window.location.href = '/status'}
          >
            Track Application Status
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="job-application">
      <div className="header">
        <h1>Job Application</h1>
        {job && (
          <div className="job-info">
            <h2>{job.title} at {job.company}</h2>
            <p>{job.location} • {job.type}</p>
          </div>
        )}
      </div>

      <div className="application-form">
        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <h3>Personal Information</h3>
            <div className="form-group">
              <label htmlFor="name">Full Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Resume Upload</h3>
            <div className="form-group">
              <label htmlFor="resume">Resume (PDF only) *</label>
              <input
                type="file"
                id="resume"
                accept=".pdf"
                onChange={handleFileChange}
                required
              />
              {resume && (
                <div className="file-info">
                  <span>✅ {resume.name}</span>
                </div>
              )}
            </div>
          </div>

          <div className="form-section">
            <h3>Cover Letter</h3>
            <div className="form-group">
              <label htmlFor="coverLetter">Cover Letter</label>
              <textarea
                id="coverLetter"
                name="coverLetter"
                value={formData.coverLetter}
                onChange={handleInputChange}
                rows="6"
                placeholder="Tell us why you're interested in this position..."
              />
            </div>
          </div>

          <div className="form-section">
            <h3>AI Screening Notice</h3>
            <div className="notice-box">
              <p>
                <strong>🔍 AI Screening Process:</strong> Your resume will be analyzed by our 
                provably fair AI system. The screening process is:
              </p>
              <ul>
                <li>✅ Completely automated and bias-free</li>
                <li>✅ Recorded on the blockchain for transparency</li>
                <li>✅ Mathematically provable for fairness</li>
                <li>✅ Results are auditable and verifiable</li>
              </ul>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !resume}
            >
              {loading ? 'Submitting...' : 'Submit Application'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default JobApplication;

