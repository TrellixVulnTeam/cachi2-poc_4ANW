# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import os
import pathlib
import shutil
from pathlib import Path
from typing import Any

from common.config import get_worker_config

# Subclassing from type(Path()) is a workaround because pathlib does not
# support subclass from Path directly. This base type will be the correct type
# for Linux or Windows individually.
base_path: Any = type(Path())

log = logging.getLogger(__name__)


class BaseRequestBundleDir(base_path):
    """
    Represents a directory tree for a request.

    :param int request_id: the request ID.
    :param str root: the root directory. A request bundle directory will be
        created under ``root/temp/``.
    """

    go_mod_cache_download_part = Path("pkg", "mod", "cache", "download")

    def __new__(cls, root, source_dir, app_subpath=os.curdir):
        """
        Create a new Path object.

        :param int request_id: the ID of the request this bundle is for.
        :param str root: the root directory to the bundles.
        :param str app_subpath: an optional relative path to where the application resides in the
            source directory. This sets ``self.source_dir`` and all other related paths to
            start from that directory. If this is not set, it is assumed the application lives in
            the root of the source directory.
        """
        self = super().__new__(cls, root)
        self._path_root = root

        self.source_root_dir = self.joinpath(source_dir)
        self.source_dir = self.source_root_dir.joinpath(app_subpath)
        self.go_mod_file = self.source_dir.joinpath("go.mod")

        self.deps_dir = self.joinpath("deps")
        self.gomod_download_dir = self.joinpath("deps", "gomod", cls.go_mod_cache_download_part)

        self.node_modules = self.source_dir.joinpath("node_modules")
        self.npm_deps_dir = self.joinpath("deps", "npm")
        self.npm_package_file = self.source_dir.joinpath("package.json")
        self.npm_package_lock_file = self.source_dir.joinpath("package-lock.json")
        self.npm_shrinkwrap_file = self.source_dir.joinpath("npm-shrinkwrap.json")

        self.pip_deps_dir = self.joinpath("deps", "pip")

        self.rubygems_deps_dir = self.joinpath("deps", "rubygems")

        self.yarn_deps_dir = self.joinpath("deps", "yarn")

        self.bundle_archive_file = Path(root, f"bundle.tar.gz")
        self.bundle_archive_checksum = Path(root, f"bundle.checksum.sha256")

        self.packages_data = Path(root, f"packages.json")
        self.gomod_packages_data = self.joinpath("gomod_packages.json")
        self.npm_packages_data = self.joinpath("npm_packages.json")
        self.pip_packages_data = self.joinpath("pip_packages.json")
        self.yarn_packages_data = self.joinpath("yarn_packages.json")
        self.rubygems_packages_data = self.joinpath("rubygems_packages.json")
        self.git_submodule_packages_data = self.joinpath("git_submodule_packages.json")

        return self

    def app_subpath(self, subpath):
        """Create a new ``RequestBundleDir`` object with the sources pointed to the subpath."""
        return BaseRequestBundleDir(self._path_root, self.source_dir, subpath)

    def relpath(self, path):
        """Get the relative path of a path from the root of the source directory."""
        return os.path.relpath(path, start=self.source_root_dir)

    def rmtree(self):
        """Remove this directory tree entirely."""
        shutil.rmtree(str(self))


class RequestBundleDir(BaseRequestBundleDir):
    """
    Represents a concrete request bundle directory used on the worker.

    The root directory is set to the ``cachito_bundles_dir`` configuration.

    By default, this request bundle directory and its dependency directory will
    be created when this object is instantiated.

    :param int request_id: the request ID.
    """

    def __new__(cls, source_dir):
        """Create a new Path object."""
        root_dir = get_worker_config().cachito_bundles_dir
        self = super().__new__(cls, root_dir, source_dir)

        log.debug("Ensure directory %s exists.", self)
        log.debug("Ensure directory %s exists.", self.deps_dir)
        self.deps_dir.mkdir(parents=True, exist_ok=True)

        return self

class SourcesDir(base_path):
    """
    Represents a sources directory tree for a package.

    The directory will be created automatically when this object is instantiated.

    :param str repo_name: a namespaced repository name of package. For example,
        ``release-engineering/retrodep``.
    :param str ref: the revision reference used to construct archive filename.
    """

    def __new__(cls, repo_name, ref):
        """Create a new Path object."""
        self = super().__new__(cls, get_worker_config().cachito_sources_dir)

        repo_relative_dir = pathlib.Path(*repo_name.split("/"))
        self.package_dir = self.joinpath(repo_relative_dir)
        self.archive_path = self.joinpath(repo_relative_dir, f"{ref}.tar.gz")

        log.debug("Ensure directory %s exists.", self.package_dir)
        self.package_dir.mkdir(parents=True, exist_ok=True)

        return self
