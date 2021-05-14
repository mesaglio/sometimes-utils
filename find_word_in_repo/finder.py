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
        return out

    def get_all_branches(self):
        out, err = self.__exec_command(f"cd {self.path} && git branch")
        return out


class Repo(object):
    default_branch: str
    branches: str
    findings: List[object]

    def __init__(self, path: str, word: str):
        self.word = word
        if os.path.exists(path) and os.path.isdir(path):
            self.path = os.path.abspath(path)
            self.search_branches()
            self.search_word()
            print(json.dumps(self.__dict__, sort_keys=True))
        else:
            raise Exception(f"The repo with path:\"{path}\" don't exist!")

    def search_word(self):
        g = CustomGit(self.path)
        pritty_findings = []
        g.stash_all()
        for branch in self.branches:
            g.go_to_branch(branch)
            findings = g.find_word(self.word).decode()
            findings = self.__split_and_discar_last(findings)
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
        self.findings = pritty_findings
        g.go_to_branch(self.default_branch)
        g.de_stash()

    @staticmethod
    def __split_and_discar_last(info: str) -> List[str]:
        return info.split('\n')[:-1]

    def search_branches(self):
        g = CustomGit(self.path)
        branches = g.get_all_branches().decode()
        branches = self.__split_and_discar_last(branches)
        actual_branch = list(filter(self.__actual_branch__, branches))
        self.default_branch = self.__clean_branch_name__(actual_branch[0])
        self.branches = self.__clean_branches_name__(branches)

    def __clean_branch_name__(self, branch_name: str) -> str:
        if self.__actual_branch__(branch_name):
            branch_name = branch_name[1:]
        return branch_name.strip()

    @staticmethod
    def __actual_branch__(branch_name: str) -> bool:
        return branch_name[0] == '*'

    def __clean_branches_name__(self, branches: List[str]) -> List[str]:
        return [self.__clean_branch_name__(b) for b in branches]


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(
        description='List the content of a folder')

    my_parser.add_argument('path',
                           metavar='path',
                           type=str, help='repository path')

    my_parser.add_argument('word',
                           type=str, help='the word to find in all branches')

    args = my_parser.parse_args()
    Repo(args.path, args.word)
