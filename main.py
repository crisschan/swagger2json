#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2
# @Author  : CrissChan
# @Site    : https://blog.csdn.net/crisschan
# @File    : swagger2json.py
# @Porject:

from swagger2json import Swagger2Json
from swagger2json import Type
import datetime
if __name__ == '__main__':
    ciscp_uri = 'XXXXXX/v2/api-docs'
    out_path = './out/'
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    out_path = out_path + '/' + filename + '/'
    sw = Swagger2Json(ciscp_uri, out_path, type=Type.new)

