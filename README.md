# Covered Call Calculator for Claude Desktop

A professional options trading tool that integrates with Claude Desktop to provide mathematically precise covered call recommendations using implied volatility calculations.

## Features

- **Probability-Based Strike Selection**: Uses IV and time decay models to recommend optimal strikes
- **84% Success Rate Targeting**: Mathematically calculated probability thresholds
- **Professional Report Generation**: Creates shareable markdown documents with comprehensive analysis
- **Risk Assessment**: Clear breakdown of favorable outcomes and risk considerations
- **Annualized Return Estimates**: Project yearly performance based on trading frequency

## Quick Install

**One-line installation** (Mac/Linux):

```bash
curl -sSL https://raw.githubusercontent.com/jmd-jude/covered_call/main/install.sh | bash
```

Then restart Claude Desktop and ask:
- *"Calculate a covered call strategy for AAPL at $200 with 25% IV and 14 days to expiry"*
- *"Create a professional report for Tesla at $250 with 40% IV and 21 days"*

## What You Get

### Quick Analysis
Ask Claude for immediate covered call calculations:
```
Calculate a covered call strategy for NVDA at $450 with 35% IV and 10 days to expiry
```

Returns probability-based strike recommendations with success rates and expected returns.

### Professional Reports
Generate formal documents for record-keeping or sharing:
```
Create a professional report for Apple at $180 with 28% IV and 21 days
```

Creates downloadable markdown artifacts with:
- Executive summary
- Detailed probability analysis
- Risk assessment
- Implementation notes

### Return Estimates
Project annualized performance:
```
What annual returns can I expect with a 30% IV stock trading bi-weekly?
```

## How It Works

The calculator uses quantitative finance models based on:
- **Implied Volatility**: Market's expectation of future price movement
- **Time Decay**: Mathematical relationship between time and option value
- **Probability Distribution**: Statistical models for strike price selection
- **Risk-Adjusted Returns**: Optimized balance between income and assignment risk

## Requirements

- Mac or Linux
- Python 3.x
- Claude Desktop
- Internet connection for installation

## Manual Installation

If you prefer manual setup:

1. Clone this repository
2. Create virtual environment: `python3 -m venv venv`
3. Install dependencies: `source venv/bin/activate && pip install mcp`
4. Update Claude Desktop config to include the server

## Uninstalling

Run the uninstall script:
```bash
~/.covered_call_calculator/uninstall.sh
```

## Support

This tool is for educational purposes only. Not financial advice. Consult a qualified advisor before implementing any options strategies.

## License

MIT License - Use at your own risk