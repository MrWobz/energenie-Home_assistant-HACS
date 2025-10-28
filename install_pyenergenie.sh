#!/bin/bash

# Install pyenergenie library and dependencies for Home Assistant Energenie integration
# Run this script if the automatic installation fails

echo "Installing pyenergenie library and dependencies for Energenie integration..."

# Check if we're in Home Assistant container
if [ -f /.dockerenv ]; then
    echo "Detected Home Assistant container environment"
else
    echo "Warning: This may not be running in Home Assistant environment"
fi

# Install RPi.GPIO first (required dependency)
echo "Step 1: Installing RPi.GPIO..."
if pip install RPi.GPIO; then
    echo "✅ RPi.GPIO installed successfully!"
else
    echo "❌ RPi.GPIO installation failed"
    echo "Note: This is normal if not running on Raspberry Pi hardware"
fi

# Try different installation methods for pyenergenie
echo "Step 2: Installing pyenergenie library..."
echo "Method 1: Installing from GitHub via pip..."
if pip install git+https://github.com/whaleygeek/pyenergenie.git; then
    echo "✅ pyenergenie installed successfully via pip!"
else
    echo "❌ pip install failed, trying alternative method..."
    
    echo "Method 2: Cloning and installing..."
    cd /tmp
    if git clone https://github.com/whaleygeek/pyenergenie.git; then
        cd pyenergenie
        if pip install .; then
            echo "✅ pyenergenie installed successfully via clone!"
        else
            echo "❌ Installation failed"
            exit 1
        fi
    else
        echo "❌ Git clone failed - check internet connection"
        exit 1
    fi
fi

# Test installations
echo "Step 3: Testing installations..."
echo "Testing RPi.GPIO..."
if python -c "import RPi.GPIO; print('RPi.GPIO import successful')"; then
    echo "✅ RPi.GPIO is working correctly!"
else
    echo "⚠️  RPi.GPIO import failed (may be normal if not on Raspberry Pi)"
fi

echo "Testing pyenergenie..."
if python -c "import energenie; print('pyenergenie import successful')"; then
    echo "✅ pyenergenie is working correctly!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Home Assistant"
    echo "2. Try adding the Energenie integration again"
else
    echo "❌ pyenergenie import failed"
    echo "Check that both RPi.GPIO and pyenergenie are installed correctly"
    exit 1
fi