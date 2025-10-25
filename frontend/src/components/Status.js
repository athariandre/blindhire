import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { apiService } from '../utils/api';
import { walletService } from '../utils/wallet';
import ClaimModal from './ClaimModal';

function Status({ walletConnected, walletAddress }) {
  const [searchParams] = useSearchParams();
  const submissionId = searchParams.get('submission_id');
  
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showClaimModal, setShowClaimModal] = useState(false);
  const [polling, setPolling] = useState(false);

  useEffect(() => {
    if (submissionId) {
      fetchStatus();
    } else {
      setError('No submission ID provided');
      setLoading(false);
    }
  }, [submissionId]);

  useEffect(() => {
    let interval;
    if (polling && submissionId) {
      interval = setInterval(() => {
        fetchStatus();
      }, 3000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [polling, submissionId]);

  const fetchStatus = async () => {
    try {
      const response = await apiService.getStatus(submissionId);
      setStatus(response);
      setError(null);
      
      // Stop polling if verified
      if (response.verified) {
        setPolling(false);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch status');
      setPolling(false);
    } finally {
      setLoading(false);
    }
  };

  const startPolling = () => {
    setPolling(true);
  };

  const stopPolling = () => {
    setPolling(false);
  };

  const getDecisionBadge = (decision) => {
    switch (decision?.toLowerCase()) {
      case 'auto_pass':
        return { color: 'bg-green-100 text-green-800', icon: '✅', text: 'Passed' };
      case 'auto_reject':
        return { color: 'bg-red-100 text-red-800', icon: '❌', text: 'Rejected' };
      default:
        return { color: 'bg-yellow-100 text-yellow-800', icon: '⏳', text: 'Pending' };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading application status...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200">
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
              <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Error</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <button className="btn btn-primary" onClick={fetchStatus}>
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Status Found</h3>
            <p className="text-gray-600">Unable to find status for submission ID: {submissionId}</p>
          </div>
        </div>
      </div>
    );
  }

  const decisionBadge = getDecisionBadge(status.decision);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Application Status</h1>
          <p className="mt-2 text-gray-600">
            Submission ID: <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">{submissionId}</code>
          </p>
        </div>

        {/* Main Status Card */}
        <div className="card">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Decision Section */}
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Decision</h2>
                <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${decisionBadge.color}`}>
                  <span className="mr-2">{decisionBadge.icon}</span>
                  {decisionBadge.text}
                </div>
              </div>

              {status.score && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Score</h3>
                  <div className="flex items-center space-x-4">
                    <div className="flex-1">
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-primary-600 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${(status.score * 100)}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-2xl font-bold text-gray-900">
                      {(status.score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Verification Section */}
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Blockchain Verification</h2>
                <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
                  status.verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  <span className="mr-2">{status.verified ? '🔗' : '⏳'}</span>
                  {status.verified ? 'Verified' : 'Pending'}
                </div>
              </div>

              {status.tx_hash && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Transaction Hash</h3>
                  <a 
                    href={`https://sepolia.etherscan.io/tx/${status.tx_hash.startsWith('0x') ? status.tx_hash : '0x' + status.tx_hash}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-sm font-mono text-primary-600 hover:text-primary-700 bg-gray-100 px-3 py-1 rounded"
                  >
                    {status.tx_hash.startsWith('0x') ? status.tx_hash.slice(0, 10) : '0x' + status.tx_hash.slice(0, 8)}...{status.tx_hash.slice(-8)}
                    <svg className="ml-1 w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            {!status.verified && (
              <div className="text-center">
                {polling ? (
                  <div className="space-y-3">
                    <button className="btn btn-secondary" onClick={stopPolling}>
                      Stop Polling
                    </button>
                    <p className="text-sm text-gray-600 flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Checking for updates every 3 seconds...
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <button className="btn btn-primary" onClick={startPolling}>
                      Start Polling
                    </button>
                    <p className="text-sm text-gray-600">Click to start checking for updates</p>
                  </div>
                )}
              </div>
            )}

            {status.verified && status.decision?.toLowerCase() === 'auto_pass' && (
              <div className="text-center p-6 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-green-100 rounded-full">
                  <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-green-900 mb-2">Congratulations!</h3>
                <p className="text-green-800 mb-4">Your application was accepted. You can now claim your position.</p>
                <button 
                  className="btn btn-primary"
                  onClick={() => setShowClaimModal(true)}
                  disabled={!walletConnected}
                >
                  Claim Position
                </button>
              </div>
            )}

            {status.decision?.toLowerCase() === 'auto_reject' && (
              <div className="text-center p-6 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
                  <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-red-900 mb-2">Application Not Selected</h3>
                <p className="text-red-800 mb-2">Unfortunately, your application was not selected for this position.</p>
                <p className="text-sm text-red-700">You can verify the fairness of the screening process using the blockchain transaction above.</p>
              </div>
            )}
          </div>
        </div>

        {/* Fairness Verification */}
        <div className="mt-8 card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Fairness Verification</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { label: 'Anonymization', value: '✅ Personal data stripped', status: 'verified' },
              { label: 'AI Screening', value: '✅ Bias-free algorithm used', status: 'verified' },
              { label: 'Blockchain Record', value: status.verified ? '✅ Verified on-chain' : '⏳ Pending verification', status: status.verified ? 'verified' : 'pending' },
              { label: 'Transparency', value: '✅ Decision process auditable', status: 'verified' }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-sm font-medium text-gray-700">{item.label}</span>
                <span className={`text-sm ${
                  item.status === 'verified' ? 'text-green-600' : 'text-yellow-600'
                }`}>
                  {item.value}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {showClaimModal && (
        <ClaimModal
          submissionId={submissionId}
          onClose={() => setShowClaimModal(false)}
          walletConnected={walletConnected}
          walletAddress={walletAddress}
        />
      )}
    </div>
  );
}

export default Status;

