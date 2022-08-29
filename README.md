# Cachi2 PoC

## How to test it

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --url="https://github.com/release-engineering/retrodep" --ref="12a0692be09fc18ce82a71904562d8408fe2296a" --workdir=$(mktemp -d)
```
