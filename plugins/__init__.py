from glob import glob
from keyword import iskeyword
from os.path import dirname, join, split, splitext

basedir = dirname(__file__)

for name in glob(join(basedir, '*.py')):
    module = splitext(split(name)[-1])[0]
    if not module.startswith('_') and \
            module.isidentifier() and \
            not iskeyword(module):
        __import__(__name__ + '.' + module)
