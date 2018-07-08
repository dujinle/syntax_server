#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../../modules/timer'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
sys.path.append(os.path.join(base_path,'../../modules/mytag'));
sys.path.append(os.path.join(base_path,'../../modules/prev_deal'));
sys.path.append(os.path.join(base_path,'../pystr'));
#============================================
import common,config
from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from wordseg import WordSeg
from scene_engin import SEngin

def analysis_result(struct,ans):
	for item in ans:
		if not struct['mcks'].has_key(item): return False;
	return True;


wd = WordSeg();
timer = TimeMager();
tag = MytagMager();
pdeal = PDealMager();
se = SEngin();

se.init('../tdata/');
timer.init('Timer');
tag.init('Mytag');
pdeal.init('PDeal');

struct = dict();
struct['result'] = dict();
#read test file
tests = common.read_json('./maddm.json');
#start tests
for test in tests:
	struct['text'] = test['test'];
	struct['inlist'] = wd.tokens(struct['text']);
	pdeal.encode(struct);
	timer.encode(struct);
	tag.encode(struct);
	se.clocks.clear();
	se.encode(struct);
	if analysis_result(struct,test['ans']) == True:
		print test['test'],'succ';
		if test.has_key('print') and test['print'] == 'true': common.print_dic(struct);
	else:
		print test['test'],'faile';
		common.print_dic(struct);
		sys.exit(-1)
