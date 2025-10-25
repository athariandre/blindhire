# BlindHire - Provably Fair AI Resume Screening

A blockchain-verified, bias-free hiring platform that ensures transparent and fair resume screening using smart contracts on Sepolia testnet.

## 🎯 What is BlindHire?

BlindHire eliminates bias in hiring by:
- 🤖 **AI-Powered Screening**: Anonymous resume analysis
- 🔗 **Blockchain Verification**: All decisions recorded on-chain
- 🔒 **Cryptographic Commitments**: Tamper-proof evaluations
- 👤 **Privacy-First**: Resume data anonymized before processing
- ✅ **Transparent**: Every decision is publicly auditable

## 🏗️ Architecture

```
Frontend (React + TailwindCSS)
    ↓
Backend (FastAPI + Python)
    ↓
Smart Contracts (Solidity + Hardhat)
    ↓
Sepolia Testnet
```

## 🚀 Quick Start (5 Minutes)

### Automated Setup

**Windows:**
```cmd
setup_env.bat
```

**Mac/Linux:**
```bash
chmod +x setup_env.sh
./setup_env.sh
```

### Manual Setup

### Prerequisites
- Node.js 18+ (for frontend & contracts)
- Python 3.8+ (for backend)
- MetaMask browser extension
- Sepolia ETH ([Get from faucet](https://sepoliafaucet.com/))

### 1. Environment Configuration

Create `.env` file in project root:

```bash
# Blockchain Configuration
SEPOLIA_RPC_URL=https://rpc.sepolia.org
PRIVATE_KEY=your_wallet_private_key_here
FACTORY_CONTRACT_ADDRESS=0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d

# Optional
ETHERSCAN_API_KEY=your_etherscan_api_key
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Start backend server
python start_backend.py
```

Backend runs on `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

Frontend runs on `http://localhost:3000`

## 🔧 API Endpoints

### Apply for Job
- **POST** `/api/apply`
- Upload resume PDF and get AI screening results

### Check Status
- **GET** `/api/status?submission_id=...`
- Check application status and blockchain verification

### Claim Position
- **POST** `/api/claim`
- Claim accepted position with wallet signature

### Admin Functions
- **POST** `/api/accept` - Accept submission
- **POST** `/api/job` - Create new job
- **GET** `/api/job/{job_id}/summary` - Get job details

## 🎯 Features

- **Provably Fair**: All decisions recorded on blockchain
- **Bias-Free**: AI screening removes human bias
- **Transparent**: Every decision is auditable
- **Privacy-Preserving**: Personal data is anonymized
- **Web3 Integration**: MetaMask wallet connection

## 📜 Smart Contracts

### Deployed on Sepolia Testnet

| Contract | Address | Purpose |
|----------|---------|---------|
| JobFactory | `0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d` | Deploy job contracts |
| JobContract | Dynamic | Store evaluations per job |

**View on Etherscan:**  
https://sepolia.etherscan.io/address/0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d

### Contract Architecture

Each job gets its own contract that stores:
- ✅ Resume hashes (SHA256)
- ✅ Model hashes (AI version)
- ✅ Score hashes (evaluation results)
- ✅ Timestamps (when evaluated)
- ✅ Encrypted email hashes (optional)

### Verification

Anyone can verify their results:
```javascript
const verified = await jobContract.verifyEvaluation(
  submissionId,
  resumeHash,
  modelHash,
  scoreHash
);
// Returns: true if evaluation matches blockchain
```

## 🏗️ Tech Stack

- **Frontend**: React + Tailwind CSS + Ethers.js
- **Backend**: FastAPI + Python + Web3.py
- **Smart Contracts**: Solidity + Hardhat
- **Blockchain**: Ethereum Sepolia Testnet
- **ML Service**: Resume analysis and scoring

## 📱 Usage

### For Candidates:

1. **Connect MetaMask** → Switch to Sepolia testnet
2. **Get Job ID** → From recruiter
3. **Upload Resume** → PDF format only
4. **Submit** → AI analyzes in 2-3 seconds
5. **View Results** → Score, decision, blockchain TX
6. **Track Status** → "My Applications" page
7. **Claim Position** → Sign with MetaMask if accepted

### For Recruiters:

1. **Connect MetaMask** → Switch to Sepolia testnet
2. **Create Job** → Fill job details
3. **Get Job ID** → Copy and share with candidates
4. **Review Applications** → See all submissions
5. **Accept/Reject** → Make decisions
6. **Track Submissions** → Monitor status

## 🔒 Security & Privacy

### Privacy
- ✅ Resume anonymized before AI processing
- ✅ No PII sent to ML service
- ✅ Original PDF not stored
- ✅ Optional encrypted email

### Security
- ✅ All evaluations on blockchain (tamper-proof)
- ✅ Cryptographic commitments (SHA256 hashes)
- ✅ MetaMask signature verification
- ✅ Open-source and auditable

### Fairness
- ✅ AI decisions recorded before applicant sees results
- ✅ Cannot change evaluation after commitment
- ✅ Transparent and verifiable
- ✅ No human bias in screening
