# BlindHire - Provably Fair AI Resume Screening

A blockchain-verified, bias-free hiring platform that ensures transparent and fair resume screening.

## 🚀 Quick Start

### Prerequisites
- Node.js (for frontend)
- Python 3.8+ (for backend)
- MetaMask browser extension

### Backend Setup
1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Start the backend server:
```bash
python start_backend.py
```
The backend will run on `http://localhost:8000`

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```
The frontend will run on `http://localhost:3000`

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

## 🏗️ Architecture

- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI + Python
- **Blockchain**: Ethereum (Sepolia testnet)
- **ML Service**: Resume analysis and scoring

## 📱 Usage

1. Connect your MetaMask wallet
2. Upload your resume (PDF only)
3. Enter job ID
4. Get AI screening results
5. View blockchain verification
6. Claim position if accepted

## 🔒 Security

- All resume data is anonymized before AI screening
- Blockchain records ensure decision integrity
- Wallet signatures verify claim authenticity
- No personal data stored permanently
