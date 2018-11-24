import os
import time

last_tag = os.popen('git describe --abbrev=0 --tags').read().strip()
print(os.environ.get('TRAVIS_TAG') or '{}.post{}'.format(last_tag, int(time.time())))
