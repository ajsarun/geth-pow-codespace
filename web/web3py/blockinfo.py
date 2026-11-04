from web3 import Web3

RPC_URL = "http://localhost:8545"

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise SystemExit("Cannot connect to Geth Node 1")

try:
    block_number = int(input("Enter block number: "))
except ValueError:
    raise SystemExit("Block number must be an integer.")

try:
    block = web3.eth.get_block(block_number)
except Exception as error:
    raise SystemExit(f"Cannot get block: {error}")

print()
print("Block Information")
print("=" * 60)

for key, value in block.items():
    if isinstance(value, bytes):
        value = value.hex()

    elif isinstance(value, list):
        value = [
            item.hex() if isinstance(item, bytes) else item
            for item in value
        ]

    print(f"{key}: {value}")
