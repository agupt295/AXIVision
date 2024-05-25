import global_file
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QDialog, QFileDialog, QSplitter, QFrame, QMainWindow, QLabel, QSizePolicy, QTabWidget, QMessageBox, QLineEdit, QComboBox, QCheckBox, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

class Layout1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_tab_index = -1
        self.cbox_labels = []
        self.currentFileName = ""
        
        self.tabs = QTabWidget()
        self.tabs.tabBar().setMovable(True)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.table_tab_changed)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.add_tabs()
    
    def tab_name_change(self, file_name):
        self.tabs.setTabText(self.table_tab_index, file_name)
        
    def table_tab_changed(self, index):
        self.table_tab_index = self.tabs.currentIndex()
        tables = self.tabs.widget(self.table_tab_index).findChildren(QTableWidget)
        counter = 0
        for table in tables:
            if counter == 0:
                self.original_table_atIdx = table
            elif counter == 1:
                self.filtered_table_atIdx = table
            counter+=1
        
        tab_widget = self.tabs.widget(self.table_tab_index)
        splitter = tab_widget.findChild(QtWidgets.QSplitter)
        
        if splitter is not None:
            left_widget = splitter.widget(0)
            if left_widget is not None:
                layout = left_widget.layout()
                if layout is not None:
                    self.filter_pane = layout 

    def add_tabs(self):
        mainSplitter = QSplitter(Qt.Horizontal)
        leftPart = QFrame()
        leftPart.setFrameShape(QFrame.StyledPanel)
        rightPart = QFrame()
        rightPart.setFrameShape(QFrame.StyledPanel)
        mainSplitter.addWidget(leftPart)
        mainSplitter.addWidget(rightPart)
        
        leftLayout = QVBoxLayout(leftPart)
        leftPart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        leftLayout.setSpacing(0)
        
        self.original_table = QTableWidget()
        self.original_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.filtered_table = QTableWidget()
        self.filtered_table.setEditTriggers(QTableWidget.NoEditTriggers)
        horizontal_header = self.filtered_table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        horizontal_header.setStretchLastSection(True)
        rightLayout = QVBoxLayout(rightPart)
        
        hbox_rename = QHBoxLayout()
        hbox_rename.addWidget(QLabel('Rename Tab  '))
        new_name = QLineEdit()
        hbox_rename.addWidget(new_name)
        renameBtn = QPushButton('Rename')
        renameBtn.clicked.connect(lambda: self.rename_tab(new_name.text()))
        closeBtn = QPushButton()
        closeBtn.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\delete.png"))
        closeBtn.clicked.connect(self.close_tab)
        hbox_rename.addWidget(renameBtn)
        save_table = QPushButton('Save Table')
        save_table.clicked.connect(lambda: self.save_table_data(self.original_table))
        save_table.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\save-table.png"))
        hbox_rename.addWidget(save_table)
        hbox_rename.addWidget(closeBtn)
        rightLayout.addLayout(hbox_rename)
        
        new_tab = QMainWindow()
        new_tab.setCentralWidget(mainSplitter)
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('---- ORIGINAL TABLE WILL BE SHOWN HERE ----'))
        select_all = QPushButton('Select All')
        select_all.clicked.connect(self.all_file_export)
        hbox.addWidget(select_all)
        filter_pop = QPushButton("Apply Filters?")
        filter_pop.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\filter.png"))
        filter_pop.clicked.connect(self.filter_popup)
        hbox.addWidget(filter_pop)
        remove_filter = QPushButton('Remove Filters?')
        remove_filter.clicked.connect(self.remove_filters)
        remove_filter.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\remove-filter.png"))
        hbox.addWidget(remove_filter)
        rightLayout.addLayout(hbox)
        rightLayout.addWidget(self.original_table)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('---- FILTERED TABLE WILL BE SHOWN HERE ----'))
        cancel = QPushButton('Clear Table')
        cancel.clicked.connect(self.cancel)
        export = QPushButton('Export to Dashboard')
        export.clicked.connect(self.export_file)
        hbox2.addWidget(cancel)
        hbox2.addWidget(export)
        
        rightLayout.addLayout(hbox2)
        rightLayout.addWidget(self.filtered_table)
        
        self.tabs.addTab(new_tab, "Table {}".format(self.currentFileName))
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                height: 30px;
                font-size: 16px;
            }
        """)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        
    def save_table_data(self, table_widget):
        if table_widget.rowCount() == 0 or table_widget.columnCount() == 0:
            QMessageBox().information(None, "ERROR", "You cannot save an empty file!")
        else:
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
                    
    def close_tab(self):
        if self.tabs.count() == 1:
            QMessageBox.information(None, "ERROR", "One Table must remain on the application!")
        else:
            confirm_dialog = QMessageBox()
            confirm_dialog.setIcon(QMessageBox.Warning)
            confirm_dialog.setText("Are you sure you want to close this tab: {}?".format(self.tabs.tabBar().tabText(self.table_tab_index)))
            confirm_dialog.setWindowTitle("Confirmation")
            confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            # If the user confirms, remove the tab
            if confirm_dialog.exec_() == QMessageBox.Yes:
                self.tabs.removeTab(self.table_tab_index)
            
    def rename_tab(self, new_name):
        nameExists = False
        for i in range(self.tabs.count()):
            if self.tabs.tabBar().tabText(i) == new_name:
                QMessageBox().information(None, "[RENAME]", "You cannot have 2 tabs with the same names!")
                nameExists = True
                
        if not nameExists:
            self.tabs.setTabText(self.table_tab_index, new_name)
            
    def remove_filters(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setText("Are you sure you want remove all the filters?")
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # If the user confirms, remove the tab
        if confirm_dialog.exec_() == QMessageBox.Yes:
            self.white_cells()
            self.clear_layout(self.filter_pane)   
            self.cbox_labels.clear()
            self.combobox_temp_list.clear()
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())
    
    def filter_popup(self):
        if self.original_table_atIdx.rowCount() == 0 or self.original_table_atIdx.columnCount() == 0:
            QMessageBox().information(None, "ERROR", "You need to import a table first!")
        else:
            popup = Filter_popupBox(self)
            popup.exec_()
    
    def cancel(self):
        self.filtered_table_atIdx.clearContents()
        self.filtered_table_atIdx.setRowCount(0)
        self.filtered_table_atIdx.setColumnCount(0)
    
    def all_file_export(self):
        num_rows = self.original_table_atIdx.rowCount()
        num_columns = self.original_table_atIdx.columnCount()
        
        if num_rows == 0 or num_columns == 0:
            QMessageBox().information(None, '[ERROR]', 'You need to import a file!')
        else:
            self.filtered_table_atIdx.setRowCount(num_rows)
            self.filtered_table_atIdx.setColumnCount(num_columns)

            for row in range(num_rows):
                for column in range(num_columns):
                    # Retrieve data from source table
                    header_item = self.original_table_atIdx.horizontalHeaderItem(column)
                    source_item = self.original_table_atIdx.item(row, column)
                    if source_item is not None:
                        source_text = source_item.text()
                    else:
                        source_text = ""
                    self.filtered_table_atIdx.setItem(row, column, QTableWidgetItem(source_text))
                    if header_item is not None:
                        header_text = header_item.text()
                        self.filtered_table_atIdx.setHorizontalHeaderItem(column, QTableWidgetItem(header_text))
    
    def export_file(self):
        if self.filtered_table_atIdx.rowCount()==0 or self.filtered_table_atIdx.columnCount()==0:
            QMessageBox.information(None, '[ERROR]', 'You cannot export an empty table!')
        else:
            global_file.dashboard_obj.update_table_idx(self.tabs.tabBar().tabText(self.table_tab_index))
            global_file.dashboard_obj.update_tabs(self.filtered_table_atIdx)
            self.show_success_message()
            self.cancel()
            
    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Task Completed")
        msg.setText("The table was exported to the dashboard successfully.\nView it in Dashboard->Home")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def white_cells(self):
        for row in range(self.original_table_atIdx.rowCount()):
            for col in range(self.original_table_atIdx.columnCount()):
                self.original_table_atIdx.item(row, col).setBackground(QColor('white'))
           
    def highlight_cells(self):
        self.white_cells()
        filter_started = False
        error = False
        if "Start and End time" in self.cbox_labels:
            start_time = self.options_start.text()
            end_time = self.options_end.text()
            if start_time.isdigit() and end_time.isdigit() and int(start_time) <= int(end_time) and int(start_time)>=0 and int(end_time) >= 0:
                error = False
                
                for col in range(self.original_table_atIdx.columnCount()):
                    if self.original_table_atIdx.horizontalHeaderItem(col).text() == "Txn Start time (ns)":
                        start_col = col
                    elif self.original_table_atIdx.horizontalHeaderItem(col).text() == "Txn End time (ns)":
                        end_col = col
                        
                for row in range(self.original_table_atIdx.rowCount()):
                    if int(start_time) <= int(self.original_table_atIdx.item(row, start_col).text()) and int(end_time) >= int(self.original_table_atIdx.item(row, end_col).text()):
                        for col in range(self.original_table_atIdx.columnCount()):
                            self.original_table_atIdx.item(row,col).setBackground(QColor('yellow'))
                            filter_started = True
            else:
                error = True
        
        if not error:
            for i in range(len(self.combobox_temp_list)):
                col_idx = self.get_column_index(self.cbox_labels[i].text(), self.original_table_atIdx)
                filter_input = self.combobox_temp_list[i].currentText()
                if not filter_input == "--SELECT--":
                    if not filter_started:
                        for row in range(self.original_table_atIdx.rowCount()):
                            if self.original_table_atIdx.item(row, col_idx).text() == filter_input:
                                for j in range(self.original_table_atIdx.columnCount()):
                                    self.original_table_atIdx.item(row, j).setBackground(QColor('yellow'))
                                    filter_started = True
                    else:
                        for row in range(self.original_table_atIdx.rowCount()):
                            if self.original_table_atIdx.item(row,0).background().color() == Qt.yellow and self.original_table_atIdx.item(row, col_idx).text() == filter_input:
                                for j in range(self.original_table_atIdx.columnCount()):
                                    self.original_table_atIdx.item(row, j).setBackground(QColor('yellow'))
                                    filter_started = True
                            else:
                                for j in range(self.original_table_atIdx.columnCount()):
                                    self.original_table_atIdx.item(row, j).setBackground(QColor('white'))
        else:
            QMessageBox.information(None, '[ERROR] INVALID INPUT', 'The input must be non-negative integer and start time < end time')
            
        filtered_row = 0
        for row in range(self.original_table_atIdx.rowCount()):
            background_color = self.original_table_atIdx.item(row, 0).background().color()
            if background_color == Qt.yellow:
                filtered_row = filtered_row + 1
        
        self.filtered_table_atIdx.setRowCount(filtered_row)
        self.filtered_table_atIdx.setColumnCount(self.original_table_atIdx.columnCount())
        row_new = -1
        for row in range(self.original_table_atIdx.rowCount()):
            col_new = -1
            if self.original_table_atIdx.item(row, 0).background().color() == Qt.yellow:
                row_new = row_new + 1
                for col in range(self.original_table_atIdx.columnCount()):
                    if self.original_table_atIdx.item(row,col).background().color() == Qt.yellow:
                        col_new = col_new + 1
                        header_item = self.original_table_atIdx.horizontalHeaderItem(col)
                        source_item = self.original_table_atIdx.item(row, col)
                        if source_item is not None:
                            source_text = source_item.text()
                        else:
                            source_text = ""
                        self.filtered_table_atIdx.setItem(row_new, col_new, QTableWidgetItem(source_text))
                        if header_item is not None:
                            header_text = header_item.text()
                            self.filtered_table_atIdx.setHorizontalHeaderItem(col, QTableWidgetItem(header_text))
     
    def get_column_index(self, header_text, data) -> int:
        for col in range(data.columnCount()):
            header = data.horizontalHeaderItem(col).text()
            if header == header_text:
                return col
        return -1
    
    def filter_visible(self, cbox_filter_names):
        if not self.filter_pane.count() == 0:
            QMessageBox().information(None, "ERROR", "You have already applied the filters! Remove the existing filters to add more filters!")
        else:
            for col in range(self.original_table_atIdx.columnCount()):
                isInt = False
                filterHbox = QHBoxLayout()
                header_item = self.original_table_atIdx.horizontalHeaderItem(col).text()
                if header_item in cbox_filter_names:
                    if not header_item == "Txn Start time (ns)" and not header_item == "Txn End time (ns)":
                        label_temp = QLabel(header_item)
                        self.cbox_labels.append(label_temp)
                        filterHbox.addWidget(label_temp)
                        options = QComboBox()
                        options.addItem('--SELECT--')
                        filterHbox.addWidget(options)
                        self.combobox_temp_list.append(options)
                        self.filter_pane.addLayout(filterHbox)
                        filter_temp_list = []
                
                        for row in range(self.original_table_atIdx.rowCount()):
                            if not str(self.original_table_atIdx.item(row, col).text()) in filter_temp_list:
                                filter_temp_list.append(str(self.original_table_atIdx.item(row, col).text()))
                                if(str(self.original_table_atIdx.item(row, col)).isdigit()):
                                    isInt = True
                        if isinstance(options, QComboBox):
                            if isInt:
                                sorted_list = sorted(filter_temp_list, key=lambda x: int(x))
                                for i in range(len(sorted_list)):
                                    options.addItem(str(sorted_list[i]))
                            else:
                                for i in range(len(filter_temp_list)):
                                    options.addItem(str(filter_temp_list[i]))
            
            if "Start and End time" in cbox_filter_names:
                self.cbox_labels.append("Start and End time")
                label_temp = QLabel("Start and End time")
                filterHbox.addWidget(label_temp)
                self.options_start = QLineEdit()
                self.options_end = QLineEdit()
                filterHbox.addWidget(self.options_start)
                filterHbox.addWidget(self.options_end)
                self.filter_pane.addLayout(filterHbox)
                
            hbox_btns = QHBoxLayout()
            highlight = QPushButton('Highlight Cells')
            highlight.clicked.connect(self.highlight_cells)
            highlight.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\highlight.png"))
            hbox_btns.addWidget(highlight)
            
            clear_highlight = QPushButton('Clear Highlight')
            clear_highlight.clicked.connect(self.white_cells)
            clear_highlight.setIcon(QIcon(r"C:\Users\z004suej\Desktop\desktopApp\app\images\delete.png"))
            hbox_btns.addWidget(clear_highlight)
            self.filter_pane.addLayout(hbox_btns)
            
class Filter_popupBox(QDialog):
    def __init__(self, layout1_obj):
        super().__init__()
        
        layout = QVBoxLayout()
        self.cbox_list = []
        self.cbox_name_list = []
        for col in range(layout1_obj.original_table_atIdx.columnCount()-2):
            cbox = QCheckBox(layout1_obj.original_table_atIdx.horizontalHeaderItem(col).text())
            self.cbox_list.append(cbox)
            layout.addWidget(cbox)
        
        self.cbox_time = QCheckBox("Start and End time")
        self.cbox_list.append(self.cbox_time)
        layout.addWidget(self.cbox_time)
        
        select = QPushButton('Select Filters')
        select.clicked.connect(lambda: self.select_filters(layout1_obj))
        layout.addWidget(select)
        
        self.setLayout(layout)
    
    def select_filters(self, layout1_obj):
        for cbox in self.cbox_list:
            if cbox.isChecked():
                self.cbox_name_list.append(cbox.text())
                
        if self.cbox_time.isChecked():
            self.cbox_name_list.append(cbox.text())
        layout1_obj.filter_visible(self.cbox_name_list)
        self.accept()