# BlindHire - Blockchain Integration Guide

## 🎯 Overview

BlindHire now uses **real smart contracts** deployed on Sepolia testnet to ensure provably fair resume screening. Every evaluation is recorded on-chain with cryptographic commitments.

## 📜 Smart Contracts

### Deployed Contracts

| Contract | Address | Network |
|----------|---------|---------|
| JobFactory | `0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d` | Sepolia |

### Contract Architecture

```
JobFactory (0x04E2AF...)
    │
    ├─► JobContract (Job 1)
    │   ├─ EvaluationCommitment (Submission 1)
    │   ├─ EvaluationCommitment (Submission 2)
    │   └─ ...
    │
    ├─► JobContract (Job 2)
    │   └─ ...
    │
    └─► ...
```

### JobFactory Contract

**Purpose:** Factory pattern to deploy individual JobContract instances

**Key Functions:**
- `createJob(bytes32 jobConfigHash, bytes jobOwnerPubEncKey)` - Deploy new job contract
- `getJobByConfigHash(bytes32 configHash)` - Get job contract address
- `getTotalJobs()` - Get total number of jobs

### JobContract

**Purpose:** Store evaluation commitments for a single job

**Key Functions:**
- `commitEvaluation(...)` - Store evaluation on-chain
- `verifyEvaluation(...)` - Verify evaluation hasn't been tampered
- `getEvaluation(bytes32 submissionId)` - Get evaluation details

## 🔄 Application Flow with Blockchain

### 1. Job Creation Flow

```
Recruiter → Frontend → Backend → BlockchainService
                                      ↓
                                  JobFactory.createJob()
                                      ↓
                                  Deploy JobContract
                                      ↓
Backend ← Contract Address ← Event Emitted
    ↓
Store job_id → contract_address mapping
    ↓
Return job_id to Frontend
```

**Code:**
```python
# backend/services/blockchain_service.py
async def create_job_contract(job_data: dict):
    # Hash job configuration
    job_config = json.dumps(job_data, sort_keys=True)
    job_config_hash = hashlib.sha256(job_config.encode()).hexdigest()
    
    # Deploy via factory
    tx = factory.functions.createJob(
        job_config_hash_bytes,
        pub_key
    ).build_transaction({...})
    
    # Sign and send
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Get contract address
    contract_address = factory.functions.getJobByConfigHash(
        job_config_hash_bytes
    ).call()
    
    return job_id, contract_address
```

### 2. Application Submission Flow

```
Candidate → Upload Resume → Backend
                              ↓
                          ML Service (AI Scoring)
                              ↓
                          Generate Hashes:
                          - resume_hash (SHA256)
                          - model_hash (SHA256)
                          - score_hash (SHA256)
                              ↓
                          BlockchainService
                              ↓
                      JobContract.commitEvaluation()
                              ↓
                      Transaction Confirmed
                              ↓
            Return: submission_id, score, decision, tx_hash
```

**Code:**
```python
# backend/routes/apply.py
async def apply(...):
    # Extract resume text
    resume_text = extract_from_pdf(resume_pdf)
    
    # ML Service
    ml_result = await call_ml_service(resume_text, job_id)
    # Returns: resume_hash, model_hash, score_hash, score, decision
    
    # Create submission ID
    submission_id = keccak256(wallet_address + job_id + resume_hash)
    
    # Record on blockchain
    tx_hash = await record_evaluation(
        submission_id, 
        ml_result, 
        wallet_address, 
        job_id
    )
    
    return {
        "submission_id": submission_id,
        "score": ml_result["similarity_score"],
        "decision": ml_result["decision"],
        "tx_hash": tx_hash
    }
```

### 3. Verification Flow

```
Frontend → Check Status → Backend
                            ↓
                    Get submission from DB
                            ↓
                    BlockchainService
                            ↓
            JobContract.verifyEvaluation(
                submission_id,
                resume_hash,
                model_hash,
                score_hash
            )
                            ↓
                    Returns: true/false
                            ↓
            Frontend ← verified status
```

## 🔐 Cryptographic Commitments

### What Gets Stored On-Chain

For each application, we store:

```solidity
struct EvaluationCommitment {
    bytes32 resumeHash;        // SHA256(anonymized_resume_text)
    bytes32 modelHash;         // SHA256(model_identifier)
    bytes32 scoreHash;         // SHA256(canonical_json_score)
    bytes32 encEmailHash;      // SHA256(encrypted_email) - optional
    uint256 timestamp;         // Block timestamp
    bool exists;               // Existence flag
}
```

### Hash Generation

**Resume Hash:**
```python
resume_text = extract_and_anonymize(pdf)
resume_hash = hashlib.sha256(resume_text.encode()).hexdigest()
```

**Model Hash:**
```python
model_id = "gpt-3.5-resume-v1"
model_hash = hashlib.sha256(model_id.encode()).hexdigest()
```

**Score Hash:**
```python
score_payload = json.dumps({
    "score": 0.85,
    "decision": "auto_pass",
    "timestamp": "2025-10-25T19:00:00Z"
}, sort_keys=True)
score_hash = hashlib.sha256(score_payload.encode()).hexdigest()
```

### Why This Matters

1. **Tamper-Proof:** Once committed, evaluations cannot be changed
2. **Verifiable:** Anyone can verify their results match blockchain
3. **Transparent:** All decisions are publicly auditable
4. **Fair:** AI model and decisions are committed before applicant sees results

## 🛠️ Setup & Configuration

### 1. Environment Variables

Create `.env` file in project root:

```bash
# Blockchain Configuration
SEPOLIA_RPC_URL=https://rpc.sepolia.org
PRIVATE_KEY=your_wallet_private_key_here
FACTORY_CONTRACT_ADDRESS=0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d

# Optional
ETHERSCAN_API_KEY=your_etherscan_api_key
```

### 2. Get Sepolia ETH

1. Go to [Sepolia Faucet](https://sepoliafaucet.com/)
2. Enter your wallet address
3. Wait for test ETH to arrive
4. You need ~0.1 ETH for testing

### 3. Install Dependencies

```bash
# Backend
pip install -r backend/requirements.txt

# Contracts
cd contracts
npm install
cd ..
```

### 4. Start Services

```bash
# Terminal 1: Backend
python start_backend.py

# Terminal 2: Frontend
cd frontend
npm start
```

## 📊 Monitoring Transactions

### View on Etherscan

Every transaction gets a hash that you can view on Sepolia Etherscan:

```
https://sepolia.etherscan.io/tx/{tx_hash}
```

### Check Factory Contract

```
https://sepolia.etherscan.io/address/0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d
```

### Query Job Contracts

```javascript
// Get total jobs
const totalJobs = await jobFactory.getTotalJobs();

// Get job contract address
const jobAddress = await jobFactory.getJobByConfigHash(configHash);

// Get evaluation
const jobContract = new ethers.Contract(jobAddress, JOB_ABI, provider);
const evaluation = await jobContract.getEvaluation(submissionId);
```

## 🧪 Testing

### Test Job Creation

```bash
cd contracts
npx hardhat test --grep "should create a new job"
```

### Test Evaluation Commitment

```bash
npx hardhat test --grep "should commit evaluation"
```

### Test Verification

```bash
npx hardhat test --grep "should verify evaluation"
```

## 🔄 Development Mode (No Private Key)

If you don't have a private key, the system will run in **mock mode**:

- Transactions are simulated
- Hashes are generated locally
- Everything works except actual blockchain writes
- Perfect for frontend development

Just leave `PRIVATE_KEY` empty in `.env`

## 🚀 Production Deployment

### 1. Deploy to Mainnet

```bash
cd contracts
npx hardhat run scripts/deploy.js --network mainnet
```

### 2. Update Configuration

Update `.env` with mainnet addresses:

```bash
MAINNET_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
FACTORY_CONTRACT_ADDRESS=0xYourMainnetFactoryAddress
```

### 3. Security Considerations

- ✅ Use hardware wallet for production
- ✅ Keep private keys in secrets manager
- ✅ Enable rate limiting
- ✅ Add monitoring/alerts
- ✅ Test thoroughly on testnet first

## 📈 Gas Costs (Sepolia)

| Operation | Gas Used | Estimated Cost (at 50 gwei) |
|-----------|----------|------------------------------|
| Create Job | ~1,500,000 | ~0.075 ETH (~$150 @ $2000/ETH) |
| Commit Evaluation | ~150,000 | ~0.0075 ETH (~$15) |
| Verify Evaluation | Free (read-only) | $0 |

## 🐛 Troubleshooting

### Issue: "Failed to connect to Sepolia network"

**Solution:**
- Check `SEPOLIA_RPC_URL` in `.env`
- Try alternative RPC: `https://ethereum-sepolia.publicnode.com`
- Check internet connection

### Issue: "Insufficient funds"

**Solution:**
- Get more Sepolia ETH from faucet
- Check wallet balance on Etherscan

### Issue: "Transaction reverted"

**Solution:**
- Check gas limit is sufficient
- Verify contract addresses are correct
- Check evaluation doesn't already exist

### Issue: "Nonce too low"

**Solution:**
- Reset nonce in MetaMask
- Wait for pending transactions to confirm

## 📚 Additional Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethers.js Documentation](https://docs.ethers.org/)
- [Sepolia Testnet](https://sepolia.dev/)

---

**🎓 Learn More:**
- [Smart Contract Security](https://consensys.github.io/smart-contract-best-practices/)
- [Gas Optimization](https://www.alchemy.com/overviews/solidity-gas-optimization)
- [Commitment Schemes](https://en.wikipedia.org/wiki/Commitment_scheme)
