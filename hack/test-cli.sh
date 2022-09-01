#!/bin/bash 
./venv/bin/python3 main.py --url="https://github.com/release-engineering/retrodep" --ref="12a0692be09fc18ce82a71904562d8408fe2296a" --workdir="$(mktemp -d)"
