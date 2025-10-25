from eth_account.messages import encode_defunct
from eth_account import Account
import hashlib

def verify_signature(submission_id: str, signature: str, wallet_address: str) -> bool:
    """Verify that the signature matches the wallet address"""
    try:
        # Create the message that was signed
        message = f"claim:{submission_id}"
        
        # Encode the message
        message_hash = encode_defunct(text=message)
        
        # Recover the address from the signature
        recovered_address = Account.recover_message(message_hash, signature=signature)
        
        # Check if the recovered address matches the expected wallet address
        return recovered_address.lower() == wallet_address.lower()
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False
