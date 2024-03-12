# Import gettext module
import gettext
import os


def get_locales_abs_path():
    absolute_path = os.path.dirname(__file__)
    return  os.path.join(absolute_path, "locales") #full_path


def get_translator(language="en"):

    # Set the local directory
    appname = 'becalib'


    language_i18n = gettext.translation(appname, get_locales_abs_path(), fallback=True, languages=[language])

    language_i18n.install()
    _=language_i18n.gettext

    return _