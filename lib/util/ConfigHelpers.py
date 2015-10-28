import json
import re

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

def parse_json(filename):
    """ Parse a JSON file
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    with open(filename) as f:
        #content = ''.join(f.readlines())
        content = ''.join(f.readlines()).replace('.,',',').replace('.]',']').replace('.}','}')

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)


        #print content

        # Return json file
        return json.loads(content)
        
        
import ConfigParser
class ConfigParserWrapper(ConfigParser.ConfigParser):
    """
    Loads standard ini configuration into dictionary like other configurations do (json, yaml, xml)
    """
    def load(self, file_object):
        self.readfp(file_object)
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d