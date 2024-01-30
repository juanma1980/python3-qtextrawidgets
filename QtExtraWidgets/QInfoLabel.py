from PySide2.QtWidgets import QScrollArea,QGridLayout,QLabel,QWidget,QPushButton
from PySide2.QtGui import QIcon,QColor,QPalette
from PySide2.QtCore import Qt,Signal

class QInfoLabel(QWidget):
	clicked=Signal()
	def __init__(self,*args,**kwargs):
		parent = kwargs.get('parent')
		text = kwargs.get('text',"")
		if not parent:
			for i in args:
				if isinstance(i,QWidget):
					parent = i
		super().__init__(*args,**kwargs)
		lay = QGridLayout()
		lay.setSpacing(3)
		lblIcn=QLabel()
		icn=QIcon.fromTheme("dialog-information")
		lblIcn.setPixmap(icn.pixmap(24,24))
		lay.addWidget(lblIcn,0,0,1,1)
		self.label = QLabel()
		self.label.setAlignment(Qt.AlignLeft)
		#self.label.setWordWrap(True)
		lay.addWidget(self.label,0,1,1,1)
		self.label.setText(text)
		self.label.adjustSize()
		self.btn=QPushButton()
		self.btn.clicked.connect(self.hide)
		self.btn.setFlat(True)
		icn=QIcon.fromTheme("dialog-close")
		self.btn.setIcon(icn)
		lay.addWidget(self.btn,0,2,1,1)
		self.btnAction=QPushButton("")
		self.btnAction.setVisible(False)
		self.btnAction.clicked.connect(self.emitClick)
		lay.addWidget(self.btnAction,1,0,1,2)
		self.setLayout(lay)
		color=QColor(QPalette().color(QPalette.Active,QPalette.Midlight))
		self.setAutoFillBackground(True)
		pal=self.palette()
		pal.setColor(QPalette.Window,color)
		pal.setColor(QPalette.Button,color)
		self.setPalette(pal);

#		self.setFixedWidth(self.label.sizeHint().width())
#		self.setFixedHeight(self.label.sizeHint().height()/2)
	#def __init__

	def hide(self):
		self.setVisible(False)

	def emitClick(self):
		self.clicked.emit()

	def setText(self,text):
		self.label.setText(text)
#		self.setFixedWidth(self.label.sizeHint().width())
#		self.setFixedHeight(self.label.sizeHint().height())
		self.label.adjustSize()
	#def setText

	def setActionText(self,text):
		self.btnAction.setText(text)
		self.btnAction.setVisible(True)

	def setWordWrap(self,boolWrap):
		self.label.setWordWrap(boolWrap)
	#def setWordWrap
#class QScrollLabel
