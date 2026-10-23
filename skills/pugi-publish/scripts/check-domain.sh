#!/usr/bin/env bash
# Look at what DNS and HTTPS say about a custom domain for a Pugi app. Read-only.
#
#   check-domain.sh app.example.com your-app.pugi.app [--resolver <ip>]
#
# It reports three separate things:
#   DNS    the CNAME chain for the domain, from your system resolver
#          (or the resolver you name with --resolver);
#   HTTPS  whether https://<domain> answers with a valid certificate;
#   Pugi   only the Check button in the Publish panel can confirm that Pugi
#          serves the app on this domain. This script cannot.
#
# Exit codes: 0 DNS points at the app and HTTPS answers · 1 not yet ·
#             2 usage error · 3 cannot tell from DNS (flattened or proxied record).
# Requires: dig (or host) and curl. Sends the domain name to your DNS resolver
# and one HTTPS request to the domain itself.

set -u
usage() { echo "usage: $0 <your-domain> <your-app.pugi.app> [--resolver <ip>]"; exit 2; }
[ $# -eq 2 ] || [ $# -eq 4 ] || usage

host_re='^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$'
norm() { printf '%s' "$1" | tr 'A-Z' 'a-z' | sed -E 's#^https?://##; s#/.*##; s#\.$##'; }
domain=$(norm "$1")
target=$(norm "$2")
resolver=""
if [ $# -eq 4 ]; then
  [ "$3" = "--resolver" ] || usage
  resolver="$4"
  printf '%s' "$resolver" | grep -Eq '^[0-9a-fA-F:.]+$' || { echo "The resolver must be an IP address."; exit 2; }
fi

printf '%s' "$domain" | grep -Eq "$host_re" || { echo "Not a valid domain name: $1"; exit 2; }
printf '%s' "$target" | grep -Eq "$host_re" || { echo "Not a valid host: $2"; exit 2; }
case "$target" in *.pugi.app) ;; *) echo "The second argument must be the app's *.pugi.app host."; exit 2 ;; esac
[ "$domain" = "$target" ] && { echo "Give your own domain first, then the app's *.pugi.app host."; exit 2; }

chain=""; addrs=""
if command -v dig >/dev/null 2>&1; then
  at=(); [ -n "$resolver" ] && at=("@$resolver")
  # dig +short follows the chain: names first, then addresses.
  out=$(dig +short +time=5 +tries=2 ${at[@]+"${at[@]}"} -t A -q "$domain" 2>/dev/null)
  chain=$(printf '%s\n' "$out" | grep -E '[a-z]' | sed -E 's#\.$##' | tr '\n' ' ')
  addrs=$(printf '%s\n' "$out" | grep -Ev '[a-z]' | grep -E '^[0-9.]+$' | tr '\n' ' ')
elif command -v host >/dev/null 2>&1; then
  out=$(host -W 5 "$domain" ${resolver:+"$resolver"} 2>/dev/null)
  chain=$(printf '%s\n' "$out" | awk '/is an alias for/ {print $NF}' | sed -E 's#\.$##' | tr '\n' ' ')
  addrs=$(printf '%s\n' "$out" | awk '/has address/ {print $NF}' | tr '\n' ' ')
else
  echo "Needs dig or host."; exit 2
fi

echo "Domain:   $domain"
echo "Resolver: ${resolver:-system default}"
echo "CNAME:    ${chain:-none}"
echo "A:        ${addrs:-none}"
echo "Wanted:   CNAME $domain -> $target (or the record the Publish panel shows)"

dns=1
case " $chain " in
  *" $target "*) echo "DNS:      points at the app" ; dns=0 ;;
  *)
    if [ -z "$chain" ] && [ -n "$addrs" ]; then
      echo "DNS:      only addresses, no CNAME. This can be a flattened or proxied record that still works,"
      echo "          or a record that points elsewhere. DNS alone cannot tell; use the panel's Check."
      dns=3
    elif [ -z "$chain" ]; then
      echo "DNS:      no record yet."
    else
      echo "DNS:      points somewhere else (${chain% })."
    fi
    ;;
esac

code=$(curl -sS -o /dev/null -m 15 --proto '=https' -w '%{http_code}' "https://$domain/" 2>/dev/null || true)
case "$code" in
  2??|3??) echo "HTTPS:    answers (HTTP $code) with a valid certificate" ; https=0 ;;
  000|"")  echo "HTTPS:    no answer, or the certificate is not valid yet" ; https=1 ;;
  *)       echo "HTTPS:    answers HTTP $code" ; https=1 ;;
esac
echo "Pugi:     press Check on the domain in the Publish panel. It shows Verified when Pugi serves the app there."

[ "$dns" -eq 0 ] && [ "$https" -eq 0 ] && exit 0
[ "$dns" -eq 3 ] && exit 3
exit 1
