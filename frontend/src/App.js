import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './components/Home';
import Status from './components/Status';
import Recruiter from './components/Recruiter';
import MyApplications from './components/MyApplications';
import { walletService } from './utils/wallet';

function App() {
  const [walletConnected, setWalletConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkWalletConnection();
  }, []);

  const checkWalletConnection = async () => {
    try {
      if (window.ethereum) {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        if (accounts.length > 0) {
          setWalletConnected(true);
          setWalletAddress(accounts[0]);
        }
      }
    } catch (error) {
      console.error('Error checking wallet connection:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectWallet = async () => {
    try {
      const { address } = await walletService.connectWallet();
      setWalletConnected(true);
      setWalletAddress(address);
    } catch (error) {
      console.error('Failed to connect wallet:', error);
      alert('Failed to connect wallet: ' + error.message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar 
          walletConnected={walletConnected} 
          walletAddress={walletAddress} 
          onConnectWallet={connectWallet}
        />
        <main className="pb-12">
          <Routes>
            <Route path="/" element={<Home walletConnected={walletConnected} walletAddress={walletAddress} />} />
            <Route path="/my-applications" element={<MyApplications walletConnected={walletConnected} walletAddress={walletAddress} />} />
            <Route path="/status" element={<Status walletConnected={walletConnected} walletAddress={walletAddress} />} />
            <Route path="/recruiter" element={<Recruiter walletConnected={walletConnected} walletAddress={walletAddress} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function Navbar({ walletConnected, walletAddress, onConnectWallet }) {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">B</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">BlindHire</span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-8">
            <div className="hidden md:flex space-x-6">
              <Link 
                to="/" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/') ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Home
              </Link>
              <Link 
                to="/my-applications" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/my-applications') ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                My Applications
              </Link>
              <Link 
                to="/status" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/status') ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Status
              </Link>
              <Link 
                to="/recruiter" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/recruiter') ? 'text-primary-600' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Recruiter
              </Link>
            </div>
            
            {walletConnected ? (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm font-medium text-gray-700 font-mono">
                  {walletAddress?.slice(0, 6)}...{walletAddress?.slice(-4)}
                </span>
              </div>
            ) : (
              <button 
                className="btn btn-primary text-sm"
                onClick={onConnectWallet}
              >
                Connect Wallet
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default App;
