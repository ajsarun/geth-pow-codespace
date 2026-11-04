#!/bin/bash
set -e

echo "Starting Ethereum PoW Network..."
docker compose up -d node1 node2

echo
echo "Waiting for nodes to start..."
sleep 3

echo
echo "Connecting nodes..."
./scripts/connect-nodes.sh

echo
echo "======================================"
echo " Ethereum PoW Network Ready"
echo "======================================"

docker compose ps

echo
echo "Node 1 console:"
echo "./scripts/usenode1.sh"

echo
echo "Node 2 console:"
echo "./scripts/usenode2.sh"