#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2
# @Author  : CrissChan
# @Site    : https://blog.csdn.net/crisschan
# @File    : swagger2json.py
# @Porject: 在线的swagger（V2）的api文档的内容保存成离线的json格式文件
import requests
import json
import re
from os import path
import os
import errno
from enum import Enum
import shutil

class TYPE(Enum):
    # new 新建，第一次使用
    # rewrite = 覆盖
    NEW = 1
    RENEW = 2
class Swagger2Json(object):

    def __init__(self, url, out_path,type=Type.new):
        '''
            url ： swagger 的json路径，类似v2/api-docs
            out_path：输出路径
            type ： Type枚举类型
        '''
        self.url = url
        self.out_path = out_path
        if type == TYPE.NEW:
            self.__new_json_files()
        elif type == TYPE.RENEW:
            self.__rewrite_jsonfile()
    def __make_dir(self, dir_path=None):
        '''
            新建目录
        '''
        if dir_path is None:
            dir_path = self.out_path
        if not path.exists(dir_path):
            try:
                os.mkdir(dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def __new_json_files(self):
        '''
            存储全部swagger的json到一个swagger.json文件，并调用单接口的json文件保存接口
        '''
        if self.__get_swagger_res():
            # save swagger information by json file and save the out_path root path
            self.__make_dir()
            with open(path.join(self.out_path, 'cri.json'), 'w', encoding='utf-8') as f:
                json.dump(self.res_json, f, ensure_ascii=False)
            self.__get_api_json()

    def __get_api_json(self):
        '''
            保存controller下的api的json到文件，并按照controller结构存储
        '''
        api_path = path.join(self.out_path, 'api')
        self.__make_dir(api_path)
        tags = self.res_json['tags']  # tags save all controller name
        for tag in tags:
            tag_name = tag['name']
            tag_dir = path.join(api_path, tag_name)
            self.__make_dir(tag_dir)

            apis = self.res_json['paths']  # tags save all api uri
            for api in apis:
                if tag_name in json.dumps(apis[api], ensure_ascii=False):
                    api_file = path.join(tag_dir, api.replace('/', '_') + '.json')
                    with open(api_file, 'w', encoding='utf-8') as f:
                        json.dump(apis[api], f, ensure_ascii=False)

    def __get_swagger_res(self):
        '''
            将swagger的json存储在memery中
        '''
        is_uri = re.search(r'https?:/{2}\w.+$', self.url)
        if is_uri:
            try:
                res_swagger = requests.get(self.url)
            except:
                raise Exception('[ERROR]  Some error about {}'.format(self.url))
            if res_swagger.status_code == 200:
                try:
                    self.res_json = res_swagger.json()
                except:
                    res_swagger_text = re.sub('<[^<]+?>', '',  res_swagger.text).replace('\n', '').strip()

                    self.res_json = json.loads(res_swagger_text)
                if self.res_json['swagger'] == '2.0':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __rewrite_jsonfile(self):
        '''
           覆盖，清空后重新生成
        '''
        shutil.rmtree(self.out_path, ignore_errors=True)
        self.__new_json_files()
