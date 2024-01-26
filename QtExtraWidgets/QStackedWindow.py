#!/usr/bin/env python3
import sys
import os
import importlib
import inspect
import time
import traceback
from PySide2.QtWidgets import QLabel, QWidget, QGridLayout,QListWidget,QListWidgetItem,QStackedWidget
from PySide2 import QtGui
from PySide2.QtCore import Qt,Signal
import gettext
try:
	confText=gettext.translation("python3-appconfig")
	_ = confText.gettext
except:
	gettext.textdomain('python3-appconfig')
	_ = gettext.gettext

QString=type("")
QInt=type(0)

class QStackedWindow(QWidget):
	pending=Signal()
	def __init__(self,*args,**kwargs):
		parent=kwargs.get("parent")
		if parent==None:
			for i in args:
				if isinstance(i,QWidget):
					parent=i
		super(QStackedWindow,self).__init__(parent)
		self.dbg=False
		self.current=-1
		self.referer=-1
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.lblBanner=QLabel()
		self.lstNav=QListWidget()
		self.stkPan=QStackedWidget()
		self.curStack=None
		self._renderGui()
	#def init
	
	def _debug(self,msg):
		if self.dbg:
			print("StackedWindow: {}".format(msg))
	#def _debug

	def _renderGui(self):
		lay=QGridLayout()
		lay.addWidget(self.lblBanner,0,0,1,2,Qt.AlignCenter)
		lay.addWidget(self.lstNav,1,0,1,1)
		self.lstNav.activated.connect(self.setCurrentStack)
		self.lstNav.itemClicked.connect(self.setCurrentStack)
		lay.addWidget(self.stkPan,1,1,1,1)
		lay.setColumnStretch(1,1)
		self.setLayout(lay)
	#def _renderGui

	def getCurrentStackIndex(self):
		return(self.current)
	#def getCurrentStack

	def getCurrentStack(self):
		return(self.stkPan.currentWidget())
	#def getCurrentStack
	
	def _getRowForIdx(self,idx):
		row=0
		for cont in range(0,self.lstNav.count()):
			w=self.lstNav.item(cont)
			if w.data(1)==idx:
				row=cont
				break
		return(row)

	def _endSetCurrentStack(self,idx,oldcursor,parms=None):
		if self.curStack!=None:
			lay=self.layout()
		self.referer=self.current
		if idx<0:
			idx=self.lstNav.currentRow()
		else:
			idx=self._getRowForIdx(idx)
		self.lstNav.setCurrentRow(idx)
		self.current=idx
		self.stkPan.setCurrentIndex(self.current)
		self.curStack=self.getCurrentStack()
		if parms!=None:
			self.curStack.setParms(parms)
			self.curStack.updateScreen()
		self.setCursor(oldcursor)
	#def _endSave

	def setCurrentStack(self,*args,**kwargs):
		oldcursor=self.cursor()
		cursor=QtGui.QCursor(Qt.WaitCursor)
		self.setCursor(cursor)
		parms=kwargs.get("parms",None)
		idx=kwargs.get("idx",-1)
		if idx<0:
			for arg in args:
				if isinstance(arg,int):
					idx=arg
					break
		widget=self.stkPan.currentWidget()
		if hasattr(widget,"btnAccept"):
			if widget.btnAccept.isEnabled()==True:
				if hasattr(widget,"dlgPendingChanges"):
					cont=widget.dlgPendingChanges()
					if cont<0:
						self.lstNav.setCurrentRow(self.current)
						self.setCursor(oldcursor)
						return
					elif cont==0:
						widget.btnAccept.clicked.emit()
						widget.updated.connect(lambda: self._endSetCurrentStack(idx,oldcursor,parms))
						return
		self._endSetCurrentStack(idx,oldcursor,parms)
	#def setCurrentStack

	def setIcon(self,ficon):
		self._debug("Icon: {}".format(icon))
		if os.path.isfile(ficon):
			icon=QtGui.QIcon(ficon)
		else:
			icon=QtGui.QIcon.fromTheme(icon)
		self.setWindowIcon(icn)
	#def setIcon

	def setBanner(self,banner):
		if not os.path.isfile(banner):
			if os.path.isfile(os.path.join(self.rsrc,banner)):
				banner=os.path.join(self.rsrc,banner)
			else:
				banner=""
				self._debug("Banner not found at {}".format(self.rsrc))
		self.lblBanner.setPixmap(banner)
	#def setBanner

	def addStack(self,stack,**kwargs):
		callback=kwargs.get("callback",stack.__initScreen__)
		props=stack.getProps()
		icon=QtGui.QIcon.fromTheme(props.get("icon"))
		self.stkPan.insertWidget(props.get("index"),stack)
		item=QListWidgetItem(icon,props.get("shortDesc"))
		item.setToolTip(props.get("tooltip"))
		idx=props.get("index")
		item.setData(1,idx)
		item.setIcon(icon)
		self.lstNav.insertItem(idx,item)
		if props.get("visible",True)==False:
			item.setHidden(True)
		callback()
	#def addStack(self,stack,**kwargs):
	
	def _importModuleFromFile(self,fmodule):
		module=None
		if fmodule.endswith(".py") and os.path.basename(fmodule)!='__init__.py':
			module=fmodule.replace(".py","").replace("/",".")
			try:
				spec = importlib.util.spec_from_file_location(module,fmodule )
				module = importlib.util.module_from_spec(spec)
			except Exception as e:
				self._debug("Unable to load {0} (perhaps aux lib): {1}".format(module,str(e)))
				module=None
				traceback.print_exc()
			try:
				spec.loader.exec_module(module)
			except Exception as e:
				print("ERROR on {}: {}".format(module,e))
				module=None
				traceback.print_exc()
		return(module)
	#def _importModuleFromFile

	def _getClassFromMod(self,module):
		moduleClass=None
		for includedClass in inspect.getmembers(module, predicate=inspect.isclass):
			name,obj=(includedClass)
			if name.lower()==module.__name__.split(".")[-1].lower():
				test=includedClass[1]
				try:
					moduleClass=test(parent=self)
				except Exception as e:
					self._debug("Unable to import {0}: {1}".format(module,str(e)))
					traceback.print_exc()
				else:
					break
		if moduleClass!=None:
			if hasattr(moduleClass,"enabled"):
				if moduleClass.enabled==False:
					moduleClass=None
		return(moduleClass)
	#def _getClassFromMod

	def addStacksFromFolder(self,dpath="stacks"):
		if os.path.isdir(dpath)==False:
			print("addStacksFromFolder: ./{} not found".format(dpath))
			return
		modulesByIndex={}
		for plugin in os.scandir(dpath):
			module=self._importModuleFromFile(plugin.path)
			if module!=None:
				moduleClass=self._getClassFromMod(module)
				if moduleClass!=None:
					props=moduleClass.getProps()
					modulesByIndex[props.get("index",1)]=moduleClass
		for mod in sorted(modulesByIndex.keys()):
			self.addStack(modulesByIndex[mod])
	#def _importStacks(self):
