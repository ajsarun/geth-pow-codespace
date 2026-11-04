from web3 import Web3

RPC_URL = "http://localhost:8545"

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise SystemExit("Cannot connect to Geth Node 1")

print("Connected to Node 1")
print()

accounts = web3.eth.accounts

print("Accounts:")

if not accounts:
    print("No accounts found.")
else:
    for i, account in enumerate(accounts):
        print(f"{i}: {account}")
