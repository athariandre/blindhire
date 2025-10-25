#!/bin/bash

# BlindHire Environment Setup Script

echo "🚀 Setting up BlindHire Environment..."
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
# Blockchain Configuration
SEPOLIA_RPC_URL=https://rpc.sepolia.org
PRIVATE_KEY=
FACTORY_CONTRACT_ADDRESS=0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d

# Optional: For Etherscan verification
ETHERSCAN_API_KEY=

# API Configuration
API_BASE_URL=http://localhost:8000

# ML Service Configuration
ML_SERVICE_URL=http://localhost:5000
EOL
    echo "✅ .env file created"
    echo "⚠️  Please add your PRIVATE_KEY to .env file"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "📦 Installing Backend Dependencies..."
pip install -r backend/requirements.txt

echo ""
echo "📦 Installing Contract Dependencies..."
cd contracts
npm install
cd ..

echo ""
echo "📦 Installing Frontend Dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Add your PRIVATE_KEY to .env file"
echo "   2. Make sure you have SepoliaETH in your wallet"
echo "   3. Run 'python start_backend.py' to start backend"
echo "   4. Run 'cd frontend && npm start' to start frontend"
echo ""
echo "🎉 Happy Hiring!"
