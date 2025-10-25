import { ethers } from 'ethers';

export class WalletService {
  constructor() {
    this.provider = null;
    this.signer = null;
    this.address = null;
  }

  async connectWallet() {
    try {
      if (!window.ethereum) {
        throw new Error('MetaMask not detected. Please install MetaMask.');
      }

      // Request account access
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
      });

      this.provider = new ethers.BrowserProvider(window.ethereum);
      this.signer = await this.provider.getSigner();
      this.address = await this.signer.getAddress();

      return {
        address: this.address,
        provider: this.provider,
        signer: this.signer
      };
    } catch (error) {
      console.error('Wallet connection failed:', error);
      throw error;
    }
  }

  async signMessage(message) {
    if (!this.signer) {
      throw new Error('Wallet not connected');
    }

    try {
      const signature = await this.signer.signMessage(message);
      return signature;
    } catch (error) {
      console.error('Message signing failed:', error);
      throw error;
    }
  }

  async getAddress() {
    if (!this.signer) {
      throw new Error('Wallet not connected');
    }
    return await this.signer.getAddress();
  }

  isConnected() {
    return !!this.signer;
  }

  async disconnect() {
    this.provider = null;
    this.signer = null;
    this.address = null;
  }
}

export const walletService = new WalletService();

