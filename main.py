import sys
import subprocess
import time
import requests
from os import chdir
from pathlib import Path

from onlinejudge.dispatch import contest_from_url
from onlinejudge.utils import with_cookiejar

ATCODER_URL = 'https://atcoder.jp/contests/'


def generate_contest_directory(contest_id):
    contest = contest_from_url(ATCODER_URL + contest_id)
    contest_dir = Path(contest_id).resolve()
    contest_dir.mkdir()
    chdir(contest_dir)
    with with_cookiejar(requests.Session()) as sess:
        problems = contest.list_problems(session=sess)
    for i, problem in enumerate(problems):

        problem_url = problem.get_url()
        problem_dir = contest_dir.joinpath(chr(ord('a') + i))
        problem_dir.mkdir()
        chdir(problem_dir)
        command = ['pipenv', 'run', 'oj', 'download', problem_url]
        subprocess.run(command).check_returncode()
        problem_dir.joinpath('main.py').touch()
        time.sleep(1)
    chdir(contest_dir)


if __name__ == '__main__':
    generate_contest_directory(sys.argv[1])
