from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__)

RPC_URL = "http://localhost:8545"
web3 = Web3(Web3.HTTPProvider(RPC_URL))


def connected():
    return web3.is_connected()


@app.route("/")
def index():
    return render_template(
        "index.html",
        connected=connected()
    )


@app.route("/accounts")
def accounts():
    error = None
    account_list = []

    try:
        if not connected():
            raise Exception("Cannot connect to Geth Node 1")

        account_list = list(web3.eth.accounts)

    except Exception as e:
        error = str(e)

    return render_template(
        "accounts.html",
        accounts=account_list,
        error=error
    )


@app.route("/balance", methods=["GET", "POST"])
def balance():
    error = None
    result = None
    accounts = []

    try:
        if not connected():
            raise Exception("Cannot connect to Geth Node 1")

        accounts = list(web3.eth.accounts)

        if request.method == "POST":
            index_text = request.form.get("index", "").strip()

            if index_text == "":
                raise Exception("Please enter an account index.")

            index = int(index_text)

            if index < 0 or index >= len(accounts):
                raise Exception(
                    f"Account index out of range. Total accounts: {len(accounts)}"
                )

            address = accounts[index]
            balance_wei = web3.eth.get_balance(address)
            balance_eth = web3.from_wei(balance_wei, "ether")

            result = {
                "index": index,
                "address": address,
                "balance": balance_eth
            }

    except Exception as e:
        error = str(e)

    return render_template(
        "balance.html",
        accounts=accounts,
        result=result,
        error=error
    )


@app.route("/block", methods=["GET", "POST"])
def block():
    error = None
    block_data = None

    try:
        if not connected():
            raise Exception("Cannot connect to Geth Node 1")

        if request.method == "POST":
            block_text = request.form.get("block_number", "").strip()

            if block_text == "":
                raise Exception("Please enter a block number.")

            block_number = int(block_text)

            block_obj = web3.eth.get_block(block_number)

            block_data = []

            for key, value in block_obj.items():
                if isinstance(value, bytes):
                    value = value.hex()
                elif isinstance(value, list):
                    value = [
                        item.hex() if isinstance(item, bytes) else item
                        for item in value
                    ]

                block_data.append((key, value))

    except Exception as e:
        error = str(e)

    return render_template(
        "block.html",
        block_data=block_data,
        error=error
    )


@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    error = None
    tx_data = None

    try:
        if not connected():
            raise Exception("Cannot connect to Geth Node 1")

        if request.method == "POST":
            tx_hash = request.form.get("tx_hash", "").strip()

            if tx_hash == "":
                raise Exception("Please enter a transaction hash.")

            tx = web3.eth.get_transaction(tx_hash)

            tx_data = []

            for key, value in tx.items():
                if isinstance(value, bytes):
                    value = value.hex()

                tx_data.append((key, value))

    except Exception as e:
        error = str(e)

    return render_template(
        "transaction.html",
        tx_data=tx_data,
        error=error
    )


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    error = None
    result = None
    sender = None
    sender_balance = None

    try:
        if not connected():
            raise Exception("Cannot connect to Geth Node 1")

        accounts = list(web3.eth.accounts)

        if not accounts:
            raise Exception("No accounts found in Node 1.")

        try:
            sender = web3.eth.coinbase
        except Exception:
            sender = accounts[0]

        if not sender or int(sender, 16) == 0:
            sender = accounts[0]

        sender_balance = web3.from_wei(
            web3.eth.get_balance(sender),
            "ether"
        )

        if request.method == "POST":
            to_address = request.form.get("to", "").strip()
            amount = request.form.get("amount", "").strip()
            password = request.form.get("password", "")

            if not web3.is_address(to_address):
                raise Exception("Invalid destination address.")

            amount_wei = web3.to_wei(amount, "ether")

            rpc_result = web3.provider.make_request(
                "personal_sendTransaction",
                [
                    {
                        "from": sender,
                        "to": Web3.to_checksum_address(to_address),
                        "value": hex(amount_wei)
                    },
                    password
                ]
            )

            if "error" in rpc_result:
                raise Exception(rpc_result["error"]["message"])

            tx_hash = rpc_result["result"]

            result = {
                "tx_hash": tx_hash
            }

            sender_balance = web3.from_wei(
                web3.eth.get_balance(sender),
                "ether"
            )

    except Exception as e:
        error = str(e)

    return render_template(
        "transfer.html",
        sender=sender,
        sender_balance=sender_balance,
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
