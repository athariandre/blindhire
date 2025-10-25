# BlindHire - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- ✅ Node.js installed
- ✅ Python 3.8+ installed
- ✅ MetaMask browser extension
- ✅ Terminal/Command Prompt

---

## Step 1: Start the Backend (30 seconds)

Open Terminal 1:
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
python start_backend.py
```

✅ **Success:** You should see "Uvicorn running on http://0.0.0.0:8000"

---

## Step 2: Start the Frontend (30 seconds)

Open Terminal 2:
```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start React app
npm start
```

✅ **Success:** Browser opens to http://localhost:3000

---

## Step 3: Connect MetaMask (30 seconds)

1. Open MetaMask extension
2. Switch to **Sepolia Testnet**
3. Click **"Connect Wallet"** button in app
4. Approve connection in MetaMask

✅ **Success:** You see your wallet address in the navbar

---

## Step 4: Test the System (3 minutes)

### As a Recruiter:

1. **Go to:** http://localhost:3000/recruiter
2. **Click:** "Create New Job"
3. **Fill in:**
   - Title: "Test Engineer"
   - Description: "Testing the system"
   - Requirements: "React, Python"
   - Location: "Remote"
   - Salary: "$100k"
4. **Submit**
5. **Copy the Job ID** from the alert

### As a Candidate:

1. **Go to:** http://localhost:3000
2. **Enter Job ID:** (paste the one you copied)
3. **Upload:** Any PDF file
4. **Submit**
5. **Wait 2-3 seconds** for AI processing
6. **View Results:** Score, Decision, TX Hash

### Check Your Applications:

1. **Go to:** http://localhost:3000/my-applications
2. **See:** Your application listed
3. **Click:** "View Details"

### Review as Recruiter:

1. **Go to:** http://localhost:3000/recruiter
2. **Click:** "Applications" tab
3. **See:** The submission you just made
4. **Click:** "Accept"

---

## 🎯 System Verification

### Backend Health Check
Open: http://localhost:8000
Expected: `{"message": "BlindHire backend running!"}`

### API Documentation
Open: http://localhost:8000/docs
Expected: Interactive API documentation

### Frontend Health
Open: http://localhost:3000
Expected: Beautiful landing page with "Connect Wallet" button

---

## 📍 Key URLs

| Page | URL | Purpose |
|------|-----|---------|
| Home | http://localhost:3000 | Apply to jobs |
| My Applications | http://localhost:3000/my-applications | Track your apps |
| Status | http://localhost:3000/status | Check specific application |
| Recruiter | http://localhost:3000/recruiter | Manage jobs & applications |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API docs |

---

## 🐛 Common Issues & Fixes

### Issue: "Port 3000 already in use"
```bash
# Kill the process
npx kill-port 3000
# Or use a different port
PORT=3001 npm start
```

### Issue: "Port 8000 already in use"
```bash
# Find and kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or (Mac/Linux)
lsof -ti:8000 | xargs kill -9
```

### Issue: "MetaMask not connecting"
1. Refresh the page
2. Make sure MetaMask is on Sepolia testnet
3. Try disconnecting and reconnecting

### Issue: "Backend not starting"
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies again
pip install -r backend/requirements.txt --force-reinstall
```

### Issue: "Frontend not loading"
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 🎬 Demo Script

**Perfect for demos/presentations:**

1. **[0:00-0:30] Introduction**
   - "This is BlindHire - a fair, AI-powered hiring platform"
   - Show homepage

2. **[0:30-1:30] Recruiter Creates Job**
   - Go to recruiter dashboard
   - Create job
   - Show Job ID generation
   - Copy Job ID

3. **[1:30-3:00] Candidate Applies**
   - Go to home page
   - Enter Job ID
   - Upload resume
   - Show AI processing
   - Show results (score, decision, blockchain TX)

4. **[3:00-4:00] Track Application**
   - Go to "My Applications"
   - Show application status
   - Click to view details
   - Show blockchain verification

5. **[4:00-5:00] Recruiter Reviews**
   - Go back to recruiter dashboard
   - Show application in list
   - Accept the application
   - Show status update

6. **[5:00-5:30] Claim Position**
   - Go back to status page
   - Show "Accepted" status
   - Click "Claim Position"
   - Sign with MetaMask
   - Success!

---

## 📊 Test Data

### Sample Jobs
```javascript
{
  title: "Senior Software Engineer",
  description: "Full-stack development with React and Python",
  requirements: "5+ years experience, React, Python, AWS",
  location: "Remote",
  salary: "$120k-180k"
}

{
  title: "Frontend Developer",
  description: "Building beautiful UIs with React",
  requirements: "React, TypeScript, TailwindCSS",
  location: "San Francisco",
  salary: "$80k-120k"
}
```

### Sample Resume Content
Any PDF works, but for best results use one with:
- Work experience
- Skills section
- Education
- Projects

---

## 💡 Pro Tips

1. **Use Browser Dev Tools**
   - Press F12 to see console logs
   - Check Network tab for API calls
   - Monitor errors in real-time

2. **Keep Both Terminals Open**
   - Backend in one terminal
   - Frontend in another
   - Watch for errors in both

3. **Refresh Data**
   - Applications update in real-time
   - Use polling on status page
   - Refresh recruiter dashboard manually

4. **Test Different Scores**
   - The ML service generates random scores
   - Refresh to see different outcomes
   - High scores (>80%) auto-pass
   - Low scores (<50%) auto-reject

5. **Multiple Wallets**
   - Use different MetaMask accounts
   - Test as different candidates
   - See how applications are isolated

---

## 🎓 Next Steps

After you're comfortable with basics:

1. **Explore the Code**
   - Check `backend/routes/` for API logic
   - Look at `frontend/src/components/` for UI
   - Understand data flow in `frontend/src/utils/api.js`

2. **Customize**
   - Change colors in `tailwind.config.js`
   - Modify ML scoring in `backend/services/ml_client.py`
   - Add new features to components

3. **Deploy**
   - Backend: Heroku, Railway, or AWS
   - Frontend: Vercel, Netlify, or Cloudflare Pages
   - Database: PostgreSQL or MongoDB

4. **Extend**
   - Real blockchain integration
   - Advanced ML models
   - Email notifications
   - Analytics dashboard

---

**Need Help?** Check `COMPLETE_SYSTEM_OVERVIEW.md` for detailed documentation.

**Happy Hiring! 🎉**
