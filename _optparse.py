from optparse import OptionParser

class ArgumentParser(OptionParser):
    
    """A thin wrapper around OptionParser implementing the relevant parts of
    the ArgumentParser API. Designed to ensure compatibility with
    Python 3.0-3.1."""
    
    def add_argument(self, *args, **kwargs):
        return Option.add_option(self, *args, **kwargs)
    
    def parse_args(self, args=None, values=None):
        return OptionParser.parse_args(self, args, values)[0]
