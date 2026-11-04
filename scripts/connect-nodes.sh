#!/bin/bash

set -e

echo "Connecting Node 2 to Node 1..."

# Get Node 1 enode
ENODE=$(docker compose exec -T node1 \
  geth --exec 'admin.nodeInfo.enode' attach /data/geth.ipc)

# Remove double quotes
ENODE=$(echo "$ENODE" | tr -d '"')

# Extract enode public-key portion
NODE_ID=$(echo "$ENODE" | cut -d'@' -f1)

# Use Docker service name as hostname
NODE1_ENODE="${NODE_ID}@node1:30303"

echo
echo "Node 1 enode:"
echo "$NODE1_ENODE"

echo
echo "Adding Node 1 as peer of Node 2..."

docker compose exec -T node2 \
  geth --exec "admin.addPeer(\"$NODE1_ENODE\")" \
  attach /data/geth.ipc

echo
echo "Waiting for connection..."
sleep 2

echo
echo "Node 1 peer count:"
docker compose exec -T node1 \
  geth --exec 'net.peerCount' \
  attach /data/geth.ipc

echo
echo "Node 2 peer count:"
docker compose exec -T node2 \
  geth --exec 'net.peerCount' \
  attach /data/geth.ipc

echo
echo "Connection complete."