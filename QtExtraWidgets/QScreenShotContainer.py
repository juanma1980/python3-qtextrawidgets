from PySide2.QtWidgets import QWidget, QPushButton,QScrollArea,QLabel,QHBoxLayout,QDialog,QAbstractItemView,QGridLayout,QTableWidgetItem,QDesktopWidget
from PySide2 import QtGui
from PySide2.QtCore import Qt,Signal,QEvent,QThread,QSize
from . import QTableTouchWidget
import os,hashlib,requests

class _loadScreenShot(QThread):
	imageLoaded=Signal("PyObject")
	def __init__(self,*args):
		super().__init__()
		self.img=args[0]
		self.cacheDir=None
		if len(args)>1:
			self.setCacheDir(args[1])
		self.destroyed.connect(self._clean)
	#def __init__

	def _debug(self,msg):
		print("{}".format(msg))
	#def _debug

	def _clean(self):
		self.quit()
	#def _clean
	
	def setCacheDir(self,cacheDir):
		sureDirs=["/tmp/.cache",os.path.join(os.environ.get('HOME',''),".cache")]
		if isinstance(cacheDir,str)==False:
			cacheDir=''
		for sure in sureDirs:
			if sure in cacheDir:
				sureDirs=[]
				break
		if sureDirs:
			return
		if isinstance(cacheDir,str)==False:
			cacheDir=""
		if os.path.exists(cacheDir)==False:
			try:
				os.makedirs(cacheDir)
			except Exception as e:
				print("mdkdir {0} failed: {1}".format(cacheDir,e))
		if os.path.isdir(cacheDir)==True:
			self.cacheDir=cacheDir
		self._debug("Cache set to {}".format(self.cacheDir))
	#def setCacheDir

	def run(self,*args):
		img=None
		md5Name=""
		md5Name=hashlib.md5(self.img.encode())
		icn=QtGui.QIcon.fromTheme("image-x-generic")
		pxm=icn.pixmap(512,512)
		if self.cacheDir:
			fPath=os.path.join(self.cacheDir,str(md5Name.hexdigest()))#self.img.split('/')[-1])
			if os.path.isfile(fPath)==True:
				pxm=QtGui.QPixmap()
				try:
					pxm.load(fPath)
					img=True
				except Exception as e:
					print("Loading cache pixmap: {}".format(e))
		if img==None:
			try:
				img=requests.get(self.img)
				pxm.loadFromData(img.content)
			except Exception as e:
				img=None
				print("request: {}".format(e))
		if img:
			if self.cacheDir:
				fPath=os.path.join(self.cacheDir,str(md5Name.hexdigest()))
				if os.path.exists(fPath)==False:
					pxm=pxm.scaled(256,256,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
					p=pxm.save(fPath,"PNG")#,quality=5)
		self.imageLoaded.emit(pxm)
		return True
	#def run
#class _loadScreenShot

class QScreenShotContainer(QWidget):
	def __init__(self,parent=None):
		QWidget.__init__(self, parent)
		self.widget=QWidget()
		self.lay=QHBoxLayout()
		self.outLay=QHBoxLayout()
		self.scroll=QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		self.outLay.addWidget(self.scroll)
		self.setLayout(self.outLay)
		self.widget.setLayout(self.lay)
		self.cacheDir=None
		self.th=[]
		self.btnImg={}
	#def __init__

	def setCacheDir(self,cacheDir):
		if os.path.exists(cacheDir)==False:
			try:
				os.makedirs(cacheDir)
			except Exception as e:
				print("mdkdir {0} failed: {1}".format(cacheDir,e))
		if os.path.isdir(cacheDir)==True:
			self.cacheDir=cacheDir
	#def setCacheDir

	def eventFilter(self,source,qevent):
		if isinstance(qevent,QEvent):
			if qevent.type()==QEvent.Type.MouseButtonPress:
				self._carrousel(source)
		return(False)
	#def eventFilter

	def _initWidget(self):
		widget=QTableTouchWidget.QTableTouchWidget()
		widget.setRowCount(1)
		widget.setShowGrid(True)
		widget.verticalHeader().hide()
		widget.horizontalHeader().hide()
		widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		widget.setRowCount(1)
		return(widget)
	#def _initWidget(self):

	def _addImgToWidget(self,img,xSize,ySize):
		self.widget.setColumnCount(self.widget.columnCount()+1)
		container=QWidget()
		lay=QHBoxLayout()
		container.setLayout(lay)
		container.setFixedSize(QSize(xSize,ySize))
		lay.addStretch()
		lay.addWidget(img)
		lay.addStretch()
		self.widget.setCellWidget(0,self.widget.columnCount()-1,container)
		self.widget.setItem(0,self.widget.columnCount()-1,QTableWidgetItem())
		self.widget.setColumnWidth(self.widget.columnCount()-1,xSize)
		self.widget.setRowHeight(self.widget.rowCount()-1,ySize)
	#def _addImgToWidget

	def _carrousel(self,btn="",w=0,h=0):
		dlg=QDialog()	
		dlg.setModal(True)
		if (w==0) or (h==0):
			sizeObject = QDesktopWidget().screenGeometry(-1)
			w=int(sizeObject.width()/2)
			h=int(sizeObject.height()/2)
		xSize=w
		ySize=h
		self.widget=self._initWidget()
		mainLay=QGridLayout()
		mainLay.setHorizontalSpacing(0)
		selectedImg=""
		arrayImg=[]
		for btnImg,img in self.btnImg.items():
			lbl=QLabel()
			lbl.setPixmap(img.scaled(xSize,ySize,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
			if btnImg==btn:	
				selectedImg=lbl
			else:
				arrayImg.append(lbl)
		if selectedImg:
			self._addImgToWidget(selectedImg,xSize,ySize)
		for lbl in arrayImg:
			self._addImgToWidget(lbl,xSize,ySize)

		icn=QtGui.QIcon.fromTheme("window-close")
		btnClose=QPushButton()
		btnClose.setIcon(icn)
		btnClose.setIconSize(QSize(24,24))
		icn=QtGui.QIcon.fromTheme("go-previous")
		btnPrev=QPushButton()
		btnPrev.setIcon(icn)
		btnPrev.setIconSize(QSize(24,24))
		icn=QtGui.QIcon.fromTheme("go-next")
		btnNext=QPushButton()
		btnNext.setIcon(icn)
		btnNext.setIconSize(QSize(24,24))
		fontSize=btnPrev.font().pointSize()
		btnClose.clicked.connect(dlg.reject)
		btnPrev.clicked.connect(lambda x:self._scrollContainer("left"))
		btnNext.clicked.connect(lambda x:self._scrollContainer("right"))
		mainLay.addWidget(btnPrev,0,0,1,1,Qt.AlignRight)
		mainLay.addWidget(self.widget,0,1,1,1)
		mainLay.addWidget(btnClose,0,2,1,1,Qt.AlignTop|Qt.AlignRight)
		mainLay.addWidget(btnNext,0,2,1,1,Qt.AlignLeft)
		dlg.setLayout(mainLay)
		dlg.setFixedSize(xSize+(0.1*xSize),ySize+(0.1*ySize))
		dlg.exec()
	#def carrousel
	
	def _scrollContainer(self,*args):
		if len(args)==0:
			return
		visible = self.widget.itemAt(20, 20)
		column=1
		if visible is not None:
			column=visible.column()
		if args[0]=="left":
			if column<=0:
				column=self.widget.columnCount()
			self.widget.scrollToItem(self.widget.item(visible.row(), column-1))
		elif args[0]=="right":
			if column>=self.widget.columnCount()-1:
				column=-1
			self.widget.scrollToItem(self.widget.item(visible.row(), column+1))
	#def scrollContainer(self,*args):
	
	def addImage(self,img):
		scr=_loadScreenShot(img,self.cacheDir)
		scr.imageLoaded.connect(self._load)
		scr.start()
		self.th.append(scr)
	#def addImage

	def loadScreenShot(self,img,cacheDir=""):
		if len(cacheDir)==0:
			cacheDir=self.cacheDir
		return(_loadScreenShot(img,cacheDir))
	#def loadScreenShot(self,img,cacheDir="")

	def _load(self,*args):
		img=args[0]
		if isinstance(img,QtGui.QPixmap):
			if img.isNull()==False:
				btnImg=QPushButton()
				self.lay.addWidget(btnImg)
				self.btnImg[btnImg]=img
				icn=QtGui.QIcon(img)
				btnImg.setIcon(icn)
				btnImg.setIconSize(QSize(128,128))
				self.scroll.setFixedHeight(btnImg.sizeHint().height()+32)
				btnImg.installEventFilter(self)
				btnImg.show()
	#def load

	def clear(self):
		self._cleanThreads()
		for i in reversed(range(self.lay.count())): 
			self.lay.itemAt(i).widget().deleteLater()
		self.btnImg={}
	#def clear

	def _cleanThreads(self):
		for th in self.th:
			th.wait()
	#def _cleanThreads
#class QScreenShotContainer
