#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys,common
from time_label import TimeLabel
from time_lamda import TimeLamda
from time_parse import TimeParse
class TimeMager():
	def __init__(self):

		base_path = os.path.dirname(__file__);
		self.dfiles = [
			os.path.join(base_path,'tdata','time_label.json'),
			os.path.join(base_path,'tdata','time_lamda.json'),
			os.path.join(base_path,'tdata','timen_seq.json')
		]
		self.tag_objs = list();
		self.tag_objs.append(TimeLabel());
		self.tag_objs.append(TimeLamda());
		self.tag_objs.append(TimeParse());

	def init(self):
		try:
			for i,obj in enumerate(self.tag_objs):
				obj.load_data(self.dfiles[i]);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e: raise e;
