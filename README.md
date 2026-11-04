# Private Ethereum PoW Lab on GitHub Codespaces

A two-node private Ethereum network for teaching accounts, transactions, mining, blocks, JSON-RPC, and peer synchronization. Students can use the Geth console or compare Web3.js, ethers.js, web3.py, and Flask clients against the same blockchain.

The lab uses **Geth v1.10.26**, **Ethash Proof of Work**, chain ID **2026**, and network ID **2026**. This is a legacy educational network; Ethereum Mainnet uses Proof of Stake.

## Repository layout

| Path | Purpose |
| --- | --- |
| `.devcontainer/devcontainer.json` | Codespaces environment with Docker-in-Docker and RPC port forwarding |
| `compose.yaml` | Two Geth services, their ports, and persistent data volumes |
| `geth/genesis.json` | Shared genesis configuration with no pre-funded accounts |
| `geth/start.sh` | Initializes each data directory on first startup and starts Geth |
| `scripts/run-all-nodes.sh` | Starts both nodes and connects them |
| `scripts/connect-nodes.sh` | Adds Node 1 as a peer of Node 2 and prints peer counts |
| `scripts/usenode1.sh` | Opens Node 1's Geth JavaScript console |
| `scripts/usenode2.sh` | Opens Node 2's Geth JavaScript console |
| `scripts/run-web.sh` | Starts the static web server and RPC proxy on port 8000 |
| `web/server.py` | Serves files from the current directory and proxies `POST /rpc` to Node 1 |
| `web/web3js/` | Five Web3.js browser examples |
| `web/etherjs/` | Five ethers.js browser examples; the folder is named `etherjs` |
| `web/web3py/` | Five web3.py command-line examples and `requirements.txt` |
| `web/web3py_flask_client/` | Flask application, `requirements.txt`, and HTML templates |

The Flask templates are `accounts.html`, `balance.html`, `base.html`, `block.html`, `index.html`, `transaction.html`, and `transfer.html`.

## 1. Open a Codespace

On the repository page, select **Code → Codespaces → Create codespace on main** and wait for setup to finish. The setup pulls the Geth Docker image; it does not start the nodes.

Run all commands below from the **repository root**, unless a section explicitly changes directory. Use separate terminals for consoles and servers.

## 2. Start and connect the nodes

```bash
./scripts/run-all-nodes.sh
```

This starts `node1` and `node2`, waits briefly, calls `connect-nodes.sh`, and displays container status.

Check status or inspect startup logs:

```bash
docker compose ps
docker compose logs --tail=50 node1 node2
```

To start services individually instead:

```bash
docker compose up -d node1
docker compose up -d node2
./scripts/connect-nodes.sh
```

Both nodes use `--nodiscover`, so connect them explicitly. If first startup takes longer than the script's short wait, wait for both IPC endpoints to be ready and rerun:

```bash
./scripts/connect-nodes.sh
```

Each node should eventually report one peer. In either Geth console, inspect:

```javascript
net.peerCount
admin.peers
```

## 3. Open the Geth consoles

| Node | Script | Equivalent command |
| --- | --- | --- |
| Node 1 | `./scripts/usenode1.sh` | `docker compose exec node1 geth attach /data/geth.ipc` |
| Node 2 | `./scripts/usenode2.sh` | `docker compose exec node2 geth attach /data/geth.ipc` |

Use a separate terminal for each console. Enter `exit` to leave a console; this does not stop its node.

### Create accounts and mine test ETH

New data volumes contain no accounts. In the **Node 1 console**:

```javascript
eth.accounts
var account1 = personal.newAccount("node1pass")
miner.setEtherbase(account1)
miner.start(1)
```

The password is an example for this private lab. Mining uses one CPU thread. Ethash dataset generation can delay the first block.

In the **Node 2 console**:

```javascript
var account2 = personal.newAccount("node2pass")
account2
```

Copy the address printed for `account2` for later transfers. Variables belong to their individual console sessions; `account2` is not automatically available in Node 1's console.

On Node 1, check progress and balance:

```javascript
eth.mining
eth.blockNumber
eth.coinbase
web3.fromWei(eth.getBalance(eth.accounts[0]), "ether")
eth.getBlock("latest")
txpool.status
```

On Node 2, check `eth.blockNumber` to observe synchronization.

Keep mining while submitting transactions so they can be included in blocks. Stop mining when finished:

```javascript
miner.stop()
```

Accounts and private keys are local to each node. Connecting the nodes shares blockchain data, but does not copy keystores: Node 1's `eth.accounts` will not list an account created only on Node 2.

## 4. Endpoints and client choices

These endpoints are accessible from processes **inside the Codespace**:

| Node | HTTP JSON-RPC | WebSocket |
| --- | --- | --- |
| Node 1 | `http://localhost:8545` | `ws://localhost:8546` |
| Node 2 | `http://localhost:9545` | `ws://localhost:9546` |

Both containers listen internally on 8545/8546; Docker maps Node 2 to host ports 9545/9546.

```bash
curl -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:8545
```

The returned block number is hexadecimal.

| Client | Location | How to run |
| --- | --- | --- |
| Web3.js 4.16.0 | `web/web3js/` | Start `./scripts/run-web.sh`; open `/web3js/` on port 8000 |
| ethers.js 6.7.0 | `web/etherjs/` | Use the same server; open `/etherjs/` on port 8000 |
| web3.py 7.x CLI | `web/web3py/` | Install Python dependencies and run a Python script |
| Flask + web3.py | `web/web3py_flask_client/` | Install dependencies and run `app.py`; open port 8000 |

All clients target **Node 1** by default.

## 5. Run Web3.js and ethers.js browser clients

From the repository root:

```bash
./scripts/run-web.sh
```

Equivalent commands:

```bash
cd web
python3 server.py
```

Leave this terminal running. In Codespaces, open the **PORTS** tab and open port **8000** in the browser. If it is not listed, select **Forward a Port** and enter `8000`. Keep its visibility **Private**.

The forwarded address resembles `https://<codespace-name>-8000.app.github.dev/`. The root displays a directory listing; open `web3js/` or `etherjs/`.

Append one of these paths to that address:

| Example | Web3.js path | ethers.js path |
| --- | --- | --- |
| List Node 1 accounts | `/web3js/listaccounts.html` | `/etherjs/listaccounts.html` |
| Balance by account index | `/web3js/showbalancebyindex.html` | `/etherjs/showbalancebyindex.html` |
| Block information | `/web3js/blockinfo.html` | `/etherjs/blockinfo.html` |
| Transaction information | `/web3js/transactioninfo.html` | `/etherjs/transactioninfo.html` |
| Transfer ETH | `/web3js/transfer.html` | `/etherjs/transfer.html` |

**Existing filename detail:** the ethers.js block page is currently named `ิblockinfo.html`, with a leading Thai character (U+0E34). Use the encoded URL above or click the file in the `/etherjs/` directory listing. `/etherjs/blockinfo.html` will return 404 with the current filename.

Browser clients send requests to `window.location.origin + "/rpc"`. The server forwards them to `http://localhost:8545`. This avoids treating the browser's `localhost` as the Codespace and keeps requests on the same HTTPS origin.

Use this server rather than opening the HTML files directly or using a static-only server: the clients need its `POST /rpc` handler. The JavaScript libraries load from jsDelivr, so the browser needs internet access. No npm install or MetaMask setup is required.

### Transfer prerequisites

1. Create an account on Node 1.
2. Set that account as Node 1's etherbase and mine enough ETH for the amount plus fees.
3. Open a transfer page and enter the recipient address, amount in ETH, and sender's password.
4. Keep Node 1 mining until the transaction is included in a block.

The JavaScript transfer pages use Node 1's coinbase account. Web3.js uses `personal_sendTransaction`; ethers.js unlocks the account for 60 seconds and sends through a signer. The ethers.js page waits for confirmation after showing the transaction hash.

## 6. Run web3.py command-line clients

These scripts run inside the Codespace and connect directly to Node 1. They do not need the browser proxy server.

From the repository root, create and activate a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r web/web3py/requirements.txt
```

If `venv` is unavailable in the Ubuntu environment, install its support package, then retry:

```bash
sudo apt-get update
sudo apt-get install -y python3-venv
```

Run the desired example from the repository root:

| Task | Command | Input |
| --- | --- | --- |
| List accounts | `python web/web3py/listaccounts.py` | None |
| Show balance | `python web/web3py/showbalancebyindex.py` | Zero-based Node 1 account index |
| Show a block | `python web/web3py/blockinfo.py` | Integer block number |
| Show a transaction | `python web/web3py/transactioninfo.py` | Transaction hash |
| Transfer ETH | `python web/web3py/transfer.py` | Recipient address, ETH amount, and sender password |

Alternatively, `cd web/web3py` and run the filenames directly, such as `python listaccounts.py`.

The Python transfer client attempts to use coinbase and falls back to the first account if unavailable. It submits using `personal_sendTransaction` and prints a transaction hash without waiting for mining. Use a funded sender and keep mining until confirmation.

The RPC URL is a source-code constant in each Python script. To query Node 2, change that script's `RPC_URL` to `http://localhost:9545`.

## 7. Run the Flask browser client

**Stop the JavaScript proxy server with Ctrl+C first:** both servers use port 8000 by default.

In a terminal at the repository root, reuse the Python environment:

```bash
source .venv/bin/activate
python -m pip install -r web/web3py_flask_client/requirements.txt
python web/web3py_flask_client/app.py
```

If you have not created `.venv` yet, follow the environment setup in section 6 first.

Open port **8000** through the Codespaces **PORTS** tab and navigate to the root URL. Flask exposes these routes:

| Route | Function |
| --- | --- |
| `/` | Home and connection status |
| `/accounts` | List Node 1 accounts |
| `/balance` | Balance by zero-based account index |
| `/block` | Block information by integer block number |
| `/transaction` | Transaction information by hash |
| `/transfer` | Transfer ETH using the sender password |

The browser talks to Flask; Flask uses web3.py to access `http://localhost:8545`. Flask does not use `web/server.py` or its `/rpc` route.

The transfer route uses the same coinbase/first-account fallback as the CLI and returns the submitted hash without waiting for confirmation.

To return to the JavaScript examples, stop Flask with **Ctrl+C**, then run `./scripts/run-web.sh` from the repository root.

## 8. Suggested classroom workflow

1. Start both nodes and verify their peer counts.
2. Open both Geth consoles and create one account on each node.
3. Mine on Node 1 and observe Node 2 receiving new blocks.
4. List Node 1's accounts and inspect its balance through each client type.
5. Transfer test ETH from Node 1 to the copied Node 2 account address.
6. Use the transaction hash to inspect the transaction and its containing block.
7. In Node 2's console, check the recipient balance:
   `web3.fromWei(eth.getBalance(eth.accounts[0]), "ether")`.
8. Compare the libraries' APIs while using the same underlying blockchain.

## 9. Stop or reset the lab

Stop containers while keeping their data:

```bash
docker compose stop
```

Remove containers and the Compose network while retaining named data volumes:

```bash
docker compose down
```

Start and reconnect later:

```bash
./scripts/run-all-nodes.sh
```

Reopen the console, check `eth.coinbase`, set the etherbase if necessary, and call `miner.start(1)` when ready to mine again.

**Destructive reset:** the following deletes both nodes' named data volumes, including accounts, private keys, blocks, and transaction history:

```bash
docker compose down -v
./scripts/run-all-nodes.sh
```

After a reset, recreate accounts and configure mining again.

Stop any Python server with **Ctrl+C**. When finished, stop the Codespace from GitHub's Codespaces page to end compute usage.

## 10. Troubleshooting and lab scope

| Symptom | What to check |
| --- | --- |
| Script or Compose file cannot be found | Run the command from the repository root |
| IPC connection fails during startup | Inspect `docker compose logs`, wait for startup, then rerun `connect-nodes.sh` |
| Peer count stays at zero | Confirm both services are running and rerun `./scripts/connect-nodes.sh` |
| Account list is empty | Create an account on the node being queried |
| Block number stays at zero | Set an etherbase, start mining, and allow time for Ethash dataset generation |
| Transfer fails or remains pending | Check sender, password, balance including fees, and active mining |
| Browser reports an RPC error | Check Node 1 and use `run-web.sh` for JavaScript clients |
| ethers.js block page returns 404 | Use the encoded filename path in section 5 |
| Port 8000 is already in use | Stop the other proxy or Flask process before switching |
| Flask routes show a directory listing or 404 | Stop the static proxy and start Flask; open its root URL |
| JavaScript paths show Flask 404 pages | Stop Flask and start the static proxy |
| Python import fails | Activate `.venv` and install the appropriate `requirements.txt` |

This configuration is for a controlled private teaching lab. It enables the Geth `personal` API, insecure account unlocking, permissive RPC origins, and Flask debug mode. Keep forwarded ports private and use only disposable lab accounts and test ETH. Do not use this setup for production or real funds.

