#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
from time_base import TimeBase
#标记对象以及链接的网络
class TimeParse(TimeBase):

	def encode(self,struct):
		try:
			if not struct.has_key('TimeLamda'):
				return False;
			self.parse_time_lamda(struct);
		except Exception as e: raise e;

	def parse_time_lamda(self,struct):
		try:
			for item in struct['TimeLamda']:
				if item['label'] == 'TimeN':
					if self.data.has_key(item['type']):
						mdata = self.data[item['type']];
						for idata in mdata:
							p = re.compile(idata['reg']);
							amatch = p.search(item['str']);
							if amatch is None: continue;
							self.match_timen(idata,item);
		except Exception as e: raise e;

	def match_timen(self,idata,item):
		print idata,item;