__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '31 July 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import io
import os
import json
import logging
from tea import shutil


logger = logging.getLogger(__name__)


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


class Settings:
    def __init__(self):
        # Paths
        self.root = '/starlogs'
        self.paths = {
            'project'   : PROJECT_DIR,
            'log'       : os.path.join(PROJECT_DIR, 'data', 'log'),
            'config'    : os.path.join(PROJECT_DIR, 'data', 'config'),
            'static'    : os.path.join(PROJECT_DIR, 'data', 'static'),
            'templates' : os.path.join(PROJECT_DIR, 'data', 'templates'),
        }
        try:
            with io.open(os.path.join(self.paths['config'], 'repos.json'), 'r', encoding='utf-8') as f:
                self.repos = json.load(f)
        except:
            self.repos = []

    def _save_repos(self):
        if not os.path.isdir(self.paths['config']):
            shutil.mkdir(self.paths['config'])
        with io.open(os.path.join(self.paths['config'], 'repos.json'), 'w+b') as f:
            json.dump(self.repos, f, indent=2, encoding='utf-8')

    def add_repo(self, repo_id, desc, url):
        self.repos.append({'id': repo_id, 'desc': desc, 'url': url})
        self._save_repos()

    def del_repo(self, repo_id):
        for i, repo in enumerate(self.repos):
            if repo_id == repo['id']:
                self.repos.pop(i)
                self._save_repos()
                return
