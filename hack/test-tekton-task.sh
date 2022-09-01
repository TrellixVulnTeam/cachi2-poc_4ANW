#!/bin/bash
kubectl apply -k tekton

tkn task start cachito -w name=source,claimName=cachito \
-p url="https://github.com/release-engineering/retrodep" \
-p revision="12a0692be09fc18ce82a71904562d8408fe2296a" \
--use-param-defaults
