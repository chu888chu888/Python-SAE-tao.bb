#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 ft=python
import inspect
import sae.kvdb
class SAEKVDBPlugin(object):
    name = 'saekvdb'
    
    def __init__(self, keyword='kv'):
            self.keyword = keyword

    def setup(self, app):
            ''' Make sure that other installed plugins don't affect the same
                keyword argument.'''
            for other in app.plugins:
                if not isinstance(other, SQLitePlugin): continue
                if other.keyword == self.keyword:
                     raise PluginError("Found another savekvdb plugin with "\
                     "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        conf = context['config'].get('saekvdb') or {}
        keyword = conf.get('keyword', self.keyword)
        args = inspect.getargspec(context['callback'])[0]

        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kv = sae.kvdb.KVClient()

            kwargs[self.keyword] = kv
            rv = callback(*args, **kwargs)
            return rv

        return wrapper
Plugin = SAEKVDBPlugin
