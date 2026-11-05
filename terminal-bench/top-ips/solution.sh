#!/bin/bash
# Reference solution: count 2xx requests per IP, print top 3.
awk '
  $0 ~ /^[0-9.]+ / && match($0, /" [0-9][0-9][0-9] [0-9]+$/) {
    status = substr($0, RSTART + 2, 3)
    if (status >= 200 && status <= 299) c[$1]++
  }
  END { for (ip in c) print ip, c[ip] }
' /app/access.log | sort -k2,2nr -k1,1 | head -n 3 > /app/top_ips.txt
