from PySide2.QtWidgets import QScrollArea,QGridLayout,QLabel,QWidget,QPushButton
from PySide2.QtGui import QIcon,QColor,QPalette
from PySide2.QtCore import Qt,Signal,QSize

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
		self.setAttribute(Qt.WA_StyledBackground, True)
		self.setObjectName("Frame")
		lay = QGridLayout()
		lay.setContentsMargins(3,3,3,3)
		lblIcn=QLabel()
		icn=QIcon.fromTheme("dialog-information")
		icnSize=24
		lblIcn.setPixmap(icn.pixmap(icnSize,icnSize))
		lblIcn.setMaximumWidth(icnSize)
		lblIcn.setMaximumHeight(icnSize)
		lay.addWidget(lblIcn,0,0,1,1,Qt.Alignment(0))
		self.label = QLabel()
		self.label.setAlignment(Qt.AlignLeft)
		lay.addWidget(self.label,0,1,1,1,Qt.AlignTop)
		self.label.setText(text)
		self.label.adjustSize()
		self.btn=QPushButton()
		self.btn.setMaximumWidth(icnSize)
		self.btn.setMaximumHeight(icnSize)
		self.btn.clicked.connect(self.hide)
		self.btn.setFlat(True)
		icn=QIcon.fromTheme("dialog-close")
		self.btn.setIcon(icn)
		self.btn.setIconSize(QSize(icnSize,icnSize))
		lay.addWidget(self.btn,0,2,1,1,Qt.AlignTop)
		self.btnAction=QPushButton("")
		self.btnAction.setVisible(False)
		self.btnAction.clicked.connect(self.emitClick)
		lay.addWidget(self.btnAction,1,1,1,2,Qt.AlignRight)
		self.setLayout(lay)
		bcolor=QColor(QPalette().color(QPalette.Active,QPalette.Highlight))
		color=QColor(QPalette().color(QPalette.Inactive,QPalette.Highlight))
		self.setAutoFillBackground(True)
		pal=self.palette()
		#pal.setColor(QPalette.Window,bcolor)
		rgbColor="{0},{1},{2}".format(color.red(),color.green(),color.blue())
		rgbBcolor="{0},{1},{2}".format(bcolor.red(),bcolor.green(),bcolor.blue())
		self.setStyleSheet("""#Frame {
			background-color: rgb(%s); 
			border-style: solid; 
			border-color: rgb(%s); 
			border-width: 1px; 
			border-radius: 2px;}"""%(rgbColor,rgbBcolor))
		#lay.setColumnStretch(1,1)

		#pal.setColor(QPalette.Button,color)
		#self.setPalette(pal);
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

	def setActionIcon(self,icon,size=0):
		if isinstance(icon,str)==True:
			icon=QIcon.fromTheme(icon)
		self.btnAction.setIcon(icon)
		if size>0:
			self.btnAction.setIconSize(QSize(size,size))
		self.btnAction.setVisible(True)

	def setWordWrap(self,boolWrap):
		self.label.setWordWrap(boolWrap)
	#def setWordWrap
#class QScrollLabel
