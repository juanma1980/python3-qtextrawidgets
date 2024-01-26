from PySide2.QtWidgets import QScroller,QScrollerProperties,QTableWidget,QWidget,QAbstractItemView

class QTableTouchWidget(QTableWidget):
	def __init__(self,*args,**kwargs):
		parent = kwargs.get('parent')
		if not parent:
			for i in args:
				if isinstance(i,QWidget):
					parent = i
		super().__init__(*args,**kwargs)
		self.scroller=QScroller()
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
#		sp=self.scroller.scrollerProperties()
#		sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor,0.6)
#		sp.setScrollMetric(QScrollerProperties.MinimumVelocity,0.0)
#		sp.setScrollMetric(QScrollerProperties.MaximumVelocity,0.5)
#		sp.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime,0.4)
#		sp.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor,1.2)
#		sp.setScrollMetric(QScrollerProperties.SnapPositionRatio,0.2)
#		sp.setScrollMetric(QScrollerProperties.MaximumClickThroughVelocity,0)
#		sp.setScrollMetric(QScrollerProperties.DragStartDistance,0.001)
#		sp.setScrollMetric(QScrollerProperties.MousePressEventDelay,0.5)
		self.scroller.grabGesture(self.viewport(),self.scroller.LeftMouseButtonGesture)
	#def __init__
#class QTableTouchWidget

if __name__=="__main__":
	obj=QTableTouchWidget()

