#!/bin/bash

# Covered Call Calculator - Bulletproof Installer v1.1
# Usage: curl -sSL https://raw.githubusercontent.com/jmd-jude/covered_call/main/install.sh | bash

set -e

echo "🎯 Installing Covered Call Calculator for Claude Desktop..."
echo ""

# Check if we're on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    PLATFORM="Mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/claude/claude_desktop_config.json"
    PLATFORM="Linux"
else
    echo "❌ Error: Unsupported operating system. This installer works on Mac and Linux only."
    exit 1
fi

echo "✅ Detected $PLATFORM"

# Function to test Python version
test_python() {
    local python_cmd=$1
    if command -v "$python_cmd" &> /dev/null; then
        local version_output=$($python_cmd --version 2>&1)
        local version=$(echo "$version_output" | grep -oE '[0-9]+\.[0-9]+' | head -1)
        local major=$(echo "$version" | cut -d. -f1)
        local minor=$(echo "$version" | cut -d. -f2)
        
        # Updated requirement: Python 3.10+ (MCP requirement)
        if [[ $major -eq 3 && $minor -ge 10 ]] || [[ $major -gt 3 ]]; then
            echo "$python_cmd"
            return 0
        fi
    fi
    return 1
}

# Find the best Python installation
echo "🔍 Checking for Python 3.10+..."

PYTHON_CMD=""
# Try common Python commands in order of preference (prioritize newer versions)
for cmd in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if PYTHON_CMD=$(test_python "$cmd"); then
        break
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    echo ""
    echo "❌ Python 3.10+ not found!"
    echo ""
    
    # Check if they have an older Python version
    for cmd in python3 python; do
        if command -v "$cmd" &> /dev/null; then
            local old_version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            if [[ -n "$old_version" ]]; then
                echo "Found Python $old_version, but the MCP library requires Python 3.10 or higher."
                echo ""
                break
            fi
        fi
    done
    
    echo "SOLUTION:"
    if [[ "$PLATFORM" == "Mac" ]]; then
        echo "1. 🌟 RECOMMENDED: Install Python 3.12 from https://www.python.org/downloads/"
        echo "   (Choose the 'macOS 64-bit universal2 installer')"
        echo ""
        echo "2. Alternative: Install via Homebrew"
        echo "   brew install python@3.12"
        echo ""
        echo "3. Alternative: Install via Mac App Store"
        echo "   Search for 'Python 3' and install Python 3.12+"
    else
        echo "Install Python 3.10+ using your package manager:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3.10 python3.10-venv"
        echo "  CentOS/RHEL: sudo dnf install python3.10 python3.10-venv"
        echo "  Arch: sudo pacman -S python"
    fi
    
    echo ""
    echo "After installing Python 3.10+, re-run this installer:"
    echo "curl -sSL https://raw.githubusercontent.com/jmd-jude/covered_call/main/install.sh | bash"
    echo ""
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi

echo "✅ Found Python: $PYTHON_CMD ($($PYTHON_CMD --version))"

# Test virtual environment creation
echo "🧪 Testing Python virtual environment..."
TEST_DIR="/tmp/python_test_$$"
if ! $PYTHON_CMD -m venv "$TEST_DIR" &>/dev/null; then
    echo "❌ Virtual environment creation failed!"
    echo ""
    echo "SOLUTION:"
    if [[ "$PLATFORM" == "Mac" ]]; then
        echo "Your Python installation might be incomplete. Try:"
        echo "1. $PYTHON_CMD -m pip install --upgrade pip"
        echo "2. If that fails, reinstall Python 3.12+ from https://www.python.org/downloads/"
    else
        echo "Install python venv module:"
        echo "  Ubuntu/Debian: sudo apt install python3.10-venv"
        echo "  CentOS/RHEL: sudo dnf install python3.10-venv"
    fi
    echo ""
    echo "Then re-run this installer."
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi
rm -rf "$TEST_DIR"
echo "✅ Python virtual environment working"

# Create installation directory
INSTALL_DIR="$HOME/.covered_call_calculator"
echo "📁 Installing to: $INSTALL_DIR"

# Remove existing installation if it exists
if [ -d "$INSTALL_DIR" ]; then
    echo "🔄 Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

# Create directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download the server file
echo "⬇️  Downloading calculator..."
if ! curl -sSL https://raw.githubusercontent.com/jmd-jude/covered_call/main/covered_call_server.py -o covered_call_server.py; then
    echo "❌ Download failed!"
    echo "Check your internet connection and try again."
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi

# Create virtual environment
echo "🐍 Setting up Python environment..."
if ! $PYTHON_CMD -m venv venv; then
    echo "❌ Failed to create virtual environment!"
    echo "Try reinstalling Python 3.12+ and run this installer again."
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate

# Aggressively upgrade pip (critical for MCP installation)
echo "🔄 Upgrading pip (required for MCP)..."
if ! pip install --upgrade pip --quiet; then
    echo "⚠️  Warning: Could not upgrade pip automatically."
    echo "This might cause MCP installation to fail."
    echo ""
    echo "If installation fails, try running:"
    echo "  $PYTHON_CMD -m pip install --upgrade pip"
    echo "Then re-run this installer."
fi

# Verify pip version
PIP_VERSION=$(pip --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "✅ Using pip version: $PIP_VERSION"

# Install MCP with better error handling
echo "📦 Installing MCP library..."
if ! pip install mcp --quiet; then
    echo "❌ Failed to install MCP library!"
    echo ""
    echo "This usually means:"
    echo "1. Your Python version is too old (need 3.10+)"
    echo "2. Your pip version is too old"
    echo "3. Network connectivity issues"
    echo ""
    echo "SOLUTIONS:"
    echo "1. Upgrade to Python 3.12+ from https://www.python.org/downloads/"
    echo "2. Upgrade pip: $PYTHON_CMD -m pip install --upgrade pip"
    echo "3. Try installing MCP manually: $PYTHON_CMD -m pip install mcp"
    echo ""
    echo "Then re-run this installer."
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create or update Claude Desktop config
echo "⚙️  Configuring Claude Desktop..."

# Create config directory if it doesn't exist
mkdir -p "$(dirname "$CONFIG_PATH")"

# Check if config file exists
if [ -f "$CONFIG_PATH" ]; then
    # Backup existing config
    cp "$CONFIG_PATH" "$CONFIG_PATH.backup.$(date +%s)"
    echo "📋 Backed up existing Claude config"
    
    # Read existing config and add our server
    $PYTHON_CMD << EOF
import json
import os

config_path = "$CONFIG_PATH"
install_dir = "$INSTALL_DIR"

try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except:
    config = {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['covered-call-calculator'] = {
    'command': f'{install_dir}/venv/bin/python',
    'args': [f'{install_dir}/covered_call_server.py'],
    'env': {}
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Updated Claude Desktop configuration")
EOF

else
    # Create new config file
    cat > "$CONFIG_PATH" << EOF
{
  "mcpServers": {
    "covered-call-calculator": {
      "command": "$INSTALL_DIR/venv/bin/python",
      "args": ["$INSTALL_DIR/covered_call_server.py"],
      "env": {}
    }
  }
}
EOF
    echo "✅ Created Claude Desktop configuration"
fi

# Test the installation
echo "🧪 Testing installation..."
if ! "$INSTALL_DIR/venv/bin/python" -c "import mcp; print('MCP imported successfully')" &>/dev/null; then
    echo "❌ Installation test failed!"
    echo "MCP library was installed but cannot be imported."
    echo "This suggests a Python environment issue."
    echo ""
    echo "Try reinstalling Python 3.12+ and running this installer again."
    echo "Need help? Email: jude.hoffner@gmail.com"
    exit 1
fi

echo ""
echo "🎉 Installation Complete!"
echo ""
echo "🔥 NEW FEATURES in v1.1:"
echo "  • Multi-timeframe comparison (weekly vs monthly strategies)"
echo "  • Enhanced UX with better analysis formatting"
echo "  • Improved professional reports"
echo ""
echo "Next steps:"
echo "1. 🔄 Restart Claude Desktop completely (Cmd+Q then reopen on Mac)"
echo "2. 🧪 Test: 'Calculate covered call for AAPL at \$200 with 25% IV and 14 days'"
echo "3. ⭐ Try new feature: 'Compare timeframes for Tesla at \$250 with 40% IV'"
echo "4. 📄 Generate reports: 'Create professional report for Microsoft covered calls'"
echo ""
echo "🚀 Happy trading!"
echo ""

# Create uninstall script
cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
echo "Removing Covered Call Calculator..."

# Remove from Claude config
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/claude/claude_desktop_config.json"
fi

if [ -f "$CONFIG_PATH" ]; then
    python3 << EOL
import json
try:
    with open("$CONFIG_PATH", 'r') as f:
        config = json.load(f)
    if 'mcpServers' in config and 'covered-call-calculator' in config['mcpServers']:
        del config['mcpServers']['covered-call-calculator']
        with open("$CONFIG_PATH", 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Removed from Claude Desktop config")
except:
    print("⚠️  Could not update Claude config")
EOL
fi

# Remove installation directory
rm -rf "$HOME/.covered_call_calculator"
echo "✅ Uninstalled successfully"
echo "Please restart Claude Desktop"
EOF

chmod +x "$INSTALL_DIR/uninstall.sh"
echo "📝 To uninstall later, run: $INSTALL_DIR/uninstall.sh"
echo ""
echo "💡 Updates: When we release new features, just re-run the install command!"