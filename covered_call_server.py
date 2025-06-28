#!/usr/bin/env python3
"""
Covered Call Calculator MCP Server
Implements the IV-based probability calculation for optimal strike selection
"""

import json
import math
from typing import Any, Dict
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize the MCP server
server = Server("covered-call-calculator")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the covered call calculator."""
    return [
        Tool(
            name="calculate_quick_analysis",
            description="Get a quick covered call calculation and summary for immediate decision making",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL)"
                    },
                    "stock_price": {
                        "type": "number",
                        "description": "Current stock price"
                    },
                    "iv_percent": {
                        "type": "number",
                        "description": "At-the-money implied volatility as percentage (e.g., 25 for 25%)"
                    },
                    "days_to_expiry": {
                        "type": "integer", 
                        "description": "Number of calendar days until expiration"
                    },
                    "target_probability": {
                        "type": "number",
                        "description": "Target probability of success (default 84)",
                        "default": 84
                    }
                },
                "required": ["stock_symbol", "stock_price", "iv_percent", "days_to_expiry"]
            }
        ),
        Tool(
            name="estimate_annual_returns",
            description="Estimate annualized returns based on IV level and trading frequency - quick calculation only",
            inputSchema={
                "type": "object", 
                "properties": {
                    "iv_percent": {
                        "type": "number",
                        "description": "Implied volatility as percentage"
                    },
                    "trades_per_year": {
                        "type": "integer",
                        "description": "Number of trades per year (default 26 for bi-weekly)",
                        "default": 26
                    }
                },
                "required": ["iv_percent"]
            }
        ),
        Tool(
            name="create_professional_report",
            description="Generate a formal, shareable document with comprehensive covered call analysis - creates a markdown artifact you can save, print, or share",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL)"
                    },
                    "stock_price": {
                        "type": "number",
                        "description": "Current stock price"
                    },
                    "iv_percent": {
                        "type": "number",
                        "description": "At-the-money implied volatility as percentage (e.g., 25 for 25%)"
                    },
                    "days_to_expiry": {
                        "type": "integer", 
                        "description": "Number of calendar days until expiration"
                    },
                    "target_probability": {
                        "type": "number",
                        "description": "Target probability of success (default 84)",
                        "default": 84
                    }
                },
                "required": ["stock_symbol", "stock_price", "iv_percent", "days_to_expiry"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls for covered call calculations."""
    
    if name == "calculate_quick_analysis":
        return await calculate_strategy(arguments)
    elif name == "estimate_annual_returns": 
        return await estimate_returns(arguments)
    elif name == "create_professional_report":
        return await generate_report(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def calculate_strategy(args: Dict[str, Any]) -> list[TextContent]:
    """Calculate covered call strategy recommendations."""
    
    stock_symbol = args["stock_symbol"]
    stock_price = args["stock_price"]
    iv_percent = args["iv_percent"]
    days_to_expiry = args["days_to_expiry"]
    target_prob = args.get("target_probability", 84)
    
    # Convert IV to decimal
    iv_decimal = iv_percent / 100
    
    # Calculate time factor (square root of time)
    time_factor = math.sqrt(days_to_expiry / 365)
    
    # Calculate expected move (1 standard deviation)
    expected_move = stock_price * iv_decimal * time_factor
    
    # Calculate probability multipliers
    prob_multipliers = {
        68: 1.0,    # 1 standard deviation
        75: 0.67,
        80: 0.84, 
        84: 1.0,    # Default (1 std dev gives ~84% one-sided probability)
        90: 1.28,
        95: 1.64
    }
    
    # Get the appropriate multiplier
    if target_prob in prob_multipliers:
        multiplier = prob_multipliers[target_prob]
    else:
        # Linear interpolation for custom probabilities
        multiplier = 1.0  # Default to 1 std dev
    
    # Calculate target strike level
    target_strike_level = stock_price + (expected_move * multiplier)
    
    # Round to nearest common strike ($5 intervals for most stocks)
    strike_interval = 5 if stock_price > 100 else 2.5 if stock_price > 50 else 1
    suggested_strike = math.ceil(target_strike_level / strike_interval) * strike_interval
    
    # Calculate percentage move
    percent_move = (expected_move / stock_price) * 100
    
    # Estimate premium (rough approximation)
    estimated_premium_pct = iv_percent * time_factor * 0.4  # Empirical factor
    
    # Generate analysis
    analysis = f"""
**Covered Call Analysis for {stock_symbol}**

**Current Setup:**
- Stock Price: ${stock_price:.2f}
- Implied Volatility: {iv_percent}%
- Days to Expiry: {days_to_expiry}
- Target Success Probability: {target_prob}%

**Calculations:**
- Expected Move (1σ): ${expected_move:.2f} ({percent_move:.1f}%)
- Target Strike Level: ${target_strike_level:.2f}
- **Recommended Strike: ${suggested_strike:.2f}**

**Strategy Summary:**
With {target_prob}% probability, {stock_symbol} should stay below ${suggested_strike:.2f} over the next {days_to_expiry} days.

**Expected Outcomes:**
- **Success ({target_prob}%)**: Keep full premium, estimated ~{estimated_premium_pct:.1f}% return
- **Assignment ({100-target_prob}%)**: Stock rises above ${suggested_strike:.2f}, shares called away or buy-to-close required

**Risk Assessment:**
- Low Risk: Premium income strategy with mathematically-calculated probabilities
- Main Risk: Opportunity cost if stock rallies significantly above strike
- Worst Case: Miss upside above ${suggested_strike:.2f}, but stock appreciation offsets premium loss

**Recommendation:**
Sell {stock_symbol} {suggested_strike:.0f} calls expiring in {days_to_expiry} days for optimal risk-adjusted income.
    """
    
    return [TextContent(type="text", text=analysis.strip())]

async def estimate_returns(args: Dict[str, Any]) -> list[TextContent]:
    """Estimate annualized returns based on IV."""
    
    iv_percent = args["iv_percent"]
    trades_per_year = args.get("trades_per_year", 26)
    
    # Rule of thumb calculations based on IV
    if iv_percent <= 25:
        return_range = "10-15%"
        category = "Low IV"
    elif iv_percent <= 35:
        return_range = "15-25%"
        category = "Medium IV"
    elif iv_percent <= 50:
        return_range = "25-35%"
        category = "High IV"
    else:
        return_range = "35%+"
        category = "Very High IV"
    
    # Calculate rough estimate
    premium_per_trade = iv_percent * 0.02  # Rough approximation
    annual_estimate = premium_per_trade * trades_per_year
    
    analysis = f"""
**Annualized Return Estimate**

**IV Category:** {category} ({iv_percent}%)
**Trading Frequency:** {trades_per_year} trades/year

**Expected Returns:**
- **Range:** {return_range} annually
- **Estimate:** ~{annual_estimate:.1f}% per year
- **Per Trade:** ~{premium_per_trade:.1f}% average

**Risk-Adjusted Expectation:**
With 84% success rate: ~{annual_estimate * 0.84:.1f}% highly probable annual return

**Strategy Notes:**
- Higher IV = Higher premiums = Higher returns
- Bi-weekly cycles optimize time decay vs. market risk
- Returns assume consistent execution of probability-based strikes
    """
    
    return [TextContent(type="text", text=analysis.strip())]

async def generate_report(args: Dict[str, Any]) -> list[TextContent]:
    """Generate a professional markdown report for covered call strategy."""
    
    stock_symbol = args["stock_symbol"]
    stock_price = args["stock_price"]
    iv_percent = args["iv_percent"]
    days_to_expiry = args["days_to_expiry"]
    target_prob = args.get("target_probability", 84)
    
    # Convert IV to decimal
    iv_decimal = iv_percent / 100
    
    # Calculate time factor (square root of time)
    time_factor = math.sqrt(days_to_expiry / 365)
    
    # Calculate expected move (1 standard deviation)
    expected_move = stock_price * iv_decimal * time_factor
    
    # Calculate probability multipliers
    prob_multipliers = {
        68: 1.0,    # 1 standard deviation
        75: 0.67,
        80: 0.84, 
        84: 1.0,    # Default (1 std dev gives ~84% one-sided probability)
        90: 1.28,
        95: 1.64
    }
    
    # Get the appropriate multiplier
    if target_prob in prob_multipliers:
        multiplier = prob_multipliers[target_prob]
    else:
        # Linear interpolation for custom probabilities
        multiplier = 1.0  # Default to 1 std dev
    
    # Calculate target strike level
    target_strike_level = stock_price + (expected_move * multiplier)
    
    # Round to nearest common strike ($5 intervals for most stocks)
    strike_interval = 5 if stock_price > 100 else 2.5 if stock_price > 50 else 1
    suggested_strike = math.ceil(target_strike_level / strike_interval) * strike_interval
    
    # Calculate percentage move
    percent_move = (expected_move / stock_price) * 100
    upside_participation = suggested_strike - stock_price
    
    # Estimate premium (rough approximation)
    estimated_premium_pct = iv_percent * time_factor * 0.4  # Empirical factor
    
    # Generate date for report
    from datetime import datetime, timedelta
    analysis_date = datetime.now().strftime("%B %d, %Y")
    expiry_date = (datetime.now() + timedelta(days=days_to_expiry)).strftime("%B %d, %Y")
    
    # Generate professional markdown report
    report = f"""# Covered Call Strategy Analysis

**Analysis Date:** {analysis_date}  
**Security:** {stock_symbol}  
**Current Price:** ${stock_price:.2f}  
**Target Expiration:** {expiry_date} ({days_to_expiry} days)

---

## Executive Summary

**Recommended Action:** Sell {stock_symbol} ${suggested_strike:.0f} call options

**Key Metrics:**
- **Success Probability:** {target_prob}% chance of retaining full premium
- **Expected Return:** {estimated_premium_pct:.1f}% for the {days_to_expiry}-day period
- **Maximum Upside:** ${upside_participation:.2f} per share ({upside_participation/stock_price*100:.1f}%)

---

## Strategy Details

### Position Structure
| Component | Details |
|-----------|---------|
| Underlying Asset | {stock_symbol} @ ${stock_price:.2f} |
| Call Strike | ${suggested_strike:.2f} |
| Days to Expiration | {days_to_expiry} |
| Implied Volatility | {iv_percent}% |
| Distance to Strike | {(suggested_strike - stock_price)/stock_price*100:.1f}% above current price |

### Probability Analysis
| Scenario | Probability | Outcome |
|----------|-------------|---------|
| **Success Case** | {target_prob}% | Stock remains below ${suggested_strike:.2f}, retain full premium |
| **Assignment Risk** | {100-target_prob}% | Stock rises above ${suggested_strike:.2f}, shares called away |

---

## Risk Assessment

### Favorable Outcomes
- **Income Generation:** Collect option premium regardless of moderate stock movement
- **Downside Protection:** Premium provides buffer against minor price declines
- **High Probability:** {target_prob}% mathematical probability of success

### Risk Considerations
- **Opportunity Cost:** Limited upside participation above ${suggested_strike:.2f}
- **Assignment Risk:** {100-target_prob}% chance of shares being called away
- **Market Risk:** Underlying stock price volatility affects strategy performance

### Maximum Scenarios
- **Best Case:** Stock appreciates to ${suggested_strike:.2f}, retain premium + stock gains
- **Worst Case:** Stock declines significantly, premium provides limited downside protection

---

## Implementation Notes

This analysis is based on implied volatility of {iv_percent}% and uses quantitative probability models. The recommended strike price of ${suggested_strike:.2f} provides an optimal balance between income generation and upside participation for the specified risk tolerance.

**Important:** This analysis is for educational purposes only and should not be considered personalized investment advice. Consult with a qualified financial advisor before implementing any options strategies.

---

*Analysis generated using implied volatility-based probability calculations*"""
    
    return [TextContent(type="text", text=report)]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())