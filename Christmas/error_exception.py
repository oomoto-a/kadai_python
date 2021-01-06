# -*- coding: utf-8 -*-

class CausaInfoScrapingException(Exception):
    """
    案件情報スクレイピングの例外
    causa　info Scraping
    """
    def __init__(self):
        pass

    def set_param(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return "メッセージ : {}".format(self.error_message)