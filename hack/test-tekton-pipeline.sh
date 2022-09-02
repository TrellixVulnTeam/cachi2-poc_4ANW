#!/bin/bash
kubectl apply -k tekton

tkn pipeline start go-build \
-s pipeline \
-w name=workspace,claimName=cachito \
-w name=registry-auth,secret=redhat-appstudio-staginguser-pull-secret \
-p git-url="https://github.com/release-engineering/retrodep" \
-p revision="12a0692be09fc18ce82a71904562d8408fe2296a" \
-p output-image="quay.io/bpimente/retrodep:12a0692be09fc18ce82a71904562d8408fe2296a" \
--use-param-defaults
