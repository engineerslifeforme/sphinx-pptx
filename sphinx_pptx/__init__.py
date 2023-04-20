__version__ = '0.0.1'
__author__ = ''

from .builders.pptx import PptxBuilder

def setup(app):
    # imports defined inside setup function, so that the __version__ can be loaded,
    # even if Sphinx is not yet installed.
    from sphinx.writers.text import STDINDENT
    
    app.require_sphinx('1.4')
    app.add_builder(PptxBuilder)
    app.add_config_value('presentation_template', None, False)

    return {
        'version': __version__,
        # 'env_version': 1,  # not needed; restbuilder does not store data in the environment
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }