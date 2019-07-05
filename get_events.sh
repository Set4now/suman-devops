#!/bin/bash
cert_key="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl --cacert $cert_key -H "Authorization: Bearer token" https://kubernetes.default.svc/api/v1/watch/events -k

