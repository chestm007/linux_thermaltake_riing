import os
import time


tag = os.environ.get('CIRCLE_TAG')
if tag:
    print(tag)
else:
    last_tag = os.popen('git describe --abbrev=0 --tags').read().strip()
    cur_epoch = int(time.time())
    cur_branch = os.environ.get('CIRCLE_BRANCH')
    print('{}-{}.post{}'.format(last_tag, cur_branch, cur_epoch))
