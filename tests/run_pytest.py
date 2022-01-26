import pytest

if __name__ == '__main__':
    pytest.main(["-s", "-v", "--setup-show", "--ignore=tests/browser/", "--cov=paralympics_app"])
    # python -m pytest --verbose --setup-show tests/functional/test_main.py --cov=paralympics_app