# -*- coding: utf-8 -*-
import sys 
import os 

def resource_path(relative_path):
    """"
    パス検索
    """
    try:
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.dirname(__file__)
        print(base_path)
    return os.path.join(base_path, relative_path)
