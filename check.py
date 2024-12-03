import requests

# Step 1: Arbitrage Calculation (same as your current script)
# Fetch data from Odos API
odos_quote_url = "https://api.odos.xyz/sor/quote/v2"
BASE_CHAIN_ID = 8453
BASE_USDC_ADDRESS = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
BASE_AIXBT_ADDRESS = "0x4F9Fd6Be4a90f2620860d680c0d4d5Fb53d1A825"
USER_ADDRESS = "0x1234567890ABCDEF1234567890ABCDEF12345678"
USDC_AMOUNT = "10000000000"

odos_payload = {
    "chainId": BASE_CHAIN_ID,
    "inputTokens": [
        {"tokenAddress": BASE_USDC_ADDRESS, "amount": USDC_AMOUNT}
    ],
    "outputTokens": [
        {"tokenAddress": BASE_AIXBT_ADDRESS, "proportion": 1.0}
    ],
    "slippageLimitPercent": 0.3,
    "userAddr": USER_ADDRESS,
    "referralCode": 0,
    "disableRFQs": True,
    "compact": True,
}

odos_response = requests.post(
    odos_quote_url, headers={"Content-Type": "application/json"}, json=odos_payload
)
odos_quote = odos_response.json()
aixbt_amount_raw = int(odos_quote["outAmounts"][0])
aixbt_amount_human = aixbt_amount_raw / 10**18

# Fetch data from Jupiter API
jupiter_quote_url = "https://quote-api.jup.ag/v6/quote"
SOLANA_AIXBT_MINT = "14zP2ToQ79XWvc7FQpm4bRnp9d6Mp1rFfsUW3gpLcRX"
SOLANA_USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
AIXBT_DECIMALS = 18
AIXBT_AMOUNT = aixbt_amount_raw // (10**(AIXBT_DECIMALS - 8))

jupiter_params = {
    "inputMint": SOLANA_AIXBT_MINT,
    "outputMint": SOLANA_USDC_MINT,
    "amount": str(AIXBT_AMOUNT),
    "slippageBps": 50,
    "swapMode": "ExactIn",
}
jupiter_response = requests.get(jupiter_quote_url, params=jupiter_params)
jupiter_quote = jupiter_response.json()
usdc_amount = int(jupiter_quote["outAmount"])
usdc_amount_human = usdc_amount / 10**6

# Step 2: Generate HTML File
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Arbitrage Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; }}
        h1 {{ color: #333; }}
        p {{ font-size: 1.2em; }}
    </style>
</head>
<body>
    <h1>Arbitrage Results</h1>
    <p><strong>Input USDC:</strong> {int(USDC_AMOUNT) / 10**6} USDC</p>
    <p><strong>AIXBT Amount:</strong> {aixbt_amount_human:.1f} AIXBT</p>
    <p><strong>Output USDC:</strong> {usdc_amount_human:.1f} USDC</p>
</body>
</html>
"""

# Save the HTML file
with open("index.html", "w") as file:
    file.write(html_content)
