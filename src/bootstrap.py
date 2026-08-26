import signal
import sys

from .application import Application
from .config import get_config


# Entry point for bootstrapping the application
def bootstrap():
    config = get_config()

    app = Application(config)

    def shutdown(signum, frame):
        print(f"Received signal {signum}")

        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        app.start()
    except Exception as error:
        print(f"Application failed to start: {error}")
        app.stop()
        raise