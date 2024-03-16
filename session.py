import logging
import serial
import time

import handler


def clear_echo(connection):
    while connection.is_open:
        if connection.in_waiting:
            connection.readline()
            return
        time.sleep(0.01)


def send_command(connection, command):
    connection.reset_output_buffer()
    connection.reset_input_buffer()
    connection.write((f"\r{command}\r").encode())
    connection.flush()
    clear_echo(connection)


def command_loop(connection):
    if connection.is_open:
        timing = time.time()
        command = "demod antenna"
        send_command(connection, command)

    while connection.is_open:
        try:
            connection.read_until(b"\n")
            if connection.in_waiting:
                if ((time.time() - timing) > 5):
                    timing = time.time()
                    raw = connection.read_until(b"\r").decode().strip()
                    output = handler.output(raw)
                    logging.debug(f"[v] Response: {raw}")
                    logging.debug(f"[v] Parsed values: {output}")
            time.sleep(0.1)

        except serial.SerialException as error:
            logging.critical(f"[x] SerialException: {error}", exc_info=True)
        except Exception as error:
            logging.critical(f"[x] Exception: {error}", exc_info=True)
