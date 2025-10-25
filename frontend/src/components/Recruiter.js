import React, { useState, useEffect } from 'react';
import { apiService } from '../utils/api';

function Recruiter({ walletConnected, walletAddress }) {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [showCreateJob, setShowCreateJob] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    requirements: '',
    location: '',
    salary: ''
  });

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = async () => {
    try {
      setLoading(true);
      // This would be a new endpoint to get all submissions for the recruiter
      const response = await apiService.getRecruiterSubmissions();
      setSubmissions(response.data || []);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch submissions');
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptSubmission = async (submissionId) => {
    try {
      await apiService.acceptSubmission(submissionId);
      // Refresh submissions after accepting
      fetchSubmissions();
      setSelectedSubmission(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to accept submission');
    }
  };

  const handleCreateJob = async (e) => {
    e.preventDefault();
    try {
      await apiService.createJob(newJob);
      setShowCreateJob(false);
      setNewJob({
        title: '',
        description: '',
        requirements: '',
        location: '',
        salary: ''
      });
      // Refresh submissions to show new job
      fetchSubmissions();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to create job');
    }
  };

  const getScoreBadge = (score) => {
    if (score >= 80) return { color: 'bg-green-100 text-green-800', text: 'High' };
    if (score >= 60) return { color: 'bg-yellow-100 text-yellow-800', text: 'Medium' };
    return { color: 'bg-red-100 text-red-800', text: 'Low' };
  };

  const getBucketBadge = (bucket) => {
    switch (bucket?.toLowerCase()) {
      case 'high':
        return { color: 'bg-green-100 text-green-800', text: 'High' };
      case 'medium':
        return { color: 'bg-yellow-100 text-yellow-800', text: 'Medium' };
      case 'low':
        return { color: 'bg-red-100 text-red-800', text: 'Low' };
      default:
        return { color: 'bg-gray-100 text-gray-800', text: 'Unknown' };
    }
  };

  const getStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return { color: 'bg-yellow-100 text-yellow-800', text: 'Pending' };
      case 'accepted':
        return { color: 'bg-green-100 text-green-800', text: 'Accepted' };
      case 'rejected':
        return { color: 'bg-red-100 text-red-800', text: 'Rejected' };
      default:
        return { color: 'bg-gray-100 text-gray-800', text: status };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading recruiter dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Recruiter Dashboard</h1>
            <p className="mt-2 text-gray-600">Manage job applications and review candidates</p>
          </div>
          <div className="mt-4 sm:mt-0">
            <button 
              className="btn btn-primary"
              onClick={() => setShowCreateJob(true)}
            >
              <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create New Job
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Submissions Table */}
        <div className="card">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Recent Submissions</h2>
            <p className="mt-1 text-gray-600">Review and manage candidate applications</p>
          </div>
          
          {submissions.length === 0 ? (
            <div className="text-center py-12">
              <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-full">
                <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No submissions yet</h3>
              <p className="text-gray-600 mb-4">Create a job to start receiving applications.</p>
              <button 
                className="btn btn-primary"
                onClick={() => setShowCreateJob(true)}
              >
                Create Your First Job
              </button>
            </div>
          ) : (
            <div className="overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Submission ID
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Score
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Bucket
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {submissions.map((submission) => {
                      const scoreBadge = getScoreBadge(submission.score);
                      const bucketBadge = getBucketBadge(submission.bucket);
                      const statusBadge = getStatusBadge(submission.status);
                      
                      return (
                        <tr key={submission.submission_id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <code className="text-sm font-mono text-gray-900">
                              {submission.submission_id.slice(0, 8)}...
                            </code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${scoreBadge.color}`}>
                              {submission.score}/100
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${bucketBadge.color}`}>
                              {bucketBadge.text}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusBadge.color}`}>
                              {statusBadge.text}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex space-x-2">
                              <button 
                                className="text-primary-600 hover:text-primary-900"
                                onClick={() => setSelectedSubmission(submission)}
                              >
                                View Details
                              </button>
                              {submission.status === 'pending' && (
                                <button 
                                  className="text-green-600 hover:text-green-900"
                                  onClick={() => handleAcceptSubmission(submission.submission_id)}
                                >
                                  Accept
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Submission Details Modal */}
      {selectedSubmission && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedSubmission(null)}>
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full animate-slide-up" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Submission Details</h3>
              <button 
                className="text-gray-400 hover:text-gray-600 transition-colors"
                onClick={() => setSelectedSubmission(null)}
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Submission ID</label>
                    <p className="mt-1 text-sm font-mono text-gray-900">{selectedSubmission.submission_id}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Score</label>
                    <div className="mt-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreBadge(selectedSubmission.score).color}`}>
                        {selectedSubmission.score}/100
                      </span>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Bucket</label>
                    <div className="mt-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBucketBadge(selectedSubmission.bucket).color}`}>
                        {getBucketBadge(selectedSubmission.bucket).text}
                      </span>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Status</label>
                    <div className="mt-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(selectedSubmission.status).color}`}>
                        {getStatusBadge(selectedSubmission.status).text}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              {selectedSubmission.tx_hash && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <label className="text-sm font-medium text-gray-700">Transaction Hash</label>
                  <div className="mt-1">
                    <a 
                      href={`https://sepolia.etherscan.io/tx/${selectedSubmission.tx_hash}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-sm font-mono text-primary-600 hover:text-primary-700 bg-gray-100 px-3 py-1 rounded"
                    >
                      {selectedSubmission.tx_hash.slice(0, 10)}...{selectedSubmission.tx_hash.slice(-8)}
                      <svg className="ml-1 w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Create Job Modal */}
      {showCreateJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setShowCreateJob(false)}>
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full animate-slide-up" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Create New Job</h3>
              <button 
                className="text-gray-400 hover:text-gray-600 transition-colors"
                onClick={() => setShowCreateJob(false)}
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <form onSubmit={handleCreateJob} className="p-6">
              <div className="space-y-6">
                <div>
                  <label htmlFor="title" className="label">Job Title</label>
                  <input
                    type="text"
                    id="title"
                    value={newJob.title}
                    onChange={(e) => setNewJob({...newJob, title: e.target.value})}
                    className="input"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="description" className="label">Description</label>
                  <textarea
                    id="description"
                    value={newJob.description}
                    onChange={(e) => setNewJob({...newJob, description: e.target.value})}
                    rows="4"
                    className="input"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="requirements" className="label">Requirements</label>
                  <textarea
                    id="requirements"
                    value={newJob.requirements}
                    onChange={(e) => setNewJob({...newJob, requirements: e.target.value})}
                    rows="3"
                    className="input"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="location" className="label">Location</label>
                    <input
                      type="text"
                      id="location"
                      value={newJob.location}
                      onChange={(e) => setNewJob({...newJob, location: e.target.value})}
                      className="input"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="salary" className="label">Salary</label>
                    <input
                      type="text"
                      id="salary"
                      value={newJob.salary}
                      onChange={(e) => setNewJob({...newJob, salary: e.target.value})}
                      className="input"
                    />
                  </div>
                </div>
              </div>
              
              <div className="mt-8 flex space-x-3">
                <button 
                  type="button" 
                  className="btn btn-secondary flex-1"
                  onClick={() => setShowCreateJob(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary flex-1">
                  Create Job
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Recruiter;

