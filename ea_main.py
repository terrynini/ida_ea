from .ea_cmd import ea_cmd
from .ea_emu_client import ea_emulate
from .ea_heap import ea_heap
from .ea_skin import apply_skin, ea_reskin
from .ea_trace import ea_trace
from .ea_utils import QtWidgets, config
from .ea_view import ea_view

# import module from same directory was changed in python3
# ref: https://stackoverflow.com/questions/27365273/

if config["apply_skin_on_startup"]:
    apply_skin(init=True)
    # apply_initial_skin()

menu_bar = next(i for i in QtWidgets.qApp.allWidgets() if isinstance(i, QtWidgets.QMenuBar))
menu = menu_bar.addMenu("IDA EA")
menu.addAction("Viewer").triggered.connect(ea_view)
menu.addAction("Heap").triggered.connect(ea_heap)
menu.addAction("Emulate").triggered.connect(ea_emulate)
menu.addAction("Trace Dump").triggered.connect(ea_trace)
menu.addAction("CMD").triggered.connect(ea_cmd)
menu.addAction("Reskin").triggered.connect(ea_reskin)
