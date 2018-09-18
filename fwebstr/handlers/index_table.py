#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging
from commons import common
from handler import RequestHandler

class ReadTableHandler(RequestHandler):

	def get(self):
		self.render('table.html');
