from web3 import Web3

RPC_URL = "http://localhost:8545"

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise SystemExit("Cannot connect to Geth Node 1")

accounts = web3.eth.accounts

if not accounts:
    raise SystemExit("No accounts found in Node 1.")

# Use Geth coinbase if available.
try:
    sender = web3.eth.coinbase
except Exception:
    sender = accounts[0]

if not sender or int(sender, 16) == 0:
    sender = accounts[0]

balance_wei = web3.eth.get_balance(sender)
balance_eth = web3.from_wei(balance_wei, "ether")

print("Node 1")
print("=" * 60)
print("Sender :", sender)
print("Balance:", balance_eth, "ETH")
print()

to_address = input("Transfer to: ").strip()
amount = input("Amount (ETH): ").strip()
password = input("Passphrase: ")

if not web3.is_address(to_address):
    raise SystemExit("Invalid destination address.")

try:
    amount_wei = web3.to_wei(amount, "ether")
except Exception:
    raise SystemExit("Invalid ETH amount.")

try:
    # Geth personal_sendTransaction:
    # signs the transaction using the account password.
    tx_hash = web3.provider.make_request(
        "personal_sendTransaction",
        [
            {
                "from": sender,
                "to": Web3.to_checksum_address(to_address),
                "value": hex(amount_wei),
            },
            password,
        ],
    )

    if "error" in tx_hash:
        raise RuntimeError(tx_hash["error"]["message"])

    tx_hash = tx_hash["result"]

    print()
    print("Transaction Hash:", tx_hash)

except Exception as error:
    raise SystemExit(f"Transaction failed: {error}")
