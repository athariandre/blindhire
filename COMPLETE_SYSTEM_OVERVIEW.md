# BlindHire - Complete System Overview

## 🎯 System Purpose
BlindHire is a blockchain-verified, bias-free hiring platform that ensures transparent and fair resume screening using AI and smart contracts.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Home   │  │ My Apps      │  │  Recruiter         │   │
│  │ (Apply)  │  │ (Candidate)  │  │  Dashboard         │   │
│  └──────────┘  └──────────────┘  └────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ API Calls (Axios)
┌────────────────────▼────────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  /apply  │  │ /status  │  │  /claim  │  │  /jobs   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐                               │
│  │ /accept  │  │/submissions│                             │
│  └──────────┘  └──────────┘                               │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌─▼──────────┐
│ ML Service   │ │ Blockchain│ │  Database  │
│ (AI Scoring) │ │ (Sepolia) │ │ (In-Memory)│
└──────────────┘ └───────────┘ └────────────┘
```

## 👥 User Roles & Workflows

### 1. Candidate (Job Applicant)

**Workflow:**
```
Connect Wallet → Get Job ID → Upload Resume → AI Screening → View Results → Track Status → Claim Position
```

**Pages:**
- **Home** - Apply to jobs
- **My Applications** - Track all your applications
- **Status** - Detailed application status

**Key Features:**
- Connect MetaMask wallet
- Upload PDF resume
- Get AI screening score (0-100%)
- See decision (Passed/Rejected/Pending)
- View blockchain verification
- Track application status
- Claim accepted positions

### 2. Recruiter (Employer)

**Workflow:**
```
Connect Wallet → Create Job → Get Job ID → Share with Candidates → Review Applications → Accept/Reject
```

**Pages:**
- **Recruiter Dashboard**
  - **My Jobs Tab** - View all created jobs
  - **Applications Tab** - Review all submissions

**Key Features:**
- Create job postings
- Get unique job IDs
- View all applications
- See AI scores and decisions
- Accept/reject candidates
- Track application status

## 🔄 Complete Application Flow

### Step 1: Job Creation (Recruiter)
```
Recruiter → Create Job Form → Submit
    ↓
Backend generates Job ID (e.g., "JOB-abc123")
    ↓
Job stored in database
    ↓
Recruiter copies Job ID
    ↓
Shares Job ID with candidates
```

### Step 2: Application (Candidate)
```
Candidate → Enter Job ID → Upload PDF → Submit
    ↓
Backend extracts resume text
    ↓
ML Service analyzes resume against job requirements
    ↓
Generates AI score (0.0 - 1.0)
    ↓
Determines decision:
  - Score ≥ 0.8: auto_pass
  - Score ≥ 0.5: pending (needs review)
  - Score < 0.5: auto_reject
    ↓
Records decision on blockchain
    ↓
Returns submission_id, score, decision, tx_hash
    ↓
Stores in database with job_id and wallet_address
```

### Step 3: Status Tracking
```
Candidate → My Applications → See all applications
    ↓
For each application:
  - Job ID
  - AI Score (%)
  - Decision (Passed/Rejected/Pending)
  - Status (Pending/Accepted/Claimed)
    ↓
Click "View Details" → Full status page
    ↓
Blockchain verification status
Poll for updates every 3 seconds
```

### Step 4: Review & Accept (Recruiter)
```
Recruiter → Dashboard → Applications Tab
    ↓
See all submissions across all jobs
    ↓
For each submission:
  - Submission ID
  - AI Score & Bucket
  - Current Status
    ↓
Click "Accept" → Updates status to "accepted"
    ↓
Blockchain records acceptance
```

### Step 5: Claim Position (Candidate)
```
Candidate → Status Page → See "Accepted"
    ↓
Click "Claim Position"
    ↓
Sign message with MetaMask: "claim:{submission_id}"
    ↓
Backend verifies signature
    ↓
Updates status to "claimed"
    ↓
Position officially claimed!
```

## 📊 Data Models

### Job
```javascript
{
  job_id: "JOB-abc123",
  title: "Software Engineer",
  description: "Full-stack developer",
  requirements: "React, Python, AWS",
  location: "Remote",
  salary: "$80k-120k",
  contract_address: "0x..."
}
```

### Submission
```javascript
{
  submission_id: "0xabc...",
  job_id: "JOB-abc123",
  wallet_address: "0x123...",
  resume_hash: "0x...",
  model_hash: "0x...",
  score_hash: "0x...",
  score: 0.85,
  decision: "auto_pass",
  status: "pending",
  tx_hash: "0x9f8a...",
  enc_email: "encrypted_string"
}
```

## 🔐 Security & Privacy

### Resume Privacy
- PDF uploaded to backend
- Text extracted (PII removed)
- Only anonymized text sent to ML
- Original PDF not stored permanently

### Blockchain Verification
- All decisions recorded on Sepolia testnet
- Hashes prevent tampering:
  - Resume hash
  - Model hash
  - Score hash
- Transaction hash for verification

### Wallet Authentication
- MetaMask integration
- Personal_sign for claims
- Signature verification
- Wallet-based access control

## 🎨 UI/UX Design Principles

### Design System
- **Framework:** TailwindCSS
- **Colors:** 
  - Primary: Blue (#3b82f6)
  - Success: Green
  - Warning: Yellow
  - Error: Red
- **Typography:** Inter font family
- **Layout:** Centered, max-width 7xl

### Components
- Card-style sections
- Subtle shadows
- Generous white space
- Micro-interactions
- Toast notifications
- Loading states
- Empty states
- Responsive tables

## 📱 Pages Overview

### 1. Home (`/`)
- Hero section
- Upload form
- Job ID input
- Submit button
- Privacy information

### 2. My Applications (`/my-applications`)
- Table of all applications
- Filterable by wallet
- Score progress bars
- Status badges
- View details button

### 3. Status (`/status?submission_id=...`)
- Decision card
- AI score visualization
- Blockchain verification
- Claim button (if accepted)
- Polling controls

### 4. Recruiter Dashboard (`/recruiter`)
- **My Jobs Tab:**
  - Job listings table
  - Job IDs with copy button
  - Job details
- **Applications Tab:**
  - Submissions table
  - Score and bucket
  - Accept/View Details actions

## 🔗 API Endpoints Reference

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/apply` | POST | Submit application | Wallet |
| `/api/status` | GET | Check status | Public |
| `/api/claim` | POST | Claim position | Signature |
| `/api/accept` | POST | Accept submission | Admin |
| `/api/job` | POST | Create job | Admin |
| `/api/jobs` | GET | List all jobs | Public |
| `/api/job/{id}/summary` | GET | Job details | Public |
| `/api/submissions` | GET | List submissions | Admin |

## 🚀 Deployment Checklist

### Backend
- [ ] Install dependencies: `pip install -r backend/requirements.txt`
- [ ] Set environment variables (blockchain RPC, etc.)
- [ ] Start server: `python start_backend.py`
- [ ] Verify at http://localhost:8000

### Frontend
- [ ] Install dependencies: `npm install`
- [ ] Configure API URL in .env
- [ ] Start dev server: `npm start`
- [ ] Verify at http://localhost:3000

### MetaMask Setup
- [ ] Install MetaMask extension
- [ ] Switch to Sepolia testnet
- [ ] Get test ETH from faucet
- [ ] Connect to application

## 🧪 Testing Checklist

### Candidate Tests
- [ ] Connect wallet
- [ ] Upload PDF resume
- [ ] Get AI screening results
- [ ] View blockchain verification
- [ ] Check "My Applications" page
- [ ] Claim accepted position

### Recruiter Tests
- [ ] Create new job
- [ ] Copy job ID
- [ ] View job in "My Jobs" tab
- [ ] See applications in "Applications" tab
- [ ] Accept submission
- [ ] View submission details

### Integration Tests
- [ ] End-to-end application flow
- [ ] Wallet persistence across pages
- [ ] Status polling updates
- [ ] Blockchain verification links
- [ ] Error handling

## 📈 Future Enhancements

1. **Real Blockchain Integration**
   - Deploy to mainnet
   - Actual smart contracts
   - Gas optimization

2. **Real ML Service**
   - Advanced NLP models
   - Better resume parsing
   - Skills extraction

3. **Enhanced Features**
   - Job search/filtering
   - Application analytics
   - Email notifications
   - Video interviews
   - Reference checks

4. **Database**
   - PostgreSQL/MongoDB
   - Data persistence
   - Backup systems

5. **Authentication**
   - Multi-wallet support
   - Social login
   - 2FA

## 🎓 Learning Resources

- React: https://react.dev
- TailwindCSS: https://tailwindcss.com
- FastAPI: https://fastapi.tiangolo.com
- Ethers.js: https://docs.ethers.org
- Web3: https://web3js.readthedocs.io

---

**Built with ❤️ for fair and transparent hiring**
