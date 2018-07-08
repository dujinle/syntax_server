#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
from time_base import TimeBase
#标记对象以及链接的网络
class TimeLamda(TimeBase):

	def encode(self,struct):
		try:
			struct['TimeLamda'] = list();
			self.prev_label(struct);
			self.find_lamda(struct);
		except Exception as e: raise e;

	def find_lamda(self,struct):
		try:
			for key in self.data.keys():
				item = self.data[key];
				for reg in item.keys():
					p = re.compile(reg);
					amatch = p.search(struct['lamda_text']);
					if amatch is None: continue;
					struct['TimeLamda'].append(amatch.group());
		except Exception as e: raise e;

	def prev_label(self,struct):
		struct['lamda_text'] = list();
		for istr in struct['seg_text'].split(' '):
			if len(istr) == 0: continue;
			for item in struct['TimeLabel']:
				if istr == item['str']:
					struct['lamda_text'].append(item['label']);
		struct['lamda_text'] = ''.join(struct['lamda_text']);
