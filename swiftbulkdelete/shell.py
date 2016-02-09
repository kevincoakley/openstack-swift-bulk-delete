#!/usr/bin/env python

import variables
import arguments
from swiftbulkdelete.auth.swauth import Swauth
from swiftbulkdelete.swift import Swift


def main():

    args = arguments.parse_arguments()

    auth = Swauth(variables.os_auth_url, variables.os_tenant_name, variables.os_username,
                  variables.os_password)
    auth.get_auth_token()

    swift = Swift(auth.auth_token, auth.storage_url, args["container"], args["limit"],
                  args["offset_multiplier"])

    swift.bulk_delete_objects()
