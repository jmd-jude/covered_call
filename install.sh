#!/bin/bash

# Covered Call Calculator - One-Line Installer
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

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found"

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
curl -sSL https://raw.githubusercontent.com/jmd-jude/covered_call/main/covered_call_server.py -o covered_call_server.py

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --quiet mcp

echo "✅ Dependencies installed"

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
    python3 << EOF
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

echo ""
echo "🎉 Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop completely (Cmd+Q then reopen)"
echo "2. Ask Claude: 'Calculate a covered call strategy for AAPL at \$200 with 25% IV and 14 days to expiry'"
echo "3. Or ask: 'Create a professional report for Tesla at \$250 with 40% IV and 21 days'"
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