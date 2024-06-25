#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cspell:ignore reuseaddr

"""
    Simple echo socket-based server. Supports only IPv4 protocol.
    For configuration - see cmd line options.

    Warning! This script should be fixed for Windows/GitBash environment -
             the socket blocks on the socket.accept() call and process the
             KeyboardInterrupt only after receiving any data.

    Created:  Dmitrii Gusev, 21.06.2024
    Modified: Dmitrii Gusev, 25.06.2024
"""

import datetime
import socket

from argparse import ArgumentParser

# Useful constants
DEFAULT_ENCODING = 'utf-8'
BLOCK_SIZE = 8192  # Block size is set to 8192 because thats usually the max header size


def serve(server_host='0.0.0.0', server_port=3246, server_verbosity=1):
    """ Method that performs the main duty. """

    try:

        # create socket to serve the requests
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_host, server_port))
        sock.listen(1)

        # set socket to non-blocking mode (return immediately/by timeout if no data)
        # sock.setblocking(True)
        # set timeout in seconds
        # sock.settimeout(1)

        # setup verbosity level
        if server_verbosity > 0:
            print(f"Echoing from http://{server_host}:{server_port}")

        while True:
            # print('1')
            # connection = None
            # client_address = None
            # try:
            #     connection, client_address = sock.accept()
            # except TimeoutError as e:
            #     print('->', e.__context__)
            # # print('2')

            connection, client_address = sock.accept()

            request = {}
            bytes_left = BLOCK_SIZE

            # data receiving cycle
            while bytes_left > 0:
                if bytes_left > BLOCK_SIZE:
                    data = connection.recv(BLOCK_SIZE)
                else:
                    data = connection.recv(max(0, bytes_left))

                if not 'header' in request:
                    request = build_request(data)
                    header_length = len(request['raw']) - len(request['body'])
                    body_length_read = BLOCK_SIZE - header_length
                    if 'content-length' in request['header']:
                        bytes_left = int(request['header']['content-length']) - body_length_read
                    else:
                        bytes_left = 0
                else:
                    request['raw'] += data
                    request['body'] += data.decode(DEFAULT_ENCODING, 'ignore')
                    bytes_left -= BLOCK_SIZE

            # request timestamp
            request_time = datetime.datetime.now().ctime()

            # print to the current console tech info about the request
            if server_verbosity > 0:
                print(' - '.join([client_address[0], request_time, request['header']['request-line']]))

            # build the response to the client
            raw_decoded = request['raw'].decode(DEFAULT_ENCODING, 'ignore')
            response = "HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\n\n{}".format(raw_decoded)

            # in case of the MAX verbosity - print response to the current console
            if server_verbosity == 2:
                print("-" * 10)
                print(response)
                print("-" * 40)

            # send response to the client
            connection.sendall(response.encode())

            # close the current socket connection
            connection.close()

    except KeyboardInterrupt:  # server was interrupted by Ctrl-C combination
        print("\nExiting - keyboard interrupt...")

    finally:  # close socket after keyboard interruption
        sock.close()


def do_serve():
    """ Main method pf the script. """

    # get parsed args
    args = parse_args()

    # start serving requests - start server
    serve(args.bind, args.port, get_verbosity(args.verbose, args.quiet))


def build_request(first_chunk):
    """ Building request object from received data. """

    lines = first_chunk.decode(DEFAULT_ENCODING, 'ignore').split('\r\n')
    h = {'request-line': lines[0]}
    i = 1
    while i < len(lines[1:]) and lines[i] != '':
        k, v = lines[i].split(': ')
        h.update({k.lower(): v})
        i += 1
    r = {
        "header": h,
        "raw": first_chunk,
        "body": lines[-1]
    }
    return r


def get_verbosity(verbose, quiet):
    """ Building verbosity level. """

    if quiet:  # quiet mode - overrides verbose
        return 0
    if verbose:  # max verbosity level
        return 2
    return 1  # default level of verbosity


def parse_args():
    """ Parsing cmd line arguments and  """

    # configure cmd line arguments parser
    parser = ArgumentParser(description="Server that returns any http request made to it")
    parser.add_argument('-b', '--bind', default='localhost', help='host to bind to')
    parser.add_argument('-p', '--port', default=3246, type=int, help='port to listen on')
    parser.add_argument('-v', '--verbose', action='store_true', help='print all requests to terminal')
    parser.add_argument('-q', '--quiet', action='store_true', help='silence all output (overrides --verbose)')

    # parse cmd line arguments and return parsed
    return parser.parse_args()


if __name__ == '__main__':
    do_serve()
