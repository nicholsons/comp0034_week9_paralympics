import pytest

if __name__ == '__main__':
    pytest.main(["-s", "-v", "--setup-show", "--cov-report term-missing", "--cov=paralympics_app", ])
