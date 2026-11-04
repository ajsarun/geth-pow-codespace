#!/bin/sh

set -e

DATADIR="/data"
GENESIS_FILE="/config/genesis.json"
NODE_NAME="${NODE_NAME:-geth-node}"

echo "========================================"
echo " Private Ethereum PoW Lab"
echo " Node: ${NODE_NAME}"
echo " Geth: v1.10.26"
echo " Chain ID: 2026"
echo "========================================"

# Initialize blockchain only the first time.
if [ ! -d "${DATADIR}/geth/chaindata" ]; then
    echo "Initializing genesis block..."

    geth \
        --datadir "${DATADIR}" \
        init "${GENESIS_FILE}"
fi

echo "Starting ${NODE_NAME}..."

exec geth \
    --identity "${NODE_NAME}" \
    --datadir "${DATADIR}" \
    --networkid 2026 \
    --nodiscover \
    --syncmode full \
    --port 30303 \
    --http \
    --http.addr 0.0.0.0 \
    --http.port 8545 \
    --http.api "eth,net,web3, personal" \
    --http.corsdomain "*" \
    --http.vhosts "*" \
    --ws \
    --ws.addr 0.0.0.0 \
    --ws.port 8546 \
    --ws.api "eth,net,web3" \
    --ws.origins "*" \
    --allow-insecure-unlock \
    --verbosity 3
