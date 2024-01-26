from PySide2.QtWidgets import QHBoxLayout,QComboBox,QLineEdit,QPushButton,QWidget
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt,Signal

class QSearchBox(QWidget):
	clicked=Signal()
	editingFinished=Signal()
	returnPressed=Signal()
	textChanged=Signal()
	def __init__(self,*args,**kwargs):
		parent = kwargs.get('parent')
		if not parent:
			for i in args:
				if isinstance(i,QWidget):
					parent = i
		super().__init__(*args,**kwargs)
		lay=QHBoxLayout()
		self.setStyleSheet('QPushButton{margin-left:1px;} QLineEdit{margin-right:0px;}')
		lay.setContentsMargins(0, 0, 0, 0)
		lay.setSpacing(0)
		self.txtSearch=QLineEdit()
		self.txtSearch.editingFinished.connect(self._emitEdit)
		self.txtSearch.returnPressed.connect(self._emitReturn)
		self.txtSearch.textChanged.connect(self._emitChange)
		lay.addWidget(self.txtSearch)
		self.btnSearch=QPushButton()
		icn=QIcon.fromTheme("search")
		self.btnSearch.clicked.connect(self._emitClick)
		self.btnSearch.setIcon(icn)
		lay.addWidget(self.btnSearch)
		self.setLayout(lay)
	#def __init__

	def _emitClick(self):
		self.clicked.emit()
	#def _emitClick

	def _emitEdit(self):
		self.editingFinished.emit()
	#def _emitEdit

	def _emitReturn(self):
		self.returnPressed.emit()
	#def _emitEdit

	def _emitChange(self):
		self.textChanged.emit()
	#def _emitEdit

	def text(self):
		return(self.txtSearch.text())
	#def text

	def setText(self,text):
		self.txtSearch.setText(text)
	#def setText

	def setPlaceholderText(self,text):
		self.txtSearch.setPlaceholderText(text)
	#def setPlaceholderText
#class QSearchBox
