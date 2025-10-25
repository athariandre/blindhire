const hre = require("hardhat");

async function main() {
  console.log("🔍 Checking BlindHire Setup...\n");
  
  try {
    // Get deployer account
    const [deployer] = await hre.ethers.getSigners();
    console.log("✅ Deployer address:", deployer.address);
    
    // Check balance
    const balance = await hre.ethers.provider.getBalance(deployer.address);
    const ethBalance = hre.ethers.formatEther(balance);
    console.log("💰 Balance:", ethBalance, "ETH");
    
    // Check network
    const network = await hre.ethers.provider.getNetwork();
    console.log("🌐 Network:", network.name, `(Chain ID: ${network.chainId})`);
    
    // Check block number
    const blockNumber = await hre.ethers.provider.getBlockNumber();
    console.log("📦 Current block:", blockNumber);
    
    console.log("\n" + "=".repeat(60));
    
    // Provide status
    if (balance === 0n) {
      console.log("⚠️  WARNING: No ETH balance!");
      console.log("\n📝 Next Steps:");
      console.log("1. Get Sepolia ETH from a faucet:");
      console.log("   - https://cloud.google.com/application/web3/faucet/ethereum/sepolia");
      console.log("   - https://www.alchemy.com/faucets/ethereum-sepolia");
      console.log("2. Send at least 0.01 ETH to:", deployer.address);
      console.log("3. Run this script again to verify");
    } else if (parseFloat(ethBalance) < 0.01) {
      console.log("⚠️  Low balance! You may need more ETH for deployment.");
      console.log("   Recommended: At least 0.01 ETH");
    } else {
      console.log("✅ Setup looks good! Ready to deploy!");
      console.log("\n📝 Next Steps:");
      console.log("1. Run tests: npx hardhat test");
      console.log("2. Deploy contracts: npx hardhat run scripts/deploy.js --network sepolia");
    }
    
  } catch (error) {
    console.error("❌ Error:", error.message);
    
    if (error.message.includes("invalid private key")) {
      console.log("\n💡 Fix: Check your PRIVATE_KEY in .env file");
      console.log("   Make sure it starts with 0x and is 64 hex characters");
    } else if (error.message.includes("could not detect network")) {
      console.log("\n💡 Fix: Check your SEPOLIA_RPC_URL in .env file");
      console.log("   Try using: https://rpc.sepolia.org");
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
