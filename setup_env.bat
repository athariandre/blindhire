@echo off
echo.
echo 🚀 Setting up BlindHire Environment...
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    (
        echo # Blockchain Configuration
        echo SEPOLIA_RPC_URL=https://rpc.sepolia.org
        echo PRIVATE_KEY=
        echo FACTORY_CONTRACT_ADDRESS=0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d
        echo.
        echo # Optional: For Etherscan verification
        echo ETHERSCAN_API_KEY=
        echo.
        echo # API Configuration
        echo API_BASE_URL=http://localhost:8000
        echo.
        echo # ML Service Configuration
        echo ML_SERVICE_URL=http://localhost:5000
    ) > .env
    echo ✅ .env file created
    echo ⚠️  Please add your PRIVATE_KEY to .env file
) else (
    echo ℹ️  .env file already exists
)

echo.
echo 📦 Installing Backend Dependencies...
pip install -r backend/requirements.txt

echo.
echo 📦 Installing Contract Dependencies...
cd contracts
call npm install
cd ..

echo.
echo 📦 Installing Frontend Dependencies...
cd frontend
call npm install
cd ..

echo.
echo ✅ Setup Complete!
echo.
echo 📋 Next Steps:
echo    1. Add your PRIVATE_KEY to .env file
echo    2. Make sure you have Sepolia ETH in your wallet
echo    3. Run 'python start_backend.py' to start backend
echo    4. Run 'cd frontend && npm start' to start frontend
echo.
echo 🎉 Happy Hiring!
pause
