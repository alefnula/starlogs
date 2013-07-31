import json
from mercurial.hgweb import webcommands, webutil


def web_command(name):
    def decorator(f):
        setattr(webcommands, name, f)
        webcommands.__all__.append(name)
        return f
    return decorator


def json_changelog(web, req):
    l = []
    if 'node' in req.form:
        ctx = webutil.changectx(web.repo, req)
        revs = web.repo.changelog.revs(ctx.rev())
    else:
        revs = web.repo.changelog.revs()
    for i in revs:
        ctx = web.repo[i]
        l.append({
            'author': ctx.user(),
            'desc': ctx.description(),
            'node': ctx.hex(),
            'date': ctx.date()[0],
        })
    return json.dumps(l)


@web_command('json_log')
def jsonlog(web, req, tmpl):
    '''Returns a json formated changelog'''
    req.respond(200, 'application/json')
    return [json_changelog(web, req)]


@web_command('jsonp_log')
def jsonplog(web, req, tmpl):
    '''Returns a json formated changelog'''
    req.respond(200, 'application/json')
    return ['%s(%s)' % (req.form['callback'][0], json_changelog(web, req))]
