from web3 import Web3

RPC_URL = "http://localhost:8545"

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise SystemExit("Cannot connect to Geth Node 1")

tx_hash = input("Enter transaction hash: ").strip()

if not tx_hash:
    raise SystemExit("Transaction hash is required.")

try:
    tx = web3.eth.get_transaction(tx_hash)
except Exception as error:
    raise SystemExit(f"Cannot get transaction: {error}")

print()
print("Transaction Information")
print("=" * 60)

for key, value in tx.items():
    if isinstance(value, bytes):
        value = value.hex()

    print(f"{key}: {value}")
