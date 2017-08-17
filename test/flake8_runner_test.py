import subprocess


def test_passes_lint():
    subprocess.check_call('flake8')
