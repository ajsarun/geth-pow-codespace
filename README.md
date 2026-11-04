# Private Ethereum PoW Lab on GitHub Codespaces

This repository provides a small **private Ethereum Proof-of-Work network** for teaching and experimentation.

It is designed to run entirely inside **GitHub Codespaces**, so students do not need to install Geth, Docker, Node.js, or other blockchain software on their own computers.

The environment contains:

- Two private Ethereum nodes
- Geth v1.10.26
- Ethash Proof of Work
- A shared private genesis block
- Manual peer connection between Node 1 and Node 2
- Geth JavaScript Console access
- JSON-RPC access
- Web3.js browser clients
- ethers.js browser clients
- web3.py command-line clients
- web3.py + Flask browser client

> This lab uses a legacy Proof-of-Work version of Ethereum for educational purposes. Ethereum Mainnet currently uses Proof of Stake.

---

## 1. Repository Overview

A typical repository structure is:

```text
.
├── .devcontainer/
│   └── devcontainer.json
│
├── geth/
│   ├── genesis.json
│   └── start.sh
│
├── scripts/
│   ├── run-node1.sh
│   ├── run-node2.sh
│   ├── run-all.sh
│   ├── connect-nodes.sh
│   ├── console-node1.sh
│   ├── console-node2.sh
│   └── run-web.sh
│
├── web/
│   ├── server.py
│   ├── listaccounts.html
│   ├── showbalancebyindex.html
│   ├── blockinfo.html
│   ├── transactioninfo.html
│   └── transfer.html
│
├── web3py_clients/
│   ├── listaccounts.py
│   ├── showbalancebyindex.py
│   ├── blockinfo.py
│   ├── transactioninfo.py
│   ├── transfer.py
│   └── requirements.txt
│
├── web3py_flask_client/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│
└── compose.yaml
```

The exact filenames in your repository may differ slightly.

---

# 2. Open the Repository in GitHub Codespaces

From the GitHub repository page:

1. Click **Code**
2. Select **Codespaces**
3. Click **Create codespace on main**

GitHub will create a cloud development environment and open VS Code in the browser.

The Codespace uses Docker to run the Ethereum nodes.

---

# 3. Start the Ethereum Nodes

## Start Node 1

```bash
./scripts/run-node1.sh
```

## Start Node 2

```bash
./scripts/run-node2.sh
```

## Start Both Nodes

```bash
./scripts/run-all.sh
```

You can also start the nodes directly with Docker Compose:

```bash
docker compose up -d node1 node2
```

Check their status:

```bash
docker compose ps
```

You should see both containers running.

Example:

```text
NAME         STATUS
geth-node1   Up
geth-node2   Up
```

---

# 4. Connect Node 1 and Node 2

The nodes use the same genesis block and network ID, but they are not automatically connected when `--nodiscover` is used.

Run:

```bash
./scripts/connect-nodes.sh
```

The script:

1. Reads the enode URL of Node 1
2. Replaces the internal address with the Docker hostname `node1`
3. Calls `admin.addPeer(...)` on Node 2
4. Checks the peer count of both nodes

After a successful connection, each node should report:

```javascript
net.peerCount
```

Result:

```text
1
```

You can also inspect the peer information:

```javascript
admin.peers
```

---

# 5. Open the Geth JavaScript Console

## Node 1 Console

```bash
./scripts/console-node1.sh
```

Equivalent command:

```bash
docker compose exec node1 geth attach /data/geth.ipc
```

## Node 2 Console

```bash
./scripts/console-node2.sh
```

Equivalent command:

```bash
docker compose exec node2 geth attach /data/geth.ipc
```

You should see the Geth JavaScript Console prompt:

```text
Welcome to the Geth JavaScript console!

>
```

---

# 6. Useful Geth Console Commands

## Show accounts

```javascript
eth.accounts
```

Initially, the result may be:

```javascript
[]
```

because no accounts are pre-funded or pre-created.

---

## Create an Account on Node 1

```javascript
var account1 = personal.newAccount("node1pass")
```

Check:

```javascript
eth.accounts
```

---

## Create an Account on Node 2

```javascript
var account2 = personal.newAccount("node2pass")
```

---

## Check Account Balance

```javascript
eth.getBalance(account1)
```

Convert Wei to Ether:

```javascript
web3.fromWei(
    eth.getBalance(account1),
    "ether"
)
```

---

## Set the Miner Account

On Node 1:

```javascript
miner.setEtherbase(account1)
```

Check:

```javascript
eth.coinbase
```

---

## Start Mining

```javascript
miner.start(1)
```

The argument `1` means one mining thread.

Check:

```javascript
eth.mining
```

---

## Stop Mining

```javascript
miner.stop()
```

---

## Check the Current Block Number

```javascript
eth.blockNumber
```

---

## View the Latest Block

```javascript
eth.getBlock("latest")
```

---

## Check the Transaction Pool

```javascript
txpool.status
```

---

# 7. JSON-RPC Endpoints

Inside the Codespace:

```text
Node 1 HTTP RPC
http://localhost:8545
```

```text
Node 2 HTTP RPC
http://localhost:9545
```

Example JSON-RPC request to Node 1:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:8545
```

Example response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x15"
}
```

---

# 8. Browser Clients

Browser applications cannot normally use:

```text
http://localhost:8545
```

because `localhost` in the browser refers to the user's local computer, not the Codespace.

For browser clients, this repository uses a small Python proxy server.

The browser communicates with:

```text
/rpc
```

and the proxy forwards the request to:

```text
http://localhost:8545
```

The architecture is:

```text
Browser
   |
   | HTTPS
   v
GitHub Codespaces Port 8000
   |
   | /rpc
   v
Python Proxy
   |
   v
Geth Node 1 :8545
```

---

# 9. Start the Browser Client Server

Run:

```bash
./scripts/run-web.sh
```

or:

```bash
cd web
python3 server.py
```

The web server runs on:

```text
Port 8000
```

In GitHub Codespaces:

1. Open the **PORTS** tab
2. Find port `8000`
3. Click **Open in Browser**

The URL will look similar to:

```text
https://<codespace-name>-8000.app.github.dev/
```

---

# 10. Web3.js Browser Clients

The Web3.js clients use **Web3.js v4** as an ES module.

The provider is created with:

```javascript
import { Web3 }
from "https://cdn.jsdelivr.net/npm/web3@4.16.0/+esm";

const web3 = new Web3(
    window.location.origin + "/rpc"
);
```

Available clients include:

```text
listaccounts.html
showbalancebyindex.html
blockinfo.html
transactioninfo.html
transfer.html
```

Example URLs:

```text
https://<codespace-name>-8000.app.github.dev/listaccounts.html
```

```text
https://<codespace-name>-8000.app.github.dev/blockinfo.html
```

The five Web3.js examples demonstrate:

1. Listing Ethereum accounts
2. Reading an account balance
3. Reading block information
4. Reading transaction information
5. Sending Ether

---

# 11. ethers.js Browser Clients

The ethers.js examples use **ethers.js v6**.

The provider is created with:

```javascript
import { ethers }
from "https://cdn.jsdelivr.net/npm/ethers@6.7.0/+esm";

const provider =
    new ethers.JsonRpcProvider(
        window.location.origin + "/rpc"
    );
```

The same general client examples are available:

```text
listaccounts.html
showbalancebyindex.html
blockinfo.html
transactioninfo.html
transfer.html
```

These examples demonstrate the ethers.js equivalent of the Web3.js examples.

---

# 12. web3.py Command-Line Clients

The Python command-line clients connect directly to Geth because they run inside the Codespace.

They do not require `server.py`.

Move to the directory:

```bash
cd web3py_clients
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The provider is:

```python
from web3 import Web3

web3 = Web3(
    Web3.HTTPProvider(
        "http://localhost:8545"
    )
)
```

---

## List Accounts

```bash
python listaccounts.py
```

---

## Show Balance by Account Index

```bash
python showbalancebyindex.py
```

---

## Show Block Information

```bash
python blockinfo.py
```

Enter a block number when requested.

Example:

```text
Enter block number: 10
```

---

## Show Transaction Information

```bash
python transactioninfo.py
```

Enter a transaction hash when requested.

---

## Transfer Ether

```bash
python transfer.py
```

The program asks for:

```text
Transfer to:
Amount (ETH):
Passphrase:
```

and then submits the transaction through Geth.

---

# 13. web3.py Flask Browser Client

The Flask version provides all five web3.py examples through one browser application.

Move to the Flask client directory:

```bash
cd web3py_flask_client
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

The Flask application runs on port:

```text
8000
```

Open port `8000` from the Codespaces **PORTS** tab.

The application contains the following pages:

```text
Home
Accounts
Balance
Block
Transaction
Transfer
```

The architecture is:

```text
Browser
   |
   v
Flask
   |
   v
web3.py
   |
   | JSON-RPC
   v
Geth Node 1 :8545
```

Unlike the JavaScript browser clients, Flask and web3.py can communicate directly with `localhost:8545` because the Python application itself runs inside the Codespace.

---

# 14. Sending Transactions

The lab uses the Geth `personal` API for educational purposes.

The Geth startup configuration should include:

```text
--http.api "eth,net,web3,personal"
--allow-insecure-unlock
```

This allows the lab clients to use operations such as:

```text
personal_sendTransaction
```

or account unlocking through JSON-RPC.

> `--allow-insecure-unlock` should only be used in a controlled private teaching environment. Do not use this configuration on a public Ethereum node or production system.

---

# 15. Example Learning Workflow

A suggested exercise sequence is:

```text
1. Start Node 1 and Node 2
2. Connect the two nodes
3. Open both JavaScript consoles
4. Verify eth.accounts is empty
5. Create one account on each node
6. Confirm both accounts have 0 ETH
7. Set Node 1's account as the miner account
8. Start mining on Node 1
9. Observe block propagation to Node 2
10. Check the mining reward on Node 1
11. Transfer ETH from Node 1 to Node 2
12. Inspect the transaction
13. Inspect the block containing the transaction
14. Repeat the same operations using:
    - Web3.js
    - ethers.js
    - web3.py
    - Flask + web3.py
```

This allows students to compare different Ethereum client libraries while interacting with the same private blockchain.

---

# 16. Stop the Ethereum Network

Stop both containers:

```bash
docker compose stop
```

or remove the containers:

```bash
docker compose down
```

The blockchain data is retained in Docker volumes.

---

# 17. Reset the Blockchain

To completely remove both nodes' blockchain data, accounts, keystores, mined blocks, and transaction history:

```bash
docker compose down -v
```

Then restart:

```bash
docker compose up -d
```

The network will return to the initial genesis state.

---

# 18. Stop the GitHub Codespace

When the lab is finished, stop the Codespace to avoid unnecessary compute usage.

From GitHub:

```text
Codespaces
→ ...
→ Stop codespace
```

Stopping a Codespace stops compute usage, but the Codespace storage remains until the Codespace is deleted.

---

# 19. Important Notes

This repository is intended only for:

- Blockchain education
- Ethereum architecture experiments
- JSON-RPC demonstrations
- Geth JavaScript Console exercises
- Web3.js exercises
- ethers.js exercises
- web3.py exercises

It is **not intended for production use**.

The network uses:

```text
Geth v1.10.26
Ethash
Proof of Work
Private Genesis Block
```

This configuration is intentionally based on legacy Ethereum Proof of Work because it makes concepts such as mining, block rewards, transaction pools, peer synchronization, and block creation easy to observe in a classroom environment.

---

# 20. Summary

This Codespace provides a complete small Ethereum laboratory:

```text
                   +----------------+
                   |    Browser     |
                   +-------+--------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
   Web3.js / ethers.js                Flask Web App
          |                                 |
          v                                 v
      /rpc Proxy                         web3.py
          |                                 |
          +---------------+-----------------+
                          |
                          v
                    Geth Node 1
                          |
                          | P2P
                          v
                    Geth Node 2
```

Students can therefore experiment with the same Ethereum network using several different client technologies while learning how accounts, transactions, mining, blocks, RPC, and peer-to-peer synchronization work.
