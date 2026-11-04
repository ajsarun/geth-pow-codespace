#!/bin/bash

set -e

echo "Connecting Node 2 to Node 1..."

# Get Node 1 enode URL
ENODE=$(docker compose exec -T node1 \
  geth attach /data/geth.ipc \
  --exec 'admin.nodeInfo.enode')

# Remove quotes
ENODE=$(echo "$ENODE" | tr -d '"')

# Replace Node 1 internal IP/host with Docker service name
NODE_ID=$(echo "$ENODE" | cut -d'@' -f1)

NODE1_ENODE="${NODE_ID}@node1:30303"

echo
echo "Node 1 enode:"
echo "$NODE1_ENODE"

echo
echo "Adding Node 1 as peer of Node 2..."

docker compose exec -T node2 \
  geth attach /data/geth.ipc \
  --exec "admin.addPeer(\"$NODE1_ENODE\")"

echo
echo "Waiting for peer connection..."
sleep 2

echo
echo "Node 1 peer count:"
docker compose exec -T node1 \
  geth attach /data/geth.ipc \
  --exec 'net.peerCount'

echo
echo "Node 2 peer count:"
docker compose exec -T node2 \
  geth attach /data/geth.ipc \
  --exec 'net.peerCount'

echo
echo "Connection complete."