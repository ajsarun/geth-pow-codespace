from web3 import Web3

RPC_URL = "http://localhost:8545"

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise SystemExit("Cannot connect to Geth Node 1")

accounts = web3.eth.accounts

if not accounts:
    raise SystemExit("No accounts found in Node 1.")

print("Accounts:")
for i, account in enumerate(accounts):
    print(f"{i}: {account}")

print()

try:
    index = int(input("Enter account index: "))
except ValueError:
    raise SystemExit("Account index must be an integer.")

if index < 0 or index >= len(accounts):
    raise SystemExit(
        f"Account index out of range. Valid range: 0-{len(accounts)-1}"
    )

account = accounts[index]
balance_wei = web3.eth.get_balance(account)
balance_eth = web3.from_wei(balance_wei, "ether")

print()
print("Address:", account)
print("Balance:", balance_eth, "ETH")
