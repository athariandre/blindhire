import React, { useState, useRef } from 'react';
import { apiService } from '../utils/api';
import { walletService } from '../utils/wallet';

function Home({ walletConnected, walletAddress }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobId, setJobId] = useState('');
  const [encEmail, setEncEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a PDF file');
      setSelectedFile(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!walletConnected) {
      setError('Please connect your wallet first');
      return;
    }

    if (!selectedFile) {
      setError('Please select a PDF file');
      return;
    }

    if (!jobId.trim()) {
      setError('Please enter a job ID');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiService.applyForJob({
        resumePdf: selectedFile,
        jobId: jobId.trim(),
        walletAddress: walletAddress,
        encEmail: encEmail.trim() || undefined
      });

      setResult(response);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to submit application');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setJobId('');
    setEncEmail('');
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl">
              Provably Fair Hiring
            </h1>
            <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
              Upload your resume for anonymous, bias-free AI screening. 
              Every decision is recorded on the blockchain for complete transparency.
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Upload Form */}
            <div className="card">
              <div className="mb-6">
                <h2 className="text-2xl font-semibold text-gray-900">Submit Your Resume</h2>
                <p className="mt-2 text-gray-600">Get screened fairly and transparently</p>
              </div>
              
              {!walletConnected && (
                <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-yellow-800">
                        Please connect your wallet to continue
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="jobId" className="label">Job ID</label>
                  <input
                    type="text"
                    id="jobId"
                    value={jobId}
                    onChange={(e) => setJobId(e.target.value)}
                    placeholder="Enter job ID"
                    className="input"
                    required
                    disabled={!walletConnected}
                  />
                </div>

                <div>
                  <label htmlFor="resume" className="label">Resume (PDF only)</label>
                  <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-gray-400 transition-colors">
                    <div className="space-y-1 text-center">
                      <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <div className="flex text-sm text-gray-600">
                        <label htmlFor="resume" className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                          <span>Upload a file</span>
                          <input
                            ref={fileInputRef}
                            type="file"
                            id="resume"
                            accept=".pdf"
                            onChange={handleFileSelect}
                            className="sr-only"
                            required
                            disabled={!walletConnected}
                          />
                        </label>
                        <p className="pl-1">or drag and drop</p>
                      </div>
                      <p className="text-xs text-gray-500">PDF up to 10MB</p>
                    </div>
                  </div>
                  {selectedFile && (
                    <div className="mt-2 flex items-center text-sm text-green-600">
                      <svg className="flex-shrink-0 mr-1.5 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      {selectedFile.name}
                    </div>
                  )}
                </div>

                <div>
                  <label htmlFor="encEmail" className="label">Email</label>
                  <input
                    type="text"
                    id="encEmail"
                    value={encEmail}
                    onChange={(e) => setEncEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="input"
                    disabled={!walletConnected}
                  />
                </div>

                {error && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
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

                {result && (
                  <div className="p-6 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center mb-4">
                      <div className="flex-shrink-0">
                        <svg className="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-lg font-medium text-green-800">Application Submitted Successfully!</h3>
                      </div>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="font-medium text-gray-700">Submission ID:</span>
                        <span className="font-mono text-gray-900">{result.submission_id}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="font-medium text-gray-700">Score:</span>
                        <span className="font-semibold text-gray-900">{(result.score * 100).toFixed(1)}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="font-medium text-gray-700">Decision:</span>
                        <span className={`font-semibold ${
                          result.decision === 'auto_pass' ? 'text-green-600' : 
                          result.decision === 'auto_reject' ? 'text-red-600' : 
                          'text-yellow-600'
                        }`}>
                          {result.decision === 'auto_pass' ? 'Passed' : 
                           result.decision === 'auto_reject' ? 'Rejected' : 
                           'Pending'}
                        </span>
                      </div>
                      {result.tx_hash && (
                        <div className="flex justify-between">
                          <span className="font-medium text-gray-700">Transaction:</span>
                          <a 
                            href={`https://sepolia.etherscan.io/tx/${result.tx_hash.startsWith('0x') ? result.tx_hash : '0x' + result.tx_hash}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-mono text-primary-600 hover:text-primary-700 text-xs"
                          >
                            {result.tx_hash.slice(0, 10)}...{result.tx_hash.slice(-8)}
                          </a>
                        </div>
                      )}
                    </div>
                    
                    <div className="mt-6 flex space-x-3">
                      <button 
                        type="button" 
                        className="btn btn-secondary"
                        onClick={() => window.location.href = `/status?submission_id=${result.submission_id}`}
                      >
                        Check Status
                      </button>
                      <button 
                        type="button" 
                        className="btn btn-primary"
                        onClick={resetForm}
                      >
                        Submit Another
                      </button>
                    </div>
                  </div>
                )}

                <div className="pt-4">
                  <button 
                    type="submit" 
                    className="btn btn-primary w-full"
                    disabled={loading || !walletConnected || !selectedFile}
                  >
                    {loading ? (
                      <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Submitting...
                      </div>
                    ) : (
                      'Submit Resume'
                    )}
                  </button>
                </div>
              </form>
            </div>

            {/* Info Section */}
            <div className="space-y-8">
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">What We Remove</h3>
                <div className="space-y-3">
                  {[
                    { icon: '👤', text: 'Name and personal identifiers' },
                    { icon: '📧', text: 'Email addresses and contact info' },
                    { icon: '📞', text: 'Phone numbers' },
                    { icon: '🏠', text: 'Addresses and location data' },
                    { icon: '📅', text: 'Birth dates and age indicators' },
                    { icon: '🖼️', text: 'Photos and profile pictures' }
                  ].map((item, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <span className="text-lg">{item.icon}</span>
                      <span className="text-sm text-gray-700">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card bg-blue-50 border-blue-200">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-semibold text-blue-900">Privacy & Fairness</h3>
                    <div className="mt-2 text-sm text-blue-800">
                      <ul className="space-y-1">
                        <li>• Your resume is anonymized before AI screening</li>
                        <li>• All decisions are recorded on the blockchain</li>
                        <li>• You can verify the fairness of your screening</li>
                        <li>• No human bias in the initial screening process</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
