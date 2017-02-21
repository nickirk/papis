
from ..document import Paper

def init(subparsers):
    """TODO: Docstring for init.

    :subparser: TODO
    :returns: TODO

    """
    config_parser = subparsers.add_parser("config",
            help="Manage the configuration options")

    config_parser.add_argument("option",
            help="Set or get option",
            default="",
            nargs="*",
            action="store"
            )


def main(config, args):
    """
    Main action if the command is triggered

    :config: User configuration
    :args: CLI user arguments
    :returns: TODO

    """
    papersDir = os.path.expanduser(config[args.lib]["dir"])
    printv("Using directory %s"%papersDir)
    # FIXME: Replacing values does not work
    option = " ".join(args.option)
    printv(option)
    value = False
    m = re.match(r"([^ ]*)\.(.*)", option)
    if not m:
        raise Exception("Syntax for option %s not recognised"%option)
    lib    = m.group(1)
    preKey = m.group(2)
    m = re.match(r"(.*)\s*=\s*(.*)", preKey)
    if m:
        key = m.group(1)
        value = m.group(2)
    else:
        key = preKey
    printv("lib -> %s" % lib)
    printv("key -> %s" % key)
    if not value:
        print(config[lib][key])
    else:
        try:
            config.remove_option(lib,key)
            config.set(lib, key, value)
        except configparser.NoSectionError:
            config.add_section(lib)
            config.set(lib, key, value)
        config.save()