#!/usr/bin/env python

import requests
import locale
from swiftbulkdelete.exceptions import SwiftException

locale.setlocale(locale.LC_ALL, 'en_US')


class Swift:

    def __init__(self, auth_token, storage_url, container, limit, offset_multiplier=0):
        self.auth_token = auth_token
        self.storage_url = storage_url
        self.container = container
        self.limit = limit
        self.offset_multiplier = offset_multiplier
        self.object_list = ""

    def list_objects(self, limit, marker=""):
        headers = {"X-Auth-Token": self.auth_token}

        r = requests.get("%s/%s?format=json&limit=%s&marker=%s" %
                         (self.storage_url, self.container, limit, marker), headers=headers)

        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            raise SwiftException("Object List Failed (%s)" % r.status_code)

    def get_object_offset_marker(self, offset):
        offset_object_response_json = self.list_objects(offset)

        if len(offset_object_response_json) > 0:
            if "name" in offset_object_response_json[-1]:
                return offset_object_response_json[-1]["name"].encode('utf-8').strip()
            else:
                raise SwiftException("Name Not In Object List")
        else:
            raise SwiftException("Object List Has 0 Length")

    def get_objects(self):

        if self.offset_multiplier is 0:
            marker = ""
        else:
            marker = self.get_object_offset_marker(self.limit * self.offset_multiplier)

        for swift_object in self.list_objects(self.limit, marker=marker):
            if not swift_object["content_type"] == "application/directory":
                self.object_list += "%s/%s\n" % (self.container,
                                                 swift_object["name"].encode('utf-8').strip())

    def bulk_delete_objects(self):
        headers = {"X-Auth-Token": self.auth_token}

        self.get_objects()

        r = requests.delete("%s/?bulk-delete" % self.storage_url,
                            data=self.object_list,
                            headers=headers)

        if r.status_code == requests.codes.ok:
            return r.content
        else:
            raise SwiftException("Bulk Delete Failed (%s)" % r.status_code)
