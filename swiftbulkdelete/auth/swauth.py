#!/usr/bin/env python

import requests
from swiftbulkdelete.auth.auth import Auth
from swiftbulkdelete.exceptions import AuthException


class Swauth(Auth):

    def __init__(self, auth_url, auth_project, auth_user, auth_pass):
        Auth.__init__(self, auth_url, auth_project, auth_user, auth_pass)

    def get_auth_token(self):

        headers = {"X-Auth-User": "%s:%s" % (self.auth_project, self.auth_user),
                   "X-Auth-Key": self.auth_pass}

        r = requests.get(self.auth_url, headers=headers)

        if r.status_code == requests.codes.ok:
            self.auth_token = r.headers["x-auth-token"]

            if "storage" in r.json():
                if "local" in r.json()["storage"]:
                    self.storage_url = r.json()["storage"]["local"]
                else:
                    raise AuthException("Auth Failed (Missing Storage Location): %s" % r.json())
            else:
                raise AuthException("Auth Failed (Missing Storage Location): %s" % r.json())

        else:
            raise AuthException("Auth Failed (%s): %s" % (r.status_code, r.headers))
