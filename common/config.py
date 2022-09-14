config = None

class Config:
    cachito_athens_url = None
    cachito_bundles_dir = None
    cachito_sources_dir = None
    cachito_default_environment_variables = {
        "gomod": {"GOSUMDB": {"value": "off", "kind": "literal"}},
        "npm": {
            "CHROMEDRIVER_SKIP_DOWNLOAD": {"value": "true", "kind": "literal"},
            "CYPRESS_INSTALL_BINARY": {"value": "0", "kind": "literal"},
            "GECKODRIVER_SKIP_DOWNLOAD": {"value": "true", "kind": "literal"},
            "SKIP_SASS_BINARY_DOWNLOAD_FOR_CI": {"value": "true", "kind": "literal"},
        },
    }
    cachito_gomod_ignore_missing_gomod_file = False
    cachito_gomod_download_max_tries = 5
    cachito_gomod_file_deps_allowlist = {}
    cachito_gomod_strict_vendor = False
    cachito_subprocess_timeout = 3600

    def __init__(self, work_dir):
        self.cachito_bundles_dir = work_dir
        self.cachito_sources_dir = work_dir


def set_worker_config(work_dir):
    global config 
    config = Config(work_dir)


def get_worker_config():
    return config
