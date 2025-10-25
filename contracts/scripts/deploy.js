const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

/**
 * Deploy JobFactory to Sepolia testnet
 * 
 * This script:
 * 1. Deploys the JobFactory contract
 * 2. Verifies the contract on Etherscan
 * 3. Saves deployment information to a JSON file
 * 
 * Usage:
 *   npx hardhat run deploy.js --network sepolia
 */
async function main() {
  console.log("🚀 Starting BlindHire contract deployment...\n");

  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  const deployerAddress = await deployer.getAddress();
  const balance = await hre.ethers.provider.getBalance(deployerAddress);

  console.log("📋 Deployment Details:");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log(`Network:         ${hre.network.name}`);
  console.log(`Deployer:        ${deployerAddress}`);
  console.log(`Balance:         ${hre.ethers.formatEther(balance)} ETH`);
  console.log(`Block Number:    ${await hre.ethers.provider.getBlockNumber()}`);
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

  // Check if deployer has enough balance
  if (balance === 0n) {
    console.error("❌ Error: Deployer account has no ETH balance");
    console.error("   Please fund the account before deploying");
    process.exit(1);
  }

  try {
    // Deploy JobFactory
    console.log("📦 Deploying JobFactory contract...");
    const JobFactory = await hre.ethers.getContractFactory("JobFactory");
    const jobFactory = await JobFactory.deploy();
    
    await jobFactory.waitForDeployment();
    const factoryAddress = await jobFactory.getAddress();

    console.log(`✅ JobFactory deployed to: ${factoryAddress}\n`);

    // Get deployment transaction
    const deployTx = jobFactory.deploymentTransaction();
    console.log("📊 Deployment Transaction:");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log(`TX Hash:         ${deployTx.hash}`);
    console.log(`Block Number:    ${deployTx.blockNumber}`);
    console.log(`Gas Used:        ${deployTx.gasLimit.toString()}`);
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    // Wait for a few confirmations
    console.log("⏳ Waiting for confirmations...");
    await jobFactory.deploymentTransaction().wait(5);
    console.log("✅ Confirmed!\n");

    // Verify contract on Etherscan (if not on localhost)
    if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
      console.log("🔍 Verifying contract on Etherscan...");
      try {
        await hre.run("verify:verify", {
          address: factoryAddress,
          constructorArguments: [],
        });
        console.log("✅ Contract verified on Etherscan\n");
      } catch (error) {
        if (error.message.includes("Already Verified")) {
          console.log("ℹ️  Contract already verified on Etherscan\n");
        } else {
          console.error("❌ Verification failed:", error.message);
          console.log("   You can verify manually later\n");
        }
      }
    }

    // Get contract version
    const version = await jobFactory.VERSION();
    const platformOwner = await jobFactory.platformOwner();

    console.log("📄 Contract Information:");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log(`Version:         ${version}`);
    console.log(`Platform Owner:  ${platformOwner}`);
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    // Save deployment information
    const deploymentInfo = {
      network: hre.network.name,
      chainId: hre.network.config.chainId,
      deployer: deployerAddress,
      contracts: {
        JobFactory: {
          address: factoryAddress,
          version: version,
          deploymentTx: deployTx.hash,
          blockNumber: deployTx.blockNumber,
          timestamp: new Date().toISOString(),
        },
      },
    };

    const deploymentsDir = path.join(__dirname, "deployments");
    if (!fs.existsSync(deploymentsDir)) {
      fs.mkdirSync(deploymentsDir);
    }

    const deploymentFile = path.join(
      deploymentsDir,
      `${hre.network.name}.json`
    );
    fs.writeFileSync(deploymentFile, JSON.stringify(deploymentInfo, null, 2));

    console.log(`💾 Deployment info saved to: ${deploymentFile}\n`);

    // Print summary
    console.log("╔═══════════════════════════════════════════════════════════╗");
    console.log("║            🎉 DEPLOYMENT SUCCESSFUL 🎉                   ║");
    console.log("╠═══════════════════════════════════════════════════════════╣");
    console.log(`║ JobFactory:  ${factoryAddress} ║`);
    console.log("╚═══════════════════════════════════════════════════════════╝");
    console.log("\n📝 Next Steps:");
    console.log("   1. Update backend/.env with FACTORY_CONTRACT_ADDRESS");
    console.log("   2. Test job creation: npx hardhat test");
    console.log("   3. Start the backend service");
    console.log("\n✨ BlindHire blockchain layer is ready!\n");

  } catch (error) {
    console.error("\n❌ Deployment failed:");
    console.error(error);
    process.exit(1);
  }
}

// Execute deployment
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
