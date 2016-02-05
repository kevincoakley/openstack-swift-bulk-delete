#!/usr/bin/env python


class Auth:

    def __init__(self, auth_url, auth_project, auth_user, auth_pass):
        self.auth_url = auth_url
        self.auth_project = auth_project
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.auth_token = None
        self.storage_url = None
