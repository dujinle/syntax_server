#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from scene_base import SceneBase

#处理音乐场景
class MusicData(SceneBase):

	#获取音乐 根据人名
	def get_favorite(self,owner):
		if self.data.has_key(owner):
			return self.data[owner];
		return None;
