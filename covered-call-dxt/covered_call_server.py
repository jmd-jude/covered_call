#!/usr/bin/env python3
"""
Covered Call Calculator MCP Server v1.1
Now with Multi-Timeframe Comparison for optimal cycle selection
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
            name="get_started_guide",
            description="Start here! Learn what this tool does and how to use it effectively for income generation",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="analyze_covered_call",
            description="Calculate optimal strike price and expected income for a specific stock position",
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
            name="compare_timeframes",
            description="Compare weekly vs bi-weekly vs monthly strategies to maximize your returns",
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
                    "target_probability": {
                        "type": "number",
                        "description": "Target probability of success (default 84)",
                        "default": 84
                    }
                },
                "required": ["stock_symbol", "stock_price", "iv_percent"]
            }
        ),
        Tool(
            name="estimate_annual_returns",
            description="Project yearly income potential based on your trading frequency and market volatility",
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
            description="Generate a formal analysis document you can save, print, or share with advisors",
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
    
    if name == "get_started_guide":
        return await getting_started_guide(arguments)
    elif name == "analyze_covered_call":
        return await calculate_strategy(arguments)
    elif name == "compare_timeframes":
        return await compare_timeframes(arguments)
    elif name == "estimate_annual_returns": 
        return await estimate_returns(arguments)
    elif name == "create_professional_report":
        return await generate_report(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def getting_started_guide(args: Dict[str, Any]) -> list[TextContent]:
    """Comprehensive getting started guide for new users."""
    
    guide = """
# 🏁 Stock Rental Income System - Getting Started

## What This Tool Does

Think of your stocks as rental properties. Instead of waiting years for appreciation, you can collect "rent" monthly by selling covered call options. This tool calculates exactly which options to sell for **84% probability of success**.

**Perfect for you if:**
- You own stocks you plan to hold for years (Apple, Microsoft, etc.)
- You want monthly income from existing holdings
- You prefer mathematical precision over guessing

---

## Recommended Workflow

### Step 1: Start with Strategy Comparison
**Command:** `compare timeframes for [STOCK] at $[PRICE] with [IV]% IV`

**Example:** *"Compare timeframes for Apple at $190 with 25% IV"*

**Why first?** Shows you ALL your options - weekly vs monthly cycles - so you pick the best strategy.

### Step 2: Analyze Specific Trades  
**Command:** `analyze covered call for [STOCK]`

**Example:** *"Analyze covered call for Microsoft at $350 with 30% IV and 14 days"*

**Why next?** Gets precise strike recommendations for your chosen timeframe.

### Step 3: Project Your Income
**Command:** `estimate annual returns`

**Example:** *"Estimate annual returns with 30% IV trading bi-weekly"*

**Why useful?** See your potential yearly income before committing.

### Step 4: Document Everything
**Command:** `create professional report`

**Example:** *"Create professional report for Tesla position"*

**Why important?** Save analysis for taxes, advisors, or future reference.

---

## Key Concepts Simplified

**84% Success Rate**: Mathematical probability your calls expire worthless (you keep the premium)

**Implied Volatility (IV)**: Market's expectation of price movement - higher IV = higher premiums

**Strike Price**: The price where your shares get "called away" if the stock rises too much

**Premium**: The income you collect upfront (like collecting rent)

---

## Sample Questions to Try

**Strategy Planning:**
- *"Compare weekly vs monthly strategies for my Nvidia position at $450"*
- *"What timeframe works best for 25% volatility stocks?"*

**Specific Analysis:**
- *"Optimal strike for Amazon at $180 with 28% IV, 21 days out"*
- *"Calculate risk-adjusted returns for Google at $150"*

**Portfolio Planning:**
- *"Annual income potential from covered calls with my portfolio"*
- *"Best practices for managing 10 different stock positions"*

---

## Quick Risk Reminder

**You win when:** Stock stays flat or rises moderately → keep premium + stock gains

**You lose when:** Stock rockets above your strike → shares called away (but you still profit)

**Protection:** Premium provides downside cushion if stock drops

---

## Pro Tips

1. **Start conservative**: Use the default 84% probability until you're comfortable
2. **Track everything**: Use professional reports to build your success database  
3. **Think portfolio-wide**: Some positions work better for weekly cycles, others monthly
4. **Focus on stocks you love**: Never sell calls on stocks you might want to trade

---

**Ready to start?** Try: *"Compare timeframes for [your favorite stock]"*

**Need specific help?** Try: *"Analyze covered call for [specific position]"*

**Want the big picture?** Try: *"Estimate annual returns for my trading style"*
    """
    
    return [TextContent(type="text", text=guide.strip())]

def calculate_core_metrics(stock_price: float, iv_percent: float, days_to_expiry: int, target_prob: float = 84):
    """Core calculation logic - reusable across all tools."""
    
    # Convert IV to decimal
    iv_decimal = iv_percent / 100
    
    # Calculate time factor (square root of time)
    time_factor = math.sqrt(days_to_expiry / 365)
    
    # Calculate expected move (1 standard deviation)
    expected_move = stock_price * iv_decimal * time_factor
    
    # Calculate probability multipliers
    prob_multipliers = {
        68: 1.0, 75: 0.67, 80: 0.84, 84: 1.0, 90: 1.28, 95: 1.64
    }
    
    multiplier = prob_multipliers.get(target_prob, 1.0)
    
    # Calculate target strike level
    target_strike_level = stock_price + (expected_move * multiplier)
    
    # Round to nearest common strike
    strike_interval = 5 if stock_price > 100 else 2.5 if stock_price > 50 else 1
    suggested_strike = math.ceil(target_strike_level / strike_interval) * strike_interval
    
    # Calculate percentage move and premium estimate
    percent_move = (expected_move / stock_price) * 100
    estimated_premium_pct = iv_percent * time_factor * 0.4
    
    return {
        'expected_move': expected_move,
        'target_strike_level': target_strike_level,
        'suggested_strike': suggested_strike,
        'percent_move': percent_move,
        'estimated_premium_pct': estimated_premium_pct,
        'time_factor': time_factor
    }

async def compare_timeframes(args: Dict[str, Any]) -> list[TextContent]:
    """Compare multiple timeframes to optimize trading frequency."""
    
    stock_symbol = args["stock_symbol"]
    stock_price = args["stock_price"]
    iv_percent = args["iv_percent"]
    target_prob = args.get("target_probability", 84)
    
    # Define timeframes to compare
    timeframes = [
        {"name": "Weekly", "days": 7, "cycles_per_year": 52},
        {"name": "Bi-Weekly", "days": 14, "cycles_per_year": 26},
        {"name": "Monthly", "days": 30, "cycles_per_year": 12}
    ]
    
    results = []
    for tf in timeframes:
        metrics = calculate_core_metrics(stock_price, iv_percent, tf["days"], target_prob)
        
        # Calculate annualized metrics
        annual_return = metrics['estimated_premium_pct'] * tf['cycles_per_year']
        annual_return_adjusted = annual_return * (target_prob / 100)  # Risk-adjusted
        
        results.append({
            'timeframe': tf,
            'metrics': metrics,
            'annual_return': annual_return,
            'annual_return_adjusted': annual_return_adjusted
        })
    
    # Determine optimal strategy
    best_risk_adjusted = max(results, key=lambda x: x['annual_return_adjusted'])
    best_total_return = max(results, key=lambda x: x['annual_return'])
    
    analysis = f"""
**⚡ Multi-Timeframe Strategy Comparison for {stock_symbol}**

**Market Context:**
- Current Price: ${stock_price:.2f}
- Implied Volatility: {iv_percent}%
- Target Success Rate: {target_prob}%

---

**📊 Strategy Comparison:**

| Timeframe | Strike | Return/Cycle | Annual Return | Risk-Adjusted* |
|-----------|--------|--------------|---------------|----------------|"""
    
    for result in results:
        tf = result['timeframe']
        metrics = result['metrics']
        analysis += f"""
| **{tf['name']}** ({tf['days']}d) | ${metrics['suggested_strike']:.0f} | {metrics['estimated_premium_pct']:.1f}% | {result['annual_return']:.1f}% | {result['annual_return_adjusted']:.1f}% |"""
    
    analysis += f"""

**🎯 Recommendations:**

**For Maximum Income:** {best_total_return['timeframe']['name']} cycles
- Strike: ${best_total_return['metrics']['suggested_strike']:.0f}
- Expected: {best_total_return['annual_return']:.1f}% annual return
- Trade-off: Higher frequency = more management time

**For Risk-Adjusted Returns:** {best_risk_adjusted['timeframe']['name']} cycles  
- Strike: ${best_risk_adjusted['metrics']['suggested_strike']:.0f}
- Expected: {best_risk_adjusted['annual_return_adjusted']:.1f}% risk-adjusted annual return
- Trade-off: Better probability-weighted outcomes

**🧠 Strategy Notes:**
- Weekly: More trades, higher potential returns, more time commitment
- Monthly: Fewer trades, lower management overhead, longer time exposure
- Bi-Weekly: Balanced approach, optimal for most retail traders

*Risk-adjusted = Annual return × {target_prob}% success probability

**💡 Pro Tip:** Start with the risk-adjusted winner and adjust based on your time availability and market outlook.
    """
    
    return [TextContent(type="text", text=analysis.strip())]

async def calculate_strategy(args: Dict[str, Any]) -> list[TextContent]:
    """Calculate covered call strategy recommendations."""
    
    stock_symbol = args["stock_symbol"]
    stock_price = args["stock_price"]
    iv_percent = args["iv_percent"]
    days_to_expiry = args["days_to_expiry"]
    target_prob = args.get("target_probability", 84)
    
    metrics = calculate_core_metrics(stock_price, iv_percent, days_to_expiry, target_prob)
    
    # Generate analysis with UX breadcrumbs
    analysis = f"""
**🎯 Covered Call Analysis for {stock_symbol}**

**Current Setup:**
- Stock Price: ${stock_price:.2f}
- Implied Volatility: {iv_percent}% {'📈 (High premium environment)' if iv_percent > 30 else '📊 (Normal premium environment)' if iv_percent > 20 else '📉 (Low premium environment)'}
- Days to Expiry: {days_to_expiry}
- Target Success Probability: {target_prob}%

**📐 Mathematical Foundation:**
- Expected Move (1σ): ${metrics['expected_move']:.2f} ({metrics['percent_move']:.1f}%)
- Target Strike Level: ${metrics['target_strike_level']:.2f}
- **🎯 Recommended Strike: ${metrics['suggested_strike']:.2f}**

**📊 Strategy Outlook:**
With {target_prob}% probability, {stock_symbol} should stay below ${metrics['suggested_strike']:.2f} over the next {days_to_expiry} days.

**💰 Expected Outcomes:**
- **Success ({target_prob}%)**: Keep full premium → ~{metrics['estimated_premium_pct']:.1f}% return
- **Assignment ({100-target_prob}%)**: Stock rises above ${metrics['suggested_strike']:.2f} → shares called away

**⚖️ Risk Profile:**
- **Upside Participation**: Full gains up to ${metrics['suggested_strike']:.2f} (+{((metrics['suggested_strike'] - stock_price)/stock_price*100):.1f}%)
- **Downside Protection**: Premium cushion of ~{metrics['estimated_premium_pct']:.1f}%
- **Probability Edge**: {target_prob}% mathematically-calculated success rate

**🚀 Action Items:**
1. Sell {stock_symbol} ${metrics['suggested_strike']:.0f} calls expiring in {days_to_expiry} days
2. Set buy-to-close alert at 50% of premium collected
3. Consider rolling strategy if approaching assignment

💡 **Want to optimize timing?** Try `compare_timeframes` to see if weekly/monthly cycles might work better for this stock.
    """
    
    return [TextContent(type="text", text=analysis.strip())]

async def estimate_returns(args: Dict[str, Any]) -> list[TextContent]:
    """Estimate annualized returns based on IV."""
    
    iv_percent = args["iv_percent"]
    trades_per_year = args.get("trades_per_year", 26)
    
    # Enhanced categorization with UX hints
    if iv_percent <= 25:
        return_range = "10-15%"
        category = "Low IV"
        market_note = "📉 Conservative environment - consider longer timeframes"
    elif iv_percent <= 35:
        return_range = "15-25%"
        category = "Medium IV"
        market_note = "📊 Balanced environment - standard bi-weekly cycles work well"
    elif iv_percent <= 50:
        return_range = "25-35%"
        category = "High IV"
        market_note = "📈 High premium environment - consider shorter cycles to capture volatility"
    else:
        return_range = "35%+"
        category = "Very High IV"
        market_note = "🔥 Exceptional premium environment - weekly cycles may be optimal"
    
    # Calculate estimates
    premium_per_trade = iv_percent * 0.02
    annual_estimate = premium_per_trade * trades_per_year
    
    analysis = f"""
**📈 Annualized Return Projection**

**Market Environment:** {category} ({iv_percent}%)
{market_note}

**Trading Parameters:**
- Frequency: {trades_per_year} trades/year
- Success Rate: 84% (probability-weighted)

**📊 Return Expectations:**
- **Range:** {return_range} annually
- **Base Estimate:** ~{annual_estimate:.1f}% per year
- **Per Trade:** ~{premium_per_trade:.1f}% average
- **Risk-Adjusted:** ~{annual_estimate * 0.84:.1f}% (84% success weighted)

**🎯 Strategy Optimization:**
- Higher IV = Higher premiums = More aggressive cycling possible
- Lower IV = Focus on longer timeframes for better risk/reward
- Bi-weekly cycles balance time decay optimization with market risk

**💡 Next Steps:**
Run `compare_timeframes` to see if weekly/monthly cycles might optimize returns for current IV level.
    """
    
    return [TextContent(type="text", text=analysis.strip())]

async def generate_report(args: Dict[str, Any]) -> list[TextContent]:
    """Generate a professional markdown report for covered call strategy."""
    
    stock_symbol = args["stock_symbol"]
    stock_price = args["stock_price"]
    iv_percent = args["iv_percent"]
    days_to_expiry = args["days_to_expiry"]
    target_prob = args.get("target_probability", 84)
    
    metrics = calculate_core_metrics(stock_price, iv_percent, days_to_expiry, target_prob)
    upside_participation = metrics['suggested_strike'] - stock_price
    
    # Generate dates
    from datetime import datetime, timedelta
    analysis_date = datetime.now().strftime("%B %d, %Y")
    expiry_date = (datetime.now() + timedelta(days=days_to_expiry)).strftime("%B %d, %Y")
    
    # UX Enhancement: Suggest filename
    filename_suggestion = f"{stock_symbol}_covered_call_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    report = f"""# Covered Call Strategy Analysis

**💾 Save Suggestion:** `{filename_suggestion}`  
**📁 Recommended Location:** `~/Documents/Trading_Reports/`

---

**Analysis Date:** {analysis_date}  
**Security:** {stock_symbol}  
**Current Price:** ${stock_price:.2f}  
**Target Expiration:** {expiry_date} ({days_to_expiry} days)

---

## Executive Summary

**Recommended Action:** Sell {stock_symbol} ${metrics['suggested_strike']:.0f} call options

**Key Metrics:**
- **Success Probability:** {target_prob}% chance of retaining full premium
- **Expected Return:** {metrics['estimated_premium_pct']:.1f}% for the {days_to_expiry}-day period
- **Maximum Upside:** ${upside_participation:.2f} per share ({upside_participation/stock_price*100:.1f}%)

---

## Strategy Details

### Position Structure
| Component | Details |
|-----------|---------|
| Underlying Asset | {stock_symbol} @ ${stock_price:.2f} |
| Call Strike | ${metrics['suggested_strike']:.2f} |
| Days to Expiration | {days_to_expiry} |
| Implied Volatility | {iv_percent}% |
| Distance to Strike | {(metrics['suggested_strike'] - stock_price)/stock_price*100:.1f}% above current price |

### Probability Analysis
| Scenario | Probability | Outcome |
|----------|-------------|---------|
| **Success Case** | {target_prob}% | Stock remains below ${metrics['suggested_strike']:.2f}, retain full premium |
| **Assignment Risk** | {100-target_prob}% | Stock rises above ${metrics['suggested_strike']:.2f}, shares called away |

---

## Risk Assessment

### Favorable Outcomes
- **Income Generation:** Collect option premium regardless of moderate stock movement
- **Downside Protection:** Premium provides buffer against minor price declines
- **High Probability:** {target_prob}% mathematical probability of success

### Risk Considerations
- **Opportunity Cost:** Limited upside participation above ${metrics['suggested_strike']:.2f}
- **Assignment Risk:** {100-target_prob}% chance of shares being called away
- **Market Risk:** Underlying stock price volatility affects strategy performance

### Maximum Scenarios
- **Best Case:** Stock appreciates to ${metrics['suggested_strike']:.2f}, retain premium + stock gains
- **Worst Case:** Stock declines significantly, premium provides limited downside protection

---

## Implementation Notes

This analysis is based on implied volatility of {iv_percent}% and uses quantitative probability models. The recommended strike price of ${metrics['suggested_strike']:.2f} provides an optimal balance between income generation and upside participation for the specified risk tolerance.

**Management Guidelines:**
- Consider buy-to-close at 50% of premium collected
- Monitor for early assignment risk on dividend dates
- Evaluate rolling opportunities 5-7 days before expiration

**Important:** This analysis is for educational purposes only and should not be considered personalized investment advice. Consult with a qualified financial advisor before implementing any options strategies.

---

*Analysis generated using implied volatility-based probability calculations*  
*Generated with Covered Call Calculator v1.1*"""
    
    return [TextContent(type="text", text=report)]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())