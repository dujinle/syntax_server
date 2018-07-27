#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common,collections
from pdeal_base import PDealBase

#汉字数字转换
class MkNumChar(PDealBase):

	def encode(self,struct):
		try:
			self.match_item(struct);
		except Exception as e: raise e;

	def match_item(self,struct):
		try:
			if not struct.has_key("SomeNum"):
				struct['SomeNum'] = collections.OrderedDict();
			for key in self.data:
				item = self.data[key];
				comp = re.compile(item['reg']);
				match = comp.findall(struct['text']);
				for im in match:
					tdic = dict();
					tdic['label'] = "D";
					tdic['value'] = im;
					tdic['type'] = "NUM";
					struct['SomeNum'][im] = tdic;
		except Exception as e: raise e;