from PyQt5.QtWidgets import QTabWidget
from Layout_Pages.table_layout import Layout1
from Layout_Pages.dashboard_layout import Layout2
from Layout_Pages.compare_layout import Compare

tabs_bottom = QTabWidget()
table_obj = Layout1()
dashboard_obj = Layout2()
compare_obj = Compare()