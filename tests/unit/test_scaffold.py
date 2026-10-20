from importlib.metadata import version

import recall


def test_package_imports() -> None:
    assert recall.__version__ == "0.1.0"


def test_installed_package_version_matches() -> None:
    assert version("recall-memory") == recall.__version__
