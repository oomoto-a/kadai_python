# -*- coding: utf-8 -*-
class HttpStatusRakutenException(Exception):
    """
    httpステータスの例外
    """
    def __init__(self):
        pass

    def set_param(self, http_status, error_message):
        self.http_status = http_status
        self.error_message = error_message

    def __str__(self):
        return "httpステータス : {}, メッセージ : {}".format(self.http_status, self.error_message)