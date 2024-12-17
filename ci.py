import subprocess


def coverage():
    from qpyci.commands import run_tests
    run_tests('qpyconf')


def check_format():
    subprocess.run(['uvx', 'ruff', 'check', '--fix'], check=True)
    subprocess.run(['uvx', 'ruff', 'format'], check=True)

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1:
#         if sys.argv[1] == 'check':
#             check_format()
#         elif sys.argv[1] == 'cov':
#             coverage()
#     else:
#         check_format()
