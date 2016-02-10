#!/usr/bin/env python

import time
import logging
import requests
import threading
import variables
import arguments
from swiftbulkdelete.auth.swauth import Swauth
from swiftbulkdelete.swift import Swift


def main():

    args = arguments.parse_arguments()

    if args["debug"] is True:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        logging.getLogger("requests").setLevel(logging.WARNING)

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        handlers=[logging.StreamHandler()])

    logging.debug("container: %s, limit: %s, threads: %s",
                  args["container"], args["limit"], args["threads"])

    try:
        threads = []

        for i in range(int(args["threads"])):
            t = threading.Thread(target=worker, args=(args["container"], args["limit"], i,))
            t.daemon = True
            threads.append(t)
            t.start()
            time.sleep(1)

        while True:
            pass
    except KeyboardInterrupt:
        return


def worker(container, limit, thread_num):

    count = 0

    try:
        while True:

            if count % 20 is 0:
                auth = Swauth(variables.os_auth_url, variables.os_tenant_name,
                              variables.os_username, variables.os_password)
                auth.get_auth_token()

            swift = Swift(auth.auth_token, auth.storage_url, container, limit, thread_num)

            response = swift.bulk_delete_objects()

            print "(%s) %s" % (thread_num, response)

            if swift.status_code != requests.codes.ok:
                print "(%s) (%s) Thread Exited" % (swift.status_code, thread_num)
                return

            if "400 Bad Request" in response:
                print "(%s) (400 Bad Request) Thread Exited" % thread_num
                return

            count += 1
    except KeyboardInterrupt:
        return

    return
