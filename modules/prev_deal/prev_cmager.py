#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from prev_rminvalid import RmInvalidChar
from prev_mknum import MkNumChar

base_path = os.path.dirname(__file__);
#数据预处理阶段，处理特殊字符，！。，？或者不常见的字符文本字符
class PrevMager:
	def __init__(self):
		self.tag_objs = list();

		self.dfiles = [
			os.path.join(base_path,'tdata','rm_invalid_char.json'),
			os.path.join(base_path,'tdata','mk_num_char.json')
		]
		# mark tag objs #
		self.tag_objs.append(RmInvalidChar());
		self.tag_objs.append(MkNumChar());

	def init(self,dtype):
		try:
			for i,obj in enumerate(self.tag_objs):
				obj.load_data(self.dfiles[i]);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e: raise e;
