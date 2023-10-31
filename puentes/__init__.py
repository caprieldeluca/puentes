# -*- coding: utf-8 -*-
__copyright__ = '(C) 2023 by Gabriel De Luca'
__email__ = 'caprieldeluca@gmail.com'
__license__ = 'GPL version 3'

def classFactory(iface):
    """Factory method for the plugin object."""
    from .plugin import Puentes
    return Puentes(iface)
