from PyQt5.QtWidgets import QHeaderView, QComboBox, QFileDialog, QTreeView, QSplitter, QFrame, QLabel, QTabWidget, QMessageBox, QLineEdit, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from stats import Stats
from data import Data
import os

class Layout2(QWidget):
    def __init__(self):
        super().__init__()
        self.tabGlobalCount = 0
        self.tab_index = -1
        
        # main Splitter
        mainSplitter = QSplitter(Qt.Horizontal)
        self.statistic = Stats()
        # LEFT part
        leftPart = QFrame()
        leftPart.setFrameShape(QFrame.StyledPanel)
        
        # RIGHT part (in 2 pieces)
        rightPart = QSplitter(Qt.Vertical)
        self.rightPart_top = QFrame()
        self.rightPart_top.setFrameShape(QFrame.StyledPanel)
        rightPart_bottom = QFrame()
        rightPart_bottom.setFrameShape(QFrame.StyledPanel)
        rightPart.addWidget(self.rightPart_top)
        rightPart.addWidget(rightPart_bottom)
        
        # adding Tabs to the lower right part of the dashboard
        self.tabs_bottom = QTabWidget()
        self.tabs_bottom.tabBar().setMovable(True)
        self.tabs_bottom.currentChanged.connect(self.tab_changed)
        template = QVBoxLayout()
        template.addWidget(self.tabs_bottom)
        rightPart_bottom.setLayout(template)
        
        # adding pane to the upper right part of the dashboard
        self.dynamic_graph_pane = QVBoxLayout(self.rightPart_top)
        self.dynamic_pattern_pane = QVBoxLayout()
        self.pattern_diff = QHBoxLayout()
        self.dynamic_graph_pane.addLayout(self.pattern_diff)
        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
        
        # adding pane to the left part of the dashboard
        self.left_stack = QVBoxLayout(leftPart)
        self.tree_graph = QTreeView()
        self.tree_graph.setHeaderHidden(True)
        self.tree_graph.setEditTriggers(QTreeView.NoEditTriggers)
        self.left_stack.addWidget(self.tree_graph)
        model = QStandardItemModel()
        self.tree_graph.setModel(model)
        self.populate_graph_model(model)
        self.tree_graph.clicked.connect(self.tree_graph_clicked)
        
        self.tree_pattern = QTreeView()
        self.tree_pattern.setHeaderHidden(True)
        self.tree_pattern.setEditTriggers(QTreeView.NoEditTriggers)
        self.left_stack.addWidget(self.tree_pattern)
        model = QStandardItemModel()
        self.tree_pattern.setModel(model)
        self.populate_pattern_model(model)
        self.tree_pattern.clicked.connect(self.tree_pattern_clicked)
        
        self.left_stack_child = QVBoxLayout()
        self.left_stack.addLayout(self.left_stack_child)
        
        mainSplitter.addWidget(leftPart)
        mainSplitter.addWidget(rightPart)
        mainSplitter.setSizes([350,1000])
        # Set the layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(mainSplitter)
        self.setLayout(layout)
        
    def update_table_idx(self, name):
        self.table_name = name
    
    def read_write_traffic_pattern(self, table, rangeNum):  
        self.clear_layout(self.dynamic_pattern_pane)
        self.dynamic_pattern_pane = QVBoxLayout()
        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
        data_obj = Data()
        canvas, x_axis, y_axis, empty = data_obj.read_write_traffic(table, rangeNum)
        save = QPushButton('Save')
     ##   save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon(r"/images/save-image.png"))
        self.dynamic_pattern_pane.addWidget(canvas)
        self.dynamic_pattern_pane.addWidget(save)
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y_axis, empty))
        
    def dynamic_pattern_latency(self, table, rangeNum):
        try:
            if int(rangeNum) <= 0:
                QMessageBox.information(None, "[ERROR]", "Invalid input!")
            else:
                self.clear_layout(self.dynamic_pattern_pane)
                self.dynamic_pattern_pane = QVBoxLayout()
                self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
                data_obj = Data()
                canvas, x_axis, y1_axis, y2_axis = data_obj.latency_pattern(table, rangeNum)
                save = QPushButton('Save')
                ##save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
                save.setIcon(QIcon("\images\save-image.png"))
                self.dynamic_pattern_pane.addWidget(canvas)
                self.dynamic_pattern_pane.addWidget(save)
                save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y1_axis, y2_axis))
        except ValueError:
            QMessageBox.information(None, "[ERROR]", "The input must be positive integer!")

    def dynamic_graph_pane_bd(self, table):
        self.clear_layout(self.dynamic_graph_pane)
        data_obj = Data()
        canvas, x_axis, y_axis, empty = data_obj.bandwidth(table)
        self.dynamic_graph_pane.addWidget(canvas)
        save = QPushButton('Save')
       ## save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        self.dynamic_graph_pane.addWidget(save)
    
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y_axis, empty))

    def save_plot(self, canvas, x_axis, y1_axis, y2_axis):
        # Get the file path from the user
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(None, "Save Graph", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;Text (*.txt)")
        if file_path:
            # Ensure the file extension is supported by Matplotlib
            file_ext = os.path.splitext(file_path)[1]
            if file_ext.lower() in ['.png', '.jpg', '.jpeg']:
                # Save the graph using Matplotlib
                canvas.figure.savefig(file_path)
                print(f"Graph saved to: {file_path}")
            
            elif file_ext.lower() in ['.txt']:
                data_file = ""
                if len(y1_axis) == 0:
                    data_file+="PIE CHART\n"
                    for element in x_axis:
                        data_file+="{}\n".format(element)
                else:
                    if len(y2_axis) == 0:
                        data_file+="Serial] Pattern -> Frequency\n"
                        for index, element in enumerate(y1_axis):
                            data_file+="{}] {} -> {}\n".format(index+1, x_axis[index], y1_axis[index])
                    else:
                        data_file+="Serial] x_axis, READ count, WRITE count\n"
                        for index, element in enumerate(y1_axis):
                            data_file+="{}] {} -> read:{}, write:{}\n".format(index+1, x_axis[index], y1_axis[index], y2_axis[index])
                
                with open(file_path, 'w') as file:
                    file.write(data_file)
           
                print(f"Line Graph saved as text to: {file_path}")
            else:
                file_path += '.png'  # Set a default extension if not provided 
        
    def save_table_data(self, table_widget):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(None, "Save Table Data", "", "CSV Files (*.csv)")
    
        if file_path:
            with open(file_path, 'w') as file:
                table = table_widget
                rows = table.rowCount()
                columns = table.columnCount()
    
                for row in range(rows):
                    row_data = []
                    for column in range(columns):
                        item = table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    file.write(",".join(row_data) + "\n")

    def dynamic_graph_pane_read_write(self, table):
        data_obj = Data()
        canvas, x_axis, empty, empty = data_obj.read_write_pie(table)
        self.dynamic_graph_pane.addWidget(canvas)
        save = QPushButton('Save')
       ## save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, empty, empty))
        self.dynamic_graph_pane.addWidget(save)
        
    def dynamic_graph_pane_txnNum(self, table):
        data_obj = Data()
        canvas, x_axis, y_axis, empty = data_obj.txn_no_time(table)
        self.dynamic_graph_pane.addWidget(canvas)
        save = QPushButton('Save')
       ## save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y_axis, empty))
        self.dynamic_graph_pane.addWidget(save)
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())
                
    def tab_changed(self, index):
        try:
            if not self.left_stack_child.count() == 0:    
                self.clear_layout(self.left_stack_child)
            
            self.tab_index = self.tabs_bottom.currentIndex()
            self.clear_layout(self.dynamic_graph_pane)
            self.tree_graph.clearSelection()
            
            def add_stat_pane(table):
                try:
                    self.statistic = Stats()
                    self.left_stack.addLayout(self.left_stack_child)
                    self.left_stack_child.addWidget(QLabel('Average transaction time: {:.2f} ns'.format(self.statistic.txn_time_diff_avg(table))))
                    self.left_stack_child.addWidget(QLabel(self.statistic.read_write_count(table)))
                    self.left_stack_child.addWidget(QLabel(self.statistic.total_fixed_incr(table)))
                    self.left_stack_child.addWidget(QLabel('Average data bytes transferred: {:.2f} bytes'.format(self.statistic.data_bytes_transfer_avg(table))))
                    bd_label = QLabel(self.statistic.bandwidthInfo(table))
                    font = QFont()
                    font.setWeight(QFont.Bold)
                    bd_label.setFont(font)
                    self.left_stack_child.addWidget(bd_label)
                
                except TypeError:
                    QMessageBox.information(None, "FATAL ERROR", "some of the stats may not be visible if the columns are missing or the naming is incorrect!")
            add_stat_pane(self.tabs_bottom.widget(self.tab_index).findChild(QTableWidget))
        except AttributeError:
            QMessageBox.information(None, "EMPTY DASHBOARD", "You can import new table to analyze that data here!")
            
    def tree_graph_clicked(self, index:QModelIndex):
        try:
            self.clear_layout(self.dynamic_graph_pane)
            item = index.model().itemFromIndex(index)
            if not item.text() == "Graphical Analysis" and not item.text() == "LATENCY":
                if self.tabs_bottom.count() == 0:
                    QMessageBox().information(None, '[ERROR]', 'You need to import a table to the dashboard first')
                else:
                    # getting the data table for plotting
                    table = self.tabs_bottom.widget(self.tab_index).findChild(QTableWidget)
                    if item.text() == "BANDWIDTH graph":
                        self.dynamic_graph_pane_bd(table)
                    elif item.text() == "LATENCY graph":
                        self.dynamic_graph_pane_txnNum(table)
                    elif item.text() == "READ-WRITE & FIXED-INCR graph":
                        self.dynamic_graph_pane_read_write(table)
                    elif item.text() == "TRANSACTION vs LATENCY Range":
                        self.clear_layout(self.dynamic_graph_pane)
                        
                        self.pattern_diff = QHBoxLayout()
                        self.dynamic_pattern_pane = QVBoxLayout()
                        
                        self.dynamic_graph_pane.addLayout(self.pattern_diff)
                        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
                        self.dynamic_pattern_pane.addWidget(FigureCanvas())
                        
                        diff_num = QLabel("Enter interval length for latency pattern   ")
                        diff_num_entry = QLineEdit()
                        diff_num_btn = QPushButton("Plot")
                        clear_plot_btn = QPushButton("Clear Plot")
                        self.pattern_diff.addWidget(diff_num)
                        self.pattern_diff.addWidget(diff_num_entry)
                        self.pattern_diff.addWidget(diff_num_btn)
                        self.pattern_diff.addWidget(clear_plot_btn)
                        
                        def plot():
                            try:
                                if diff_num_entry.text() == '':
                                    QMessageBox.information(None, "ERROR", "Enter an integer value!")
                                else:
                                    self.dynamic_pattern_latency(table, diff_num_entry.text())
                            except ValueError:
                                QMessageBox.information(None, "[ERROR]", "Invalid input!")
                                
                        diff_num_btn.clicked.connect(plot)
                        clear_plot_btn.clicked.connect(self.clear_plot_function)
        
                    elif item.text() == "TRANSACTION ID Count":
                        self.clear_layout(self.dynamic_graph_pane)
                        self.txn_id_count(table)
                    
                    elif item.text() == "ADDRESS USAGE Breakdown":
                        self.clear_layout(self.dynamic_graph_pane)
                        self.address_breakdown(table)
                        
                    elif item.text() == "ONGOING Transactions":
                        self.clear_layout(self.dynamic_graph_pane)
                        
                        self.pattern_diff = QHBoxLayout()
                        self.dynamic_pattern_pane = QVBoxLayout()
                        
                        self.dynamic_graph_pane.addLayout(self.pattern_diff)
                        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
                        self.dynamic_pattern_pane.addWidget(FigureCanvas())
                        
                        diff_num = QLabel("Enter time length for non-ending transactions   ")
                        diff_num_entry = QLineEdit()
                        diff_num_btn = QPushButton("Plot")
                        clear_plot_btn = QPushButton("Clear Plot")
                        self.pattern_diff.addWidget(diff_num)
                        self.pattern_diff.addWidget(diff_num_entry)
                        self.pattern_diff.addWidget(diff_num_btn)
                        self.pattern_diff.addWidget(clear_plot_btn)
                        
                        def plot():
                            try:
                                if diff_num_entry.text() == '':
                                    QMessageBox.information(None, "ERROR", "Enter an integer value!")
                                else:
                                    self.outstanding_txns(table, diff_num_entry.text())
                                    
                            except ValueError:
                                QMessageBox.information(None, "[ERROR]", "Invalid input!")
                                
                        diff_num_btn.clicked.connect(plot)
                        clear_plot_btn.clicked.connect(self.clear_plot_function)
        except TypeError:
            QMessageBox().information(None, "[FATAL ERROR]", "Graph not available!")
    
    def clear_plot_function(self):
        self.clear_layout(self.dynamic_pattern_pane)
        self.dynamic_pattern_pane = QVBoxLayout()
        self.dynamic_pattern_pane.addWidget(FigureCanvas())
        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
        
    def address_breakdown(self, table):
        data_obj = Data()
        canvas, x_axis, y1_axis, y2_axis = data_obj.address_breakdown(table)
        self.dynamic_graph_pane.addWidget(canvas)
        save = QPushButton('Save')
       ## save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        self.dynamic_graph_pane.addWidget(save)
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y1_axis, y2_axis))
        
    def outstanding_txns(self, table, rangeNum):
        self.clear_layout(self.dynamic_pattern_pane)
        self.dynamic_pattern_pane = QVBoxLayout()
        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
        data_obj = Data()
        canvas, x_axis, y1_axis, y2_axis = data_obj.outstanding_graph(table, rangeNum)
        self.dynamic_pattern_pane.addWidget(canvas)
        save = QPushButton('Save')
        ##save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        self.dynamic_pattern_pane.addWidget(save)
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y1_axis, y2_axis))
    
    def txn_id_count(self, table):
        data_obj = Data()
        canvas, x_axis, y1_axis, y2_axis = data_obj.txn_id_count(table)
        self.dynamic_graph_pane.addWidget(canvas)
        save = QPushButton('Save')
       ## save.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-image.png"))
        save.setIcon(QIcon("\images\save-image.png"))
        self.dynamic_graph_pane.addWidget(save)
        save.clicked.connect(lambda: self.save_plot(canvas, x_axis, y1_axis, y2_axis))
        
    def clear_pattern_pane(self, layout):
        self.clear_layout(self.dynamic_pattern_pane)
        self.dynamic_pattern_pane.addWidget(FigureCanvas())
    
    def tree_pattern_clicked(self, index:QModelIndex):
        try:
            item = index.model().itemFromIndex(index)
            if not item.text() == "Pattern Analysis":
                if self.tabs_bottom.count() == 0:
                    QMessageBox().information(None, '[ERROR]', 'You need to import a table to the dashboard first')
                else:
                    table = self.tabs_bottom.widget(self.tab_index).findChild(QTableWidget)
                    self.clear_layout(self.dynamic_graph_pane)
                    
                    if item.text() == "Traffic Pattern Analysis":
                        self.pattern_diff = QHBoxLayout()
                        self.dynamic_pattern_pane = QVBoxLayout()
                        
                        self.dynamic_graph_pane.addLayout(self.pattern_diff)
                        self.dynamic_graph_pane.addLayout(self.dynamic_pattern_pane)
                        self.dynamic_pattern_pane.addWidget(FigureCanvas())
                        
                        diff_num = QLabel("Select grouping interval for traffic pattern   ")
                        diff_num_entry = QComboBox()
                        diff_num_entry.addItem("DEFAULT")
                        for i in range(2, 10):
                            diff_num_entry.addItem(str(i))
                        diff_num_btn = QPushButton("Plot")
                        clear_plot_btn = QPushButton("Clear Plot")
                        self.pattern_diff.addWidget(diff_num)
                        self.pattern_diff.addWidget(diff_num_entry)
                        self.pattern_diff.addWidget(diff_num_btn)
                        self.pattern_diff.addWidget(clear_plot_btn)
                        
                        def plot():
                            self.read_write_traffic_pattern(table, diff_num_entry.currentText())
                                
                        diff_num_btn.clicked.connect(plot)
                        clear_plot_btn.clicked.connect(self.clear_plot_function)
                        
        except TypeError:
            QMessageBox().information(None, "[FATAL ERROR]", "Graph not available!")
        
    def populate_graph_model(self, model):
        root_item = QStandardItem("Graphical Analysis")
        model.appendRow(root_item)
        child1 = QStandardItem('BANDWIDTH graph')
        child2 = QStandardItem('LATENCY')
        child3 = QStandardItem('READ-WRITE & FIXED-INCR graph')
        child4 = QStandardItem('TRANSACTION ID Count')
        child5 = QStandardItem('ADDRESS USAGE Breakdown')
        child6 = QStandardItem('ONGOING Transactions')
        root_item.appendRow(child1)
        root_item.appendRow(child2)
        root_item.appendRow(child3)
        root_item.appendRow(child4)
        root_item.appendRow(child5)
        root_item.appendRow(child6)
        sub_child1_of_2 = QStandardItem("LATENCY graph")
        child2.appendRow(sub_child1_of_2)
        sub_child2_of_2 = QStandardItem("TRANSACTION vs LATENCY Range")
        child2.appendRow(sub_child2_of_2)
        
    def populate_pattern_model(self, model):
        root_item = QStandardItem("Pattern Analysis")
        model.appendRow(root_item)
        child1 = QStandardItem('Traffic Pattern Analysis')
        root_item.appendRow(child1)
    
    def update_tabs(self, tab_table):
        table = QTableWidget()
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        horizontal_header = table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        horizontal_header.setStretchLastSection(True)
        table.setRowCount(tab_table.rowCount())
        table.setColumnCount(tab_table.columnCount())
        
        for col in range(tab_table.columnCount()):
            header_item = tab_table.horizontalHeaderItem(col)
            if header_item:
                table.setHorizontalHeaderItem(col, header_item.clone())
        
        for row in range(tab_table.rowCount()):
            for col in range(tab_table.columnCount()):
                item = QTableWidgetItem(tab_table.item(row, col).text())
                table.setItem(row, col, item)
        self.tabGlobalCount += 1
        new_tab = QWidget()
        new_tab_layout = QVBoxLayout()
        new_tab.setLayout(new_tab_layout)
        self.tabs_bottom.addTab(new_tab, "Tab {} ({})".format(self.tabGlobalCount, self.table_name))
        hbox_rename = QHBoxLayout()
        hbox_rename.addWidget(QLabel('Rename Tab  '))
        new_name = QLineEdit()
        hbox_rename.addWidget(new_name)
        renameBtn = QPushButton('Rename')
        renameBtn.clicked.connect(lambda: self.rename_tab(new_name.text()))
        closeBtn = QPushButton()
        ##closeBtn.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\delete.png"))
        closeBtn.setIcon(QIcon(r"/images/delete.png"))
        closeBtn.clicked.connect(self.close_tab)
        hbox_rename.addWidget(renameBtn)
        save_table = QPushButton('Save Table')
        save_table.clicked.connect(lambda: self.save_table_data(table))
        save_table.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-table.png"))
        hbox_rename.addWidget(save_table)
        hbox_rename.addWidget(closeBtn)
        new_tab_layout.addLayout(hbox_rename)
        new_tab_layout.addWidget(table)
        
    def close_tab(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setText("Are you sure you want to close this tab: {}?".format(self.tabs_bottom.tabBar().tabText(self.tab_index)))
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # If the user confirms, remove the tab
        if confirm_dialog.exec_() == QMessageBox.Yes:
            self.tabs_bottom.removeTab(self.tab_index)
        
    def rename_tab(self, new_name):
        nameExists = False
        for i in range(self.tabs_bottom.count()):
            if self.tabs_bottom.tabBar().tabText(i) == new_name:
                QMessageBox().information(None, "[RENAME]", "You cannot have 2 tabs with the same names!")
                nameExists = True
                
        if not nameExists:
            self.tabs_bottom.setTabText(self.tab_index, new_name)