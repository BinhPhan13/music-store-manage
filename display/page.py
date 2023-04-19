import ttkbootstrap as ttk

class Page:
	def __init__(self, main_frame:ttk.Frame) :
		self._font = "bookman old style"
		self._frame = ttk.Frame(main_frame)
		self._init_frame()

	def _init_frame(self):
		pass

	def _reload(self):
		pass
	
	def show(self):
		self._reload()
		self._frame.pack(fill='both', expand=1)

	def forget(self):
		self._frame.pack_forget()