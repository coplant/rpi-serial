import logging
import serial

import session


def main(port, baud_rate=9600):
    logging.basicConfig(
        format="[%(levelname)s]:%(asctime)s.%(msecs)03d - %(message)s",
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )

    try:
        with serial.Serial(port, baud_rate, timeout=2, rtscts=True) as connection:
            connection.flush()
            session.command_loop(connection)

    except serial.SerialException as error:
        logging.critical(f"[x] Exception: {error}", exc_info=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="A string with COM-port.", type=str, nargs="?", const="/dev/ttyACM0")
    args = parser.parse_args()

    main(port=args.port)
