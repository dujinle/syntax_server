#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web
from commons.handler import RequestHandler
from commons.logger import logging

class IndexHandler(RequestHandler):

	def get(self):
		self.render('index.html');
