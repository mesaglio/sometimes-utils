from typing import List
import os
import argparse
import subprocess
import json


class CustomGit:

    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def __exec_command(command: str):
        proc = subprocess.Popen(
            [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out, err

    def go_to_branch(self, branch_name: str):
        out, err = self.__exec_command(
            f"cd {self.path} && git checkout {branch_name}")
        return

    def stash_all(self):
        out, err = self.__exec_command(f"cd {self.path} && git stash -u")
        return

    def de_stash(self):
        out, err = self.__exec_command(f"cd {self.path} && git stash pop")
        return

    def find_word(self, word: str):
        out, err = self.__exec_command(f"grep -rnw '{self.path}' -e '{word}'")
        return out.decode()

    def get_all_branches(self):
        out, err = self.__exec_command(f"cd {self.path} && git branch")
        return out.decode()


def __actual_branch__(branch_name: str) -> bool:
    return branch_name[0] == '*'


def __split_and_discar_last(info: str) -> List[str]:
    return info.split('\n')[:-1]


def __clean_branch_name__(branch_name: str) -> str:
    if __actual_branch__(branch_name):
        branch_name = branch_name[1:]
    return branch_name.strip()


def __clean_branches_name__(branches: List[str]) -> List[str]:
    return [__clean_branch_name__(b) for b in branches]


def all_repos(path):
    repos = []
    dirs = os.listdir(path)
    if '.git' in dirs:
        repos.append(path)
    os.chdir(path)
    for file in dirs:
        subdirs = os.listdir(file)
        if '.git' in subdirs:
            repos.append(file)
    return repos


def find_in_repo(path, word):
    if os.path.exists(path) and os.path.isdir(path) and '.git' in os.listdir(path):
        path = os.path.abspath(path)
    else:
        return f"The repo with path: {os.path.abspath(path)} don't exist!"

    g = CustomGit(path)
    branches = g.get_all_branches()
    branches = __split_and_discar_last(branches)
    actual_branch = list(filter(__actual_branch__, branches))
    default_branch = __clean_branch_name__(actual_branch[0])
    branches = __clean_branches_name__(branches)

    pritty_findings = []
    g.stash_all()
    for branch in branches:
        g.go_to_branch(branch)
        findings = g.find_word(word)
        findings = __split_and_discar_last(findings)
        for f in findings:
            f = f.split(':')
            if 'Binary file' in f[0]:
                continue
            pritty_findings.append({
                'branch': branch,
                'file': f[0],
                'line_numbre': f[1],
                'line': f[2].strip()
            })
    findings = pritty_findings
    g.go_to_branch(default_branch)
    g.de_stash()
    return {
        'branches': branches,
        'default_branch': default_branch,
        'findings': findings,
        'path': path,
        'word': word
    }


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(
        description='List the content of a folder')

    my_parser.add_argument('path',
                           metavar='path',
                           type=str, help='repository path')

    my_parser.add_argument('word',
                           type=str, help='the word to find in all branches')

    my_parser.add_argument('-d',
                           action="store_true", default=False,
                           required=False, help="find all repositories in path directory")

    args = my_parser.parse_args()
    results = None
    if args.d:
        results = []
        for path in all_repos(args.path):
            results.append(find_in_repo(path, args.word))
    else:
        results = find_in_repo(args.path, args.word)

    print(json.dumps(results,sort_keys=True))
