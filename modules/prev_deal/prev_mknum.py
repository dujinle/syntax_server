#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common,collections
from pdeal_base import PDealBase

#汉字数字转换
class MkNumChar(PDealBase):

	def encode(self,struct):
		try:
			self.match_item(struct);
			self.sort_num_label(struct);
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

	def sort_num_label(self,struct):
		num_list = list();
		
		while True:
			tmp_text = struct['text'];
			prev_id = -1;
			prev_num = None;
			if len(struct['SomeNum']) <= 0: break;
			for key in struct['SomeNum'].keys():
				tid = tmp_text.find(key);
				if tid >= prev_id:
					item = struct['SomeNum'][key]
					prev_num = key;
					prev_id = tid;
					tmp_text = tmp_text.replace(item['value'],item['label'],1);
			if not prev_num is None:
				num_list.append(struct['SomeNum'][prev_num]);
				del struct['SomeNum'][prev_num];
		num_list.reverse();
		tdic = collections.OrderedDict();
		for item in num_list:
			tdic[item['value']] = item;
		struct['SomeNum'] = tdic;
