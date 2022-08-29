import argparse
import logging
import os

from common.config import set_worker_config
from common.models import Request
from tasks.git import fetch_app_source
from tasks.gomod import fetch_gomod_source


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str)
parser.add_argument("--ref", type=str)
parser.add_argument("--workdir", type=str)

args = parser.parse_args()

work_dir = os.path.abspath(args.workdir)
set_worker_config(work_dir)

request = Request(
    id=1, 
    url=args.url, 
    ref=args.ref
)

fetch_app_source(request)
fetch_gomod_source(request)
