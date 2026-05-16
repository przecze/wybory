#!/bin/sh
set -e

apk add --no-cache wireguard-tools wireguard-go

if [ ! -s /etc/wireguard/gateway.conf ]; then
  echo "Missing or empty gateway.conf - run 'make wg-create' first"
  exit 1
fi

export FLY_DNS=$(grep "^DNS" /etc/wireguard/gateway.conf | cut -d= -f2 | tr -d " ")
WG_ADDR=$(grep "^Address" /etc/wireguard/gateway.conf | cut -d= -f2 | tr -d " ")
echo "Fly DNS: $FLY_DNS"

envsubst "\${FLY_DNS}" < /etc/nginx/templates/default.conf > /etc/nginx/conf.d/default.conf

echo "Bringing up WireGuard tunnel..."
if ! ip link add dev gateway type wireguard 2>/dev/null; then
  wireguard-go gateway
fi
grep -v "^\(Address\|DNS\)" /etc/wireguard/gateway.conf > /tmp/wg.conf
wg setconf gateway /tmp/wg.conf
ip -6 addr add "$WG_ADDR" dev gateway
ip link set mtu 1420 up dev gateway
ip -6 route add fdaa:4d:3b81::/48 dev gateway 2>/dev/null || true
echo "nameserver $FLY_DNS" > /etc/resolv.conf
echo "WireGuard up, nginx starting..."

exec nginx -g "daemon off;"
