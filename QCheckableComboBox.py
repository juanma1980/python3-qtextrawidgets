from PySide2.QtWidgets import QComboBox
from PySide2.QtGui import QStandardItemModel
from PySide2.QtCore import Qt,Signal

class QCheckableComboBox(QComboBox):
	clicked=Signal()
	closed=Signal()
	def __init__(self,*args,**kwargs):
		parent = kwargs.get('parent')
		if not parent:
			for i in args:
				if isinstance(i,QWidget):
					parent = i
		super().__init__(*args,**kwargs)
		self.view().pressed.connect(self._checked)
		self.setModel(QStandardItemModel(self))
		self.checked=False
		self.addItem("")
	#def __init__

	def _checked(self, index):
		self.checked=True
		if index.row()==0:
			return
		item = self.model().itemFromIndex(index)
		if item.checkState() == Qt.Checked:
			item.setCheckState(Qt.Unchecked)
		else:
			item.setCheckState(Qt.Checked)
		self.clicked.emit()
		return(False)
	#def _checked

	def setText(self,text):
		if self.count()==0:
			self.addItem("")
		item=self.model().item(0)
		item.setText(text)
	#def setText

	def hidePopup(self,*args,close=False):
		self.setCurrentIndex(0)
		if close==False and self.checked==True:
			self.checked=False
			self.closed.emit()
			return close
		super().hidePopup()
	#def hidePopup

	def addItem(self,*args,state=True):
		super().addItem(args[0])
		item=self.model().item(self.count()-1)
		if self.count()>1:
			if state==True:
				item.setCheckState(Qt.Checked)
			else:
				item.setCheckState(Qt.Unchecked)
	#	rect=self.view().sizeHint()
	#	Xpos=0
	#	Ypos=rect.height()
	#	self.btn.move(Xpos,Ypos)
	#def addItem

	def getItems(self,*args):
		items=[]
		for i in range(0,self.count()):
			item=self.model().item(i)
			items.append(item)
		return(items)
	#def getItems

	def setState(self,idx,state):
		item=self.model().item(idx)
		if state==True:
			item.setCheckState(Qt.Checked)
		else:
			item.setCheckState(Qt.Unchecked)
	#def setState
#class QCheckableComboBox
