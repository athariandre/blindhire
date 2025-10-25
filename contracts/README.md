# 🔐 BlindHire Smart Contracts

Solidity contracts for the BlindHire provably fair AI resume screening system.

## 📁 Contract Architecture

### JobFactory.sol
Factory contract that deploys individual `JobContract` instances. Each job posting gets its own contract for isolated, provably fair evaluation tracking.

**Key Functions:**
- `createJob(bytes32 jobConfigHash, bytes jobOwnerPubEncKey)` - Deploy a new job contract
- `getJobsByOwner(address owner)` - Get all jobs for a recruiter
- `jobExists(bytes32 configHash)` - Check if a job exists

### JobContract.sol
Stores cryptographic commitments for resume evaluations. Ensures transparency and verifiability.

**Key Functions:**
- `computeSubmissionId(address, bytes32, bytes32)` - Generate submission ID
- `commitEvaluation(...)` - Store evaluation commitments on-chain
- `verifyEvaluation(...)` - Verify commitments match expected values
- `getEvaluation(bytes32)` - Retrieve commitment details

**Commitment Structure:**
- `resumeHash` - sha256 of anonymized resume text
- `modelHash` - sha256 of ML model identifier
- `scoreHash` - sha256 of canonical JSON score payload
- `encEmailHash` - hash of encrypted applicant email (optional)

## 🚀 Setup

### 1. Install Dependencies
```bash
cd contracts
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required variables:
- `SEPOLIA_RPC_URL` - Sepolia testnet RPC endpoint
- `PRIVATE_KEY` - Deployer wallet private key (fund with Sepolia ETH)
- `ETHERSCAN_API_KEY` - For contract verification

### 3. Compile Contracts
```bash
npm run compile
```

## 📦 Deployment

### Deploy to Sepolia Testnet
```bash
npm run deploy:sepolia
```

### Deploy to Local Hardhat Network
```bash
# Terminal 1: Start local node
npm run node

# Terminal 2: Deploy
npm run deploy:local
```

### After Deployment
1. Copy the `JobFactory` address from deployment output
2. Update `backend/.env` with `FACTORY_CONTRACT_ADDRESS=<address>`
3. Deployment info is saved to `deployments/<network>.json`

## 🧪 Testing

```bash
npm test
```

## 🔍 Contract Verification

Contracts are automatically verified on Etherscan during deployment. To verify manually:

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS>
```

## 📊 Gas Reporting

Enable gas reporting in `.env`:
```bash
REPORT_GAS=true
```

Then run tests to see gas usage:
```bash
npm test
```

## 🔄 Workflow Integration

### Backend Integration
The backend calls these contract functions:

1. **Job Creation** (recruiter creates job)
   ```javascript
   jobAddress = await factory.createJob(jobConfigHash, pubEncKey)
   ```

2. **Commit Evaluation** (after ML scoring)
   ```javascript
   await jobContract.commitEvaluation(
     submissionId,
     resumeHash,
     modelHash,
     scoreHash,
     encEmailHash
   )
   ```

3. **Verify Result** (applicant verifies)
   ```javascript
   isValid = await jobContract.verifyEvaluation(
     submissionId,
     resumeHash,
     modelHash,
     scoreHash
   )
   ```

## 🏗️ Contract Addresses

### Sepolia Testnet
See `deployments/sepolia.json` for deployed contract addresses.

## 📝 Notes

- Each job posting gets its own `JobContract` instance
- Only job owners can commit evaluations to their job contracts
- All commitments are immutable once stored
- Applicants can verify their results at any time
- All events are indexed for easy querying

## 🛠️ Development Commands

```bash
npm run compile      # Compile contracts
npm run test         # Run tests
npm run clean        # Clean artifacts
npm run node         # Start local Hardhat node
npm run size         # Check contract sizes
npm run coverage     # Generate coverage report
```

## 🔒 Security Considerations

1. **Private Key Safety**: Never commit `.env` file or expose private keys
2. **Access Control**: Only job owners can commit evaluations to their contracts
3. **Immutability**: Evaluations cannot be modified once committed
4. **Hash Verification**: All hashes use sha256 for consistency with backend

## 📚 Additional Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [Ethers.js Documentation](https://docs.ethers.org/)
- [Sepolia Faucet](https://sepoliafaucet.com/)
- [Etherscan Sepolia](https://sepolia.etherscan.io/)
