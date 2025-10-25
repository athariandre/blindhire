import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Request interceptor to add auth headers if needed
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Apply for a job
  async applyForJob({ resumePdf, jobId, walletAddress, encEmail }) {
    const formData = new FormData();
    formData.append('resume_pdf', resumePdf);
    formData.append('job_id', jobId);
    formData.append('wallet_address', walletAddress);
    if (encEmail) {
      formData.append('enc_email', encEmail);
    }

    const response = await api.post('/api/apply', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Check application status
  async getStatus(submissionId) {
    const response = await api.get('/api/status', {
      params: { submission_id: submissionId }
    });
    return response.data;
  },

  // Admin accept submission
  async acceptSubmission(submissionId) {
    const response = await api.post('/api/accept', {
      submission_id: submissionId
    });
    return response.data;
  },

  // Claim submission
  async claimSubmission(submissionId, signature) {
    const response = await api.post('/api/claim', {
      submission_id: submissionId,
      signature: signature
    });
    return response.data;
  },

  // Create job (recruiter)
  async createJob(jobData) {
    const response = await api.post('/api/job', jobData);
    return response.data;
  },

  // Get job summary
  async getJobSummary(jobId) {
    const response = await api.get(`/api/job/${jobId}/summary`);
    return response.data;
  },

  // Get recruiter submissions
  async getRecruiterSubmissions(jobId = null, walletAddress = null) {
    const params = {};
    if (jobId) params.job_id = jobId;
    if (walletAddress) params.wallet_address = walletAddress;
    
    try {
      const response = await api.get('/api/submissions', { params });
      return response.data;
    } catch (error) {
      // Fallback to mock data if endpoint fails
      console.warn('Using mock submission data');
      return {
        submissions: []
      };
    }
  },

  // Get all jobs
  async getAllJobs() {
    const response = await api.get('/api/jobs');
    return response.data;
  }
};

export default api;

