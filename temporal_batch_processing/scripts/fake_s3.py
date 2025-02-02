import signal
import time

from moto.server import ThreadedMotoServer

server = ThreadedMotoServer(port=5050)


def signal_handler(_, __):
    print("\nShutting down the server...")
    server.stop()
    exit(0)


def run():
    server.start()

    # Register the signal handler for CTRL+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        server.stop()


if __name__ == "__main__":
    run()
