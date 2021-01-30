#!/bin/sh
set -e
user=ipfs
repo="$IPFS_PATH"

if [ `id -u` -eq 0 ]; then
  echo "Changing user to $user"
  # ensure folder is writable
  su-exec "$user" test -w "$repo" || chown -R -- "$user" "$repo"
  # restart script with new privileges
  exec su-exec "$user" "$0" "$@"
fi

# 2nd invocation with regular user
ipfs version

if [ -e "$repo/config" ]; then
  echo "Found IPFS fs-repo at $repo"
else
  case "$IPFS_PROFILE" in
    "") INIT_ARGS="" ;;
    *) INIT_ARGS="--profile=$IPFS_PROFILE" ;;
  esac

  ipfs init $INIT_ARGS
  ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
  ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
  ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001"]' --json
  ipfs config Peering.Peers '[{"ID":"QmTczxAdhstmCTa4DMx3a7guuCBrt4Q1zujaxct1iGg4LD", "Addrs":["/ip4/34.220.29.107/tcp/4001"]}, {"ID":"QmZcYrzhxp6V8VN6V4BCmGh342qGBd3BRme61gYRnQqNYL", "Addrs":["/ip4/34.220.216.205/tcp/4001"]},{ "ID": "12D3KooWQw3vx2E4FKpL9GHC9BpFya1MXVUFEVBAQVhMDkreCqwF", "Addrs": ["/ip4/185.215.224.79/tcp/4001"] }, { "ID": "12D3KooWD4Z47R1pnzTxCVQAiTKTHasWU2xTAcffyC38BNKM68yw", "Addrs": ["/ip4/185.215.227.40/tcp/4001"] }, { "ID": "QmbPFTECrXd7o2HS2jWAJ2CyAckv3Z5SFy8gnEHKxxH52g", "Addrs": ["/ip4/144.172.69.157/tcp/4001"] }]' --json

  # Set up the swarm key, if provided
  SWARM_KEY_FILE="$repo/swarm.key"
  SWARM_KEY_PERM=0400

  # Create a swarm key from a given environment variable
  if [ ! -z "$IPFS_SWARM_KEY" ] ; then
    echo "Copying swarm key from variable..."
    echo -e "$IPFS_SWARM_KEY" >"$SWARM_KEY_FILE" || exit 1
    chmod $SWARM_KEY_PERM "$SWARM_KEY_FILE"
  fi

  # Unset the swarm key variable
  unset IPFS_SWARM_KEY

  # Check during initialization if a swarm key was provided and
  # copy it to the ipfs directory with the right permissions
  # WARNING: This will replace the swarm key if it exists
  if [ ! -z "$IPFS_SWARM_KEY_FILE" ] ; then
    echo "Copying swarm key from file..."
    install -m $SWARM_KEY_PERM "$IPFS_SWARM_KEY_FILE" "$SWARM_KEY_FILE" || exit 1
  fi

  # Unset the swarm key file variable
  unset IPFS_SWARM_KEY_FILE
  ipfs config Datastore.StorageMax 30GB
  ipfs config Swarm.EnableAutoRelay true
  ipfs config Swarm.EnableRelayHop false
  ipfs config Discovery.MDNS.Enabled true

  # Get current id
  current_node_id=$(ipfs id -f="<id>")
  ipfs bootstrap add /dns4/watchit_ipfs/tcp/4001/p2p/"$current_node_id"
  ipfs bootstrap add /dns4/watchit_ipfs/tcp/4002/ws/p2p/"$current_node_id"
  ipfs bootstrap add /ip4/0.0.0.0/tcp/4001/p2p/"$current_node_id"
  ipfs bootstrap add /ip4/0.0.0.0/tcp/4002/ws/p2p/"$current_node_id"

  export IPFS_FD_MAX=8192
  ulimit -n 8192

fi

exec ipfs "$@"
