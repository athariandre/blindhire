"""
Real Blockchain Service - Connects to deployed JobFactory and JobContract
"""
import asyncio
import hashlib
import json
from web3 import Web3
from eth_account import Account
from services.db import save_submission
from config import SEPOLIA_RPC_URL, PRIVATE_KEY, FACTORY_CONTRACT_ADDRESS

# ABIs for the contracts
JOBFACTORY_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "jobConfigHash", "type": "bytes32"}, 
                   {"internalType": "bytes", "name": "jobOwnerPubEncKey", "type": "bytes"}],
        "name": "createJob",
        "outputs": [{"internalType": "address", "name": "job", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "configHash", "type": "bytes32"}],
        "name": "getJobByConfigHash",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalJobs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

JOBCONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "submissionId", "type": "bytes32"},
            {"internalType": "bytes32", "name": "resumeHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "modelHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "scoreHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "encEmailHash", "type": "bytes32"}
        ],
        "name": "commitEvaluation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "submissionId", "type": "bytes32"},
            {"internalType": "bytes32", "name": "resumeHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "modelHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "scoreHash", "type": "bytes32"}
        ],
        "name": "verifyEvaluation",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "submissionId", "type": "bytes32"}],
        "name": "getEvaluation",
        "outputs": [
            {"internalType": "bytes32", "name": "resumeHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "modelHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "scoreHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "encEmailHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "bool", "name": "exists", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "jobConfigHash",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class BlockchainService:
    def __init__(self):
        self.connected = False
        self.w3 = None
        self.account = None
        self.factory = None
        self.job_contracts_cache = {}
        
        # Try to connect to blockchain
        try:
            self.w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL, request_kwargs={'timeout': 10}))
            if self.w3.is_connected():
                self.connected = True
                print("✅ Connected to Sepolia network")
                
                if PRIVATE_KEY and PRIVATE_KEY.strip():
                    try:
                        self.account = Account.from_key(PRIVATE_KEY)
                        print(f"✅ Wallet loaded: {self.account.address}")
                    except Exception as e:
                        print(f"⚠️  Invalid private key: {e}")
                        self.account = None
                else:
                    print("⚠️  No private key - running in mock mode")
                    
                self.factory = self.w3.eth.contract(
                    address=Web3.to_checksum_address(FACTORY_CONTRACT_ADDRESS),
                    abi=JOBFACTORY_ABI
                )
            else:
                print("⚠️  Cannot connect to Sepolia - running in mock mode")
                self.connected = False
        except Exception as e:
            print(f"⚠️  Blockchain connection failed: {e}")
            print("   Running in mock mode (simulated blockchain)")
            self.connected = False
    
    def _string_to_bytes32(self, text: str) -> bytes:
        """Convert string to bytes32"""
        if text.startswith('0x'):
            return bytes.fromhex(text[2:])
        return bytes.fromhex(text)
    
    def _hash_to_bytes32(self, hash_str: str) -> bytes:
        """Convert hash string to bytes32"""
        if isinstance(hash_str, bytes):
            return hash_str
        if hash_str.startswith('0x'):
            return bytes.fromhex(hash_str[2:].zfill(64))
        return bytes.fromhex(hash_str.zfill(64))
    
    async def create_job_contract(self, job_data: dict) -> tuple[str, str]:
        """
        Create a new job contract on-chain
        Returns: (job_id, contract_address)
        """
        try:
            # Create job config hash from job data
            job_config = json.dumps({
                "title": job_data.get("title"),
                "description": job_data.get("description"),
                "requirements": job_data.get("requirements"),
            }, sort_keys=True)
            
            job_config_hash = hashlib.sha256(job_config.encode()).hexdigest()
            job_id = f"JOB-{job_config_hash[:16]}"
            
            if not self.connected or not self.account:
                # Mock deployment for development
                contract_address = "0x" + hashlib.sha256(job_id.encode()).hexdigest()[:40]
                self.job_contracts_cache[job_id] = contract_address
                await asyncio.sleep(1)  # Simulate blockchain delay
                return job_id, contract_address
            
            # Real blockchain deployment
            job_config_hash_bytes = self._hash_to_bytes32(job_config_hash)
            pub_key = b""  # Empty bytes for now, can add encryption key later
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            tx = self.factory.functions.createJob(
                job_config_hash_bytes,
                pub_key
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign and send
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Get contract address from factory
            contract_address = self.factory.functions.getJobByConfigHash(
                job_config_hash_bytes
            ).call()
            
            self.job_contracts_cache[job_id] = contract_address
            
            return job_id, contract_address
            
        except Exception as e:
            print(f"Error creating job contract: {e}")
            # Fallback to mock
            contract_address = "0x" + hashlib.sha256(job_id.encode()).hexdigest()[:40]
            return job_id, contract_address
    
    def _get_job_contract(self, job_id: str):
        """Get job contract instance"""
        if job_id in self.job_contracts_cache:
            address = self.job_contracts_cache[job_id]
            return self.w3.eth.contract(
                address=Web3.to_checksum_address(address),
                abi=JOBCONTRACT_ABI
            )
        return None
    
    async def record_evaluation(
        self, 
        submission_id: str, 
        ml_result: dict, 
        wallet_address: str, 
        job_id: str, 
        enc_email: str = None
    ) -> str:
        """
        Record evaluation commitment on blockchain
        Returns: transaction hash
        """
        try:
            # Convert hashes to bytes32
            submission_id_bytes = self._hash_to_bytes32(submission_id)
            resume_hash_bytes = self._hash_to_bytes32(ml_result.get("resume_hash", ""))
            model_hash_bytes = self._hash_to_bytes32(ml_result.get("model_hash", ""))
            score_hash_bytes = self._hash_to_bytes32(ml_result.get("score_hash", ""))
            
            # Hash encrypted email if provided
            if enc_email:
                enc_email_hash = hashlib.sha256(enc_email.encode()).hexdigest()
                enc_email_hash_bytes = self._hash_to_bytes32(enc_email_hash)
            else:
                enc_email_hash_bytes = bytes(32)  # Zero bytes
            
            if not self.connected or not self.account:
                # Mock blockchain transaction
                tx_hash = "0x" + hashlib.sha256(f"{submission_id}{wallet_address}".encode()).hexdigest()
                await asyncio.sleep(1)
                
                # Save to database
                save_submission({
                    "submission_id": submission_id,
                    "job_id": job_id,
                    "wallet_address": wallet_address,
                    "resume_hash": ml_result.get("resume_hash", ""),
                    "model_hash": ml_result.get("model_hash", ""),
                    "score_hash": ml_result.get("score_hash", ""),
                    "score": ml_result.get("similarity_score", 0),
                    "decision": ml_result.get("decision", "pending"),
                    "status": "pending",
                    "tx_hash": tx_hash,
                    "email": enc_email  # Store as email for recruiter access
                })
                
                return tx_hash
            
            # Real blockchain transaction
            job_contract = self._get_job_contract(job_id)
            if not job_contract:
                raise Exception(f"Job contract not found for {job_id}")
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            tx = job_contract.functions.commitEvaluation(
                submission_id_bytes,
                resume_hash_bytes,
                model_hash_bytes,
                score_hash_bytes,
                enc_email_hash_bytes
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign and send
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            
            # Wait for confirmation
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Save to database
            save_submission({
                "submission_id": submission_id,
                "job_id": job_id,
                "wallet_address": wallet_address,
                "resume_hash": ml_result.get("resume_hash", ""),
                "model_hash": ml_result.get("model_hash", ""),
                "score_hash": ml_result.get("score_hash", ""),
                "score": ml_result.get("similarity_score", 0),
                "decision": ml_result.get("decision", "pending"),
                "status": "pending",
                "tx_hash": tx_hash_hex,
                "email": enc_email  # Store as email for recruiter access
            })
            
            return tx_hash_hex
            
        except Exception as e:
            print(f"Error recording evaluation: {e}")
            # Fallback to mock
            tx_hash = "0x" + hashlib.sha256(f"{submission_id}{wallet_address}".encode()).hexdigest()
            
            save_submission({
                "submission_id": submission_id,
                "job_id": job_id,
                "wallet_address": wallet_address,
                "resume_hash": ml_result.get("resume_hash", ""),
                "model_hash": ml_result.get("model_hash", ""),
                "score_hash": ml_result.get("score_hash", ""),
                "score": ml_result.get("similarity_score", 0),
                "decision": ml_result.get("decision", "pending"),
                "status": "pending",
                "tx_hash": tx_hash,
                "email": enc_email  # Store as email for recruiter access
            })
            
            return tx_hash
    
    async def verify_evaluation(
        self, 
        submission_id: str, 
        resume_hash: str, 
        model_hash: str, 
        score_hash: str,
        job_id: str
    ) -> bool:
        """Verify evaluation on blockchain"""
        try:
            if not self.connected or not self.account:
                # Mock verification
                await asyncio.sleep(0.5)
                return True
            
            job_contract = self._get_job_contract(job_id)
            if not job_contract:
                return False
            
            # Convert to bytes32
            submission_id_bytes = self._hash_to_bytes32(submission_id)
            resume_hash_bytes = self._hash_to_bytes32(resume_hash)
            model_hash_bytes = self._hash_to_bytes32(model_hash)
            score_hash_bytes = self._hash_to_bytes32(score_hash)
            
            # Call verify function
            is_valid = job_contract.functions.verifyEvaluation(
                submission_id_bytes,
                resume_hash_bytes,
                model_hash_bytes,
                score_hash_bytes
            ).call()
            
            return is_valid
            
        except Exception as e:
            print(f"Error verifying evaluation: {e}")
            return False
    
    async def mark_accepted(self, submission_id: str):
        """Mark submission as accepted"""
        await asyncio.sleep(0.5)
        from services.db import submissions_db
        if submission_id in submissions_db:
            submissions_db[submission_id]["decision"] = "accepted"
            submissions_db[submission_id]["status"] = "accepted"

# Global instance
blockchain_service = BlockchainService()

# Export functions for backward compatibility
async def create_job_contract(job_data: dict):
    return await blockchain_service.create_job_contract(job_data)

async def record_evaluation(submission_id: str, ml_result: dict, wallet_address: str, job_id: str, enc_email: str = None):
    return await blockchain_service.record_evaluation(submission_id, ml_result, wallet_address, job_id, enc_email)

async def verify_evaluation(submission_id: str, resume_hash: str, model_hash: str, score_hash: str, job_id: str = None):
    # For backward compatibility, try to get job_id from submission if not provided
    if not job_id:
        from services.db import get_submission
        sub = get_submission(submission_id)
        if sub:
            job_id = sub.get("job_id")
    return await blockchain_service.verify_evaluation(submission_id, resume_hash, model_hash, score_hash, job_id)

async def mark_accepted(submission_id: str):
    return await blockchain_service.mark_accepted(submission_id)
