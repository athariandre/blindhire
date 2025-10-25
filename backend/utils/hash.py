import hashlib
from eth_utils import keccak

def sha256_hex(text: str) -> str:
    return "0x" + hashlib.sha256(text.encode()).hexdigest()

def keccak256(text: str) -> str:
    return "0x" + keccak(text=text).hex()
