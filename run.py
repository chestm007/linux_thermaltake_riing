import logging
import sys

from linux_thermaltake_rgb import DEBUG
from linux_thermaltake_rgb.daemon.daemon import ThermaltakeDaemon


def main():
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,  # if DEBUG else logging.INFO,
                        format='%(message)s')

    daemon = ThermaltakeDaemon()
    try:
        daemon.run()
    except KeyboardInterrupt:
        daemon.stop()


if __name__ == '__main__':
    main()
