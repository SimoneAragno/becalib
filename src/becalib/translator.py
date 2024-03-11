# Import gettext module
import gettext

# https://www.labri.fr/perso/fleury/posts/programming/a-quick-gettext-tutorial.html


def get_translator(language="en"):

    # Set the local directory
    appname = 'becalib'
    localedir = './locales'

    language_i18n = gettext.translation(appname, localedir, fallback=True, languages=[language])

    language_i18n.install()
    _=language_i18n.gettext

    return _