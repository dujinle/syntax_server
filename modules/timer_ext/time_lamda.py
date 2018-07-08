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
			self.creat_lamda(struct);
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
					#struct['lamda_text'] = struct['lamda_text'].replace(amatch.group(),'',1);
			print struct['TimeLamda'];
		except Exception as e: raise e;

	def creat_lamda(self,struct):
		try:
			timelamda = list();
			for lamda in struct['TimeLamda']:
				tmp_lamda = lamda;
				lamda_stc = list();
				index = 7;
				print lamda;
				while True:
					if len(tmp_lamda) == 0:
						print 'finish ok';
						break;
					index = index - 1;
					if index <= 0:
						print 'finish error';
						break;
					for timelabel in struct['TimeLabel']:
						idx = tmp_lamda.find(timelabel['label']);
						if idx == 0:
							tmp_lamda = tmp_lamda.replace(timelabel['label'],'',1);
							lamda_stc.append(timelabel);
							print tmp_lamda;
						else:
							tmp_lamda = lamda;
							lamda_stc = list();
							timelabel = struct['TimeLabel'].pop(0);
							struct['TimeLabel'].append(timelabel);
							break;
				if len(lamda_stc) > 0:
					timelamda.append(lamda_stc);
			struct['TimeLamda'] = timelamda;

		except Exception as e: raise e;
	def prev_label(self,struct):
		struct['lamda_text'] = list();
		timelabel = list();
		for istr in struct['seg_text'].split(' '):
			if len(istr) == 0: continue;
			for item in struct['TimeLabel']:
				if istr == item['str']:
					struct['lamda_text'].append(item['label']);
					timelabel.append(item);
		struct['lamda_text'] = ''.join(struct['lamda_text']);
		struct['TimeLabel'] = timelabel;
