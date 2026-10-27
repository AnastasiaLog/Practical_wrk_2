import pytest
from src.validators import ConfigError, validate_package_name, validate_repo_mode

def test_package_name_ok():
    assert validate_package_name("curl") == "curl"

def test_package_name_error():
    with pytest.raises(ConfigError):
        validate_package_name("")

def test_repo_mode_ok():
    assert validate_repo_mode("remote") == "remote"

def test_repo_mode_error():
    with pytest.raises(ConfigError):
        validate_repo_mode("invalid")