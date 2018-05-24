#!/usr/bin/env python3

from pathlib import Path
from string import Template

import os
import yaml


def build_template(cfg: dict) -> dict:
    """
    Build string's template dictionary
    :rtype: dict
    :param cfg: representation of the config
    :return: dictionary to be used with Template().substutute() function
    """
    task = cfg['main']

    def concat(*dictionaries: dict) -> dict:
        res = dict()
        for d in dictionaries:
            res = {**res, **d}
        return res

    template = concat(task['miner'], task['pool'], cfg['rig'])
    return template


def create_command(cfg: dict) -> str:
    """
    Create a command to be executed to run miner
    :rtype: str
    :param cfg: representation of the config
    :return: string to be passed to os.system() function
    """
    template = build_template(cfg)
    path = str(absolutize(template['bin']))
    args = Template(template['args']).substitute(template)
    return path + " " + args


def read_file(path: Path) -> dict:
    with open(path, 'r') as file:
        try:
            config = yaml.load(file)
            return config
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print('Error position: ({}:{})', mark.line + 1, mark.column + 1, flush=True)


def absolutize(rel: Path) -> Path:
    """
    Return absolute path
    :rtype: Path
    :param rel: relative to user's home path
    :return: the absolute path
    """
    return Path().home().joinpath(rel)


def run(conf_file: Path):
    cfg = read_file(conf_file)
    cmd = create_command(cfg)
    # print(cmd)
    os.system(cmd)

def main():
    conf_file_here = False  # Set to True for debug or experiments

    if conf_file_here:
        conf_file: Path = 'config.yaml'
    else:
        conf_file: Path = absolutize('.config/start-mining/config.yaml')
    run(conf_file)


if __name__ == '__main__':
    main()
