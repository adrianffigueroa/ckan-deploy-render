from ckan.plugins import SingletonPlugin, implements, IConfigurer, ITemplateHelpers
from ckan.logic import get_action
from ckan.common import c

class MiTemaPlugin(SingletonPlugin):
    implements(IConfigurer)
    implements(ITemplateHelpers)

    def update_config(self, config):
        from ckan.common import config as ckan_config
        import ckan.plugins.toolkit as toolkit

        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'mitema')


    def get_helpers(self):
        return {
            'get_action': get_action,
            'get_user_name': lambda: c.user,
        }
