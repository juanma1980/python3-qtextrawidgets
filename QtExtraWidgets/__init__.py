from . import QTableTouchWidget as _QTableTouchWidget
from . import QCheckableComboBox as _QCheckableComboBox
from . import QSearchBox as _QSearchBox
from . import QHotkeyButton as _QHotkeyButton
from . import QScrollLabel as _QScrollLabel
from . import QScreenShotContainer as _QScreenShotContainer
from . import QStackedWindow as _QStackedWindow
from . import QStackedWindowItem as _QStackedWindowItem

class QTableTouchWidget(_QTableTouchWidget.QTableTouchWidget):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QCheckableComboBox(_QCheckableComboBox.QCheckableComboBox):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QSearchBox(_QSearchBox.QSearchBox):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QHotkeyButton(_QHotkeyButton.QHotkeyButton):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QScrollLabel(_QScrollLabel.QScrollLabel):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QScreenShotContainer(_QScreenShotContainer.QScreenShotContainer):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QStackedWindow(_QStackedWindow.QStackedWindow):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

class QStackedWindowItem(_QStackedWindowItem.QStackedWindowItem):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
