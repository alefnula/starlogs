__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '31 July 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import logging
# tornado imports
from tornado import ioloop, web
# tea imports
from tea.logger import configure_logging
# board imports
from starlogs.settings import Settings


logger = logging.getLogger(__name__)


class BaseHandler(web.RequestHandler):
    def initialize(self, ss):
        self.ss = ss

    def render(self, template, **kwargs):
        kwargs['ss'] = self.ss
        return super(BaseHandler, self).render(template, **kwargs)


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html', repos=self.ss.repos)


class RepoHandler(BaseHandler):
    def get(self, repo_id):
        for repo in self.ss.repos:
            if repo['id'] == repo_id:
                return self.render('repo.html', repo=repo)
        return self.redirect('%s/' % self.ss.root)


class ConfigHandler(BaseHandler):
    def get(self):
        return self.render('config.html', repos=self.ss.repos)

    def post(self):
        action = self.get_argument('action')
        if action == 'delete':
            repo_id = self.get_argument('id', '').strip()
            self.ss.del_repo(repo_id)
        else:
            repo_id = self.get_argument('id', '').strip()
            desc = self.get_argument('desc', '').strip()
            url = self.get_argument('url', '').strip()
            self.ss.add_repo(repo_id, desc, url)
        self.redirect('%s/_config/' % self.ss.root)


class Application(web.Application):
    def __init__(self, ss, debug):
        settings = {
            'debug'             : debug,
            'static_path'       : ss.paths['static'],
            'static_url_prefix' : '%s/static/' % ss.root,
            'template_path'     : ss.paths['templates']
        }
        super(Application, self).__init__([
            (r'%s/'         % ss.root, IndexHandler,  {'ss': ss}),
            (r'%s/_config/' % ss.root, ConfigHandler, {'ss': ss}),
            (r'%s/([^/]*)/' % ss.root, RepoHandler,   {'ss': ss}),
        ], **settings)


def main(args=None, port=8000, debug=False):
    ss = Settings()
    configure_logging(os.path.join(ss.paths['log'], 'starlogs.log'))
    try:
        application = Application(ss, debug)
        # Start Web Server
        application.listen(port)
        ioloop.IOLoop.instance().start()
    except:
        logger.exception('Board crashed')
