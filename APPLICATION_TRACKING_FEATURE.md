# Application Tracking Feature

## 🎯 Feature Overview
Complete application tracking system that allows:
- Recruiters to see all applications for their jobs
- Candidates to see all their applications tied to their wallet
- Real-time status updates based on wallet connection

## ✨ What Was Implemented

### Backend Changes

1. **Enhanced Database Functions**
   - `get_submissions_by_job(job_id)` - Get all submissions for a specific job
   - `get_submissions_by_wallet(wallet_address)` - Get all submissions for a wallet
   - Store job_id and wallet_address with each submission

2. **New Endpoint - GET /api/submissions**
   - Query params: `job_id` (optional), `wallet_address` (optional)
   - Returns filtered list of submissions
   - Located in `backend/routes/admin.py`

3. **Updated record_evaluation()**
   - Now stores job_id with submissions
   - Stores score, decision, and status
   - Links applications to specific jobs

### Frontend Changes

1. **Recruiter Dashboard - Applications Tab**
   - Shows all submissions across all jobs
   - Displays: Submission ID, Score, Bucket, Status
   - Real-time data from backend
   - Accept/View Details actions

2. **New Page - My Applications**
   - Dedicated page for candidates
   - Shows all applications for connected wallet
   - Displays: Job ID, AI Score, Decision, Status
   - Click to view full details
   - Auto-updates when wallet changes

3. **Navigation Updates**
   - Added "My Applications" link to navbar
   - Between "Home" and "Status"
   - Only accessible when wallet connected

4. **Data Flow**
   - Applications automatically tied to wallet on submission
   - Recruiter sees all applications
   - Candidate only sees their own applications
   - Status persists across sessions via wallet

## 🚀 User Flows

### Candidate Flow:
1. Connect wallet (e.g., 0xABC...)
2. Apply to job with ID "JOB-123"
3. Go to "My Applications"
4. See application with:
   - Job ID: JOB-123
   - AI Score: 85%
   - Decision: Passed
   - Status: Pending
5. Click "View Details" for more info
6. Status persists as long as same wallet is connected

### Recruiter Flow:
1. Create job → Get Job ID
2. Candidates apply to job
3. Go to Recruiter Dashboard
4. Switch to "Applications" tab
5. See all submissions:
   - Submission ID
   - Score & Bucket
   - Status
6. Accept or reject submissions
7. View detailed submission info

## 📋 API Endpoints

| Endpoint | Method | Description | Query Params |
|----------|--------|-------------|--------------|
| `/api/submissions` | GET | Get submissions | `job_id`, `wallet_address` |
| `/api/apply` | POST | Submit application | - |
| `/api/accept` | POST | Accept submission | - |

## 💡 Key Features

### For Candidates:
- ✅ See all your applications in one place
- ✅ Track status of each application
- ✅ View AI scores and decisions
- ✅ Status tied to wallet (persists)
- ✅ Direct link to detailed status page

### For Recruiters:
- ✅ See all applications across all jobs
- ✅ Filter by job (coming soon)
- ✅ Accept/reject applications
- ✅ View detailed candidate info
- ✅ Track application status

## 🔗 Data Persistence

Applications are stored with:
```json
{
  "submission_id": "0xabc...",
  "job_id": "JOB-123",
  "wallet_address": "0x123...",
  "score": 0.85,
  "decision": "auto_pass",
  "status": "pending",
  "tx_hash": "0x9f8a..."
}
```

This allows:
- Filtering by wallet address (candidate view)
- Filtering by job ID (recruiter view)
- Status persistence across sessions
- Blockchain verification via tx_hash

## 🎨 UI/UX Features

- Clean table layouts
- Color-coded badges (score, decision, status)
- Progress bars for AI scores
- Empty states with helpful messages
- Responsive design
- Hover effects on rows
- Copy buttons for IDs

## 🧪 Testing the Feature

1. **Backend Running:**
   ```bash
   python start_backend.py
   ```

2. **Frontend Running:**
   ```bash
   cd frontend && npm start
   ```

3. **Test Flow:**
   - Connect wallet (MetaMask)
   - Create job as recruiter
   - Copy job ID
   - Apply to job as candidate
   - Go to "My Applications"
   - See your application listed
   - Go to Recruiter Dashboard
   - See application in "Applications" tab
   - Accept the application
   - Refresh "My Applications"
   - See status updated to "Accepted"

## 🔮 Future Enhancements

- Filter applications by job in recruiter view
- Search functionality
- Sort by score, date, status
- Bulk actions (accept multiple)
- Application analytics
- Email notifications
- Download reports
