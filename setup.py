# This script was automatically generated by distutils2
import codecs
from distutils.core import setup
try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser


def split_multiline(value):
    """Split a multiline string into a list, excluding blank lines."""

    return [element for element in
            (line.strip() for line in value.split('\n'))
            if element]


def cfg_to_args(path='setup.cfg'):
    """Compatibility helper to use setup.cfg in setup.py.

    This functions uses an existing setup.cfg to generate a dictionnary of
    keywords that can be used by distutils.core.setup(**kwargs).  It is used
    by generate_setup_py.

    *file* is the path to the setup.cfg file.  If it doesn't exist,
    PackagingFileError is raised.
    """

    # XXX ** == needs testing
    D1_D2_SETUP_ARGS = {"name": ("metadata",),
                        "version": ("metadata",),
                        "author": ("metadata",),
                        "author_email": ("metadata",),
                        "maintainer": ("metadata",),
                        "maintainer_email": ("metadata",),
                        "url": ("metadata", "home_page"),
                        "description": ("metadata", "summary"),
                        "long_description": ("metadata", "description"),
                        "download-url": ("metadata",),
                        "classifiers": ("metadata", "classifier"),
                        "platforms": ("metadata", "platform"),  # **
                        "license": ("metadata",),
                        "requires": ("metadata", "requires_dist"),
                        "provides": ("metadata", "provides_dist"),  # **
                        "obsoletes": ("metadata", "obsoletes_dist"),  # **
                        "package_dir": ("files", 'packages_root'),
                        "packages": ("files",),
                        "scripts": ("files",),
                        "py_modules": ("files", "modules"),  # **
                        }

    MULTI_FIELDS = ("classifiers",
                    "platforms",
                    "requires",
                    "provides",
                    "obsoletes",
                    "packages",
                    "scripts",
                    "py_modules")

    def has_get_option(config, section, option):
        if config.has_option(section, option):
            return config.get(section, option)
        elif config.has_option(section, option.replace('_', '-')):
            return config.get(section, option.replace('_', '-'))
        else:
            return False

    # The real code starts here
    config = RawConfigParser()
    f = codecs.open(path, encoding='utf-8')
    try:
        config.readfp(f)
    finally:
        f.close()

    kwargs = {}
    for arg in D1_D2_SETUP_ARGS:
        if len(D1_D2_SETUP_ARGS[arg]) == 2:
            # The distutils field name is different than distutils2's
            section, option = D1_D2_SETUP_ARGS[arg]

        else:
            # The distutils field name is the same thant distutils2's
            section = D1_D2_SETUP_ARGS[arg][0]
            option = arg

        in_cfg_value = has_get_option(config, section, option)
        if not in_cfg_value:
            # There is no such option in the setup.cfg
            if arg == 'long_description':
                filenames = has_get_option(config, section, 'description-file')
                if filenames:
                    filenames = split_multiline(filenames)
                    in_cfg_value = []
                    for filename in filenames:
                        fp = codecs.open(filename, encoding='utf-8')
                        try:
                            in_cfg_value.append(fp.read())
                        finally:
                            fp.close()
                    in_cfg_value = '\n\n'.join(in_cfg_value)
            else:
                continue

        if arg == 'package_dir' and in_cfg_value:
            in_cfg_value = {'': in_cfg_value}

        if arg in MULTI_FIELDS:
            # support multiline options
            # Map to str values as workaround for
            #     http://bugs.python.org/issue13943 and similar
            in_cfg_value = map(str, split_multiline(in_cfg_value))
            print arg, in_cfg_value

        kwargs[arg] = in_cfg_value

    return kwargs

print(cfg_to_args())
setup(**cfg_to_args())
