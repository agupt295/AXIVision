import re
import statistics
from PyQt5.QtWidgets import QMessageBox
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import MouseEvent
from scipy.spatial import distance
from matplotlib.figure import Figure

class Data(): 
    def get_column_index(self, header_text, data) -> int:
        for col in range(data.columnCount()):
            header = data.horizontalHeaderItem(col).text()
            if header == header_text:
                return col
        return -1
    
    def txn_no_time(self, data) -> (FigureCanvas, list, list, list):
        try:
            x_axis = []
            y_axis = []
            empty = []
            figure = plt.figure(figsize=(0,0))
            ax = figure.add_subplot(111)
            
            canvas = FigureCanvas(figure)
            end_col_index = self.get_column_index("Txn End time (ns)", data)
            for row in range(data.rowCount()):
                if data.isRowHidden(row):
                    pass
                else:
                    y = int(data.item(row, end_col_index).text()) - int(data.item(row, end_col_index-1).text())
                    x_axis.append(row+1)
                    y_axis.append(y)
                    
            ax.plot(x_axis, y_axis, marker = "o", mec = 'r')
            ax.set_xlabel('transaction numbers')
            ax.set_ylabel('latency period (ns)')
            
            ax.grid(color='green', linestyle='--', linewidth=0.8)
            ax.legend(['mean: {:.2f}'.format(statistics.mean(y_axis))], loc ="upper left")
            canvas.draw()
            return canvas, x_axis, y_axis, empty
        
        except Exception:
            pass
        
    def outstanding_graph(self, data, rangeNum) -> (FigureCanvas, list, list, list):
        try:
            end_time_col_idx = self.get_column_index("Txn End time (ns)", data)
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            x = []
            x_copy = []
            y = []
            read_list=[]
            write_list=[]
            bar_thickness = 0.35
            # Create the bar graph with specified thickness
            num = int(rangeNum)
            end_time_max = 0
            for row in range(data.rowCount()):
                end_time_max = int(data.item(row, end_time_col_idx).text())
            counter = 0
            while True:
                counter+=1
                x.append('{}'.format(num*counter))
                x_copy.append(num*counter)
                y.append(0)
                read_list.append(0)
                write_list.append(0)
                if end_time_max <= num*counter:
                    break
    
            read_write_col_idx = self.get_column_index("Txn_type", data)
            for row in range(data.rowCount()):
                start_time_check = int(data.item(row, end_time_col_idx-1).text())
                end_time_check = int(data.item(row, end_time_col_idx).text())
                idx = 0
                while idx < len(x):
                    if start_time_check <= x_copy[idx] and end_time_check >= x_copy[idx]:
                        y[idx]+=1
                        if data.item(row, read_write_col_idx).text().upper() == "READ":
                            read_list[idx]+=1
                        elif data.item(row, read_write_col_idx).text().upper() == "WRITE":
                            write_list[idx]+=1
                        break
                    idx+=1
             
            X = np.arange(len(x))
            X_shifted = X+bar_thickness
            fig, ax = plt.subplots()
            ax.bar(X, read_list, bar_thickness, label='READ instruction')
            ax.bar(X_shifted, write_list, bar_thickness, label='WRITE instruction')
            ax.set_xticks(X_shifted - bar_thickness/2)
            ax.set_xticklabels(x)
            
            legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='orange', label='WRITE instructions'),
            plt.Rectangle((0, 0), 1, 1, color='blue', label='READ instructions')
            ]
            ax.legend(handles=legend_elements, fontsize='large')
            
            ax.grid(color = 'green', linestyle = '--', linewidth = 0.8)
            ax.set_xlabel('Latency range')
            ax.set_ylabel('Frequency')
            # Create a canvas and add the figure to it
            canvas = FigureCanvas(fig)
            canvas.draw()
            return canvas, x, read_list, write_list
        
        except Exception:
            pass    
        
    def read_write_pie(self, data) -> (FigureCanvas, list, list, list):
        try:
            readCount = 0
            writeCount = 0
            read_fixed = 0
            read_incr = 0
            write_fixed = 0
            write_incr = 0
            address_type_index = self.get_column_index("Address_type", data)
            txn_type_index = self.get_column_index("Txn_type", data)
            
            for i in range(data.rowCount()):
                if data.isRowHidden(i):
                    pass
                else:
                    if data.item(i, txn_type_index).text().upper() == "READ":
                        readCount = readCount+1
                        if data.item(i, address_type_index).text().upper() == "FIXED":
                            read_fixed = read_fixed+1
                        else:
                            read_incr = read_incr+1
                    else:
                        writeCount = writeCount+1
                        if data.item(i, address_type_index).text().upper() == "FIXED":
                            write_fixed = write_fixed+1
                        else:
                            write_incr = write_incr+1
            
            figure = plt.figure()
            figure.set_size_inches(8, 8)
            
            ax = figure.add_subplot(111)
            canvas = FigureCanvas(figure)
            
            info = np.array([read_fixed, read_incr, write_fixed, write_incr])
            info_nonzero = [element for element in info if element != 0]
            
            mylabels = ['read_Fixed: {0}'.format(read_fixed), 'read_Incr: {0}'.format(read_incr) , 'write_Fixed: {0}'.format(write_fixed), 'write_Incr: {0}'.format(write_incr)]
            mylabels_nonzero = [label for i, element in enumerate(info) if element != 0 for label in mylabels[i:i+1]]
            
            colors = ['yellow', 'orange', 'red', 'green']
            colors_nonzero = [color for i, element in enumerate(info) if element != 0 for color in colors[i:i+1]]
            
            #legend_patches = [plt.Rectangle((0, 0), 1, 1, fc=color) for color in colors_nonzero] 
            #ax.legend(legend_patches, mylabels, loc='upper left', fontsize='large')
            ax.pie(info_nonzero, labels=mylabels_nonzero, colors = colors_nonzero, startangle=90, shadow=True)
            empty_list = []
            return canvas, mylabels, empty_list, empty_list
        
        except Exception:
            pass    
  
    def latency_pattern(self, data, rangeNum) -> (FigureCanvas, list, list, list):
        try:
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            x = []
            x_copy = []
            y = []
            read_list=[]
            write_list=[]
            bar_thickness = 0.35
            # Create the bar graph with specified thickness
            num = int(rangeNum)
            latency_max = self.latency_max(data)
            counter = 0
            while True:
                counter+=1
                x.append('{}-{}'.format(num*(counter-1), num*counter))
                x_copy.append(num*counter)
                y.append(0)
                read_list.append(0)
                write_list.append(0)
                if latency_max <= num*counter:
                    break
            
            end_time_col_idx = self.get_column_index("Txn End time (ns)", data)
            read_write_col_idx = self.get_column_index("Txn_type", data)
            for row in range(data.rowCount()):
                time_diff = (int(data.item(row, end_time_col_idx).text()))-(int(data.item(row, end_time_col_idx-1).text()))
                idx = 0
                while idx < len(x):
                    if time_diff <= x_copy[idx]:
                        y[idx]+=1
                        if data.item(row, read_write_col_idx).text().upper() == "READ":
                            read_list[idx]+=1
                        elif data.item(row, read_write_col_idx).text().upper() == "WRITE":
                            write_list[idx]+=1
                        break
                    idx+=1
             
            X = np.arange(len(x))
            X_shifted = X+bar_thickness
            fig, ax = plt.subplots()
            ax.bar(X, read_list, bar_thickness, label='READ instruction')
            ax.bar(X_shifted, write_list, bar_thickness, label='WRITE instruction')
            ax.set_xticks(X_shifted - bar_thickness/2)
            ax.set_xticklabels(x)
            
            legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='orange', label='WRITE instructions'),
            plt.Rectangle((0, 0), 1, 1, color='blue', label='READ instructions')
            ]
            ax.legend(handles=legend_elements, fontsize='large')
            
            ax.grid(color = 'green', linestyle = '--', linewidth = 0.8)
            ax.set_xlabel('Latency range')
            ax.set_ylabel('Frequency')
            # Create a canvas and add the figure to it
            canvas = FigureCanvas(fig)
            canvas.draw()
            return canvas, x, read_list, write_list
        
        except Exception:
           pass
        
    def bandwidth(self, data) -> (FigureCanvas, list, list, list):
        try:
            total_bytes = 0
            rows = 0
            end_col_index = self.get_column_index("Txn End time (ns)", data)
            bytes_col_index = self.get_column_index("Number of data bytes", data)
            for row in range(data.rowCount()):
                rows = rows + 1
                end_time = int(data.item(row, end_col_index).text())
                total_bytes = total_bytes + int(data.item(row, bytes_col_index).text())
            
            band_data = total_bytes/(end_time-int(data.item(0,end_col_index-1).text()))
            
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            ax.grid(color = 'green', linestyle = '--', linewidth = 0.8)
            
            x_axis = []
            y_axis = []
            
            for row in range(data.rowCount()):
                #x = data.item(row, 0).text()
                y = int(data.item(row, bytes_col_index).text())
                #x_axis.append(x)
                x_axis.append(row+1)
                y_axis.append(y/(int(data.item(row, end_col_index).text()) - int(data.item(row, end_col_index-1).text())))
                
            ax.plot(x_axis, y_axis, marker = "o", mec = 'r')
            ax.set_xlabel('transaction numbers')
            ax.set_ylabel('bandwidth (1/s) of data transfer(bytes)')
            ax.legend(['bandwidth of data transfer = {:.2f} 1/s'.format(band_data)], loc ="upper left")
            
            canvas.resize(1700, 800)
            canvas.draw()
            
            coord_label = plt.text(0.5, 0.95, "", transform=ax.transAxes, ha="center")
            coord_label.set_fontsize(16)
            
            def on_mouse_move(event: MouseEvent):
                if event.inaxes and event.inaxes is ax:
                    x = event.xdata
                    y = event.ydata
                    ##########################
                    if x is not None and y is not None:
                        # Get the data points of the line graph
                        line = event.inaxes.lines[0]
                        x_data = line.get_xdata()
                        y_data = line.get_ydata()
            
                        # Find the nearest data point
                        distances = distance.cdist([(x, y)], np.vstack((x_data, y_data)).T)
                        nearest_index = np.argmin(distances)
            
                        # Get the snapped coordinates
                        snapped_x = x_data[nearest_index]
                        snapped_y = y_data[nearest_index]
                    ##########################
                    coord_label.set_text(f"({snapped_x:.2f}, {snapped_y:.2f})")
                    canvas.draw_idle()
                else:
                    coord_label.set_text("")
                    canvas.draw_idle()
            
            canvas.mpl_connect("motion_notify_event", on_mouse_move)
            empty = []
            return canvas, x_axis, y_axis, empty
        
        except Exception:
           pass    
        
    def bandwidthInfo(self, data) -> str:
        try:
            end_col_index = self.get_column_index("Txn End time (ns)", data)
            bytes_index = self.get_column_index("Number of data bytes", data)
            total_bytes = 0
            rows = 0
            bd_data_list = []
            for row in range(data.rowCount()):
                if data.isRowHidden(row):
                    pass
                else:
                    rows = rows + 1
                    end_time = int(data.item(row, end_col_index).text())
                    total_bytes = total_bytes + int(data.item(row, bytes_index).text())
                    bd_data_list.append(total_bytes/(end_time-int(data.item(0,end_col_index-1).text())))
            
            band_address = rows/(end_time-int(data.item(0,end_col_index-1).text()))
            band_data = total_bytes/(end_time-int(data.item(0,end_col_index-1).text()))
            
            return 'Bandwidth of address usage: {:.2f}\nBandwidth of data transfers: {:.2f}'.format(band_address, band_data)
    
        except Exception:
            pass    

    def read_write_traffic(self, data, max_series_length) -> (FigureCanvas, list, list, list):
        try:
            txn_type_col_idx = self.get_column_index("Txn_type", data)
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            data_str = ""
            for row in range(data.rowCount()):
                temp_txn = data.item(row, txn_type_col_idx).text()
                data_str = data_str+(temp_txn[0].upper())
                
            x = []
            y = []
            
            # Define the pattern to search for repetitive series of characters with the specified length
            if max_series_length == "DEFAULT":
                pattern = rf"([RW]{{2,}})(?=.*\1)"
            else:
                pattern = rf"([RW]{{2,{max_series_length}}})(?=.*\1)"
    
            # Find all matches of the pattern in the data
            matches = re.findall(pattern, data_str)
    
            # Count the frequency of each match
            frequency_count = {}
            for match in matches:
                frequency_count[match] = frequency_count.get(match, 0) + 1
    
            # Sort the matches by frequency in descending order
            sorted_matches = sorted(frequency_count.items(), key=lambda x: x[1], reverse=True)
    
            # Print the repetitive series and their frequencies
            for match, frequency in sorted_matches:
                x.append(match)
                y.append(frequency)
                
            bar_thickness = 0.1
            # Create the bar graph with specified thickness
                    
            ax.bar(x, y, width=bar_thickness)
            ax.grid(color='green', linestyle='--', linewidth=0.5)
            # Create a canvas and add the figure to it
            canvas = FigureCanvas(fig)
            canvas.draw()
            empty = []
            return canvas, x, y, empty
    
        except Exception:
            pass    

    def latency_max(self, data) -> int:
        try:
            end_col_index = self.get_column_index("Txn End time (ns)", data)
            latency_list = []
            for row in range(data.rowCount()):
                if data.isRowHidden(row):
                    pass
                else:
                    latency_list.append((int(data.item(row, end_col_index).text())-int(data.item(row,end_col_index-1).text())))
                    
            return max(latency_list)

        except Exception:
            QMessageBox.information(None, "FATAL ERROR", "The column name is not as expected! Rename the column name and then import the file again!")    

    def txn_id_count(self, data) -> (FigureCanvas, list, list, list):
        try:
            txn_id_idx = self.get_column_index("Txn_id", data)
            txn_type_col_idx = self.get_column_index("Txn_type", data)
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            ids = []
            x_labels = []
            read_count = []
            write_count = []
            
            for row in range(data.rowCount()):
                ids.append(data.item(row, txn_id_idx).text())
                
            frequency_count = Counter(ids)
            for number, frequency in sorted(frequency_count.items()):
                x_labels.append(number)
                read_count.append(0)
                write_count.append(0)
                
            def idx_finder(id_tofind, id_list) -> int:
                idx = 0
                for i in id_list:
                    if id_tofind == i:
                        return idx
                    idx+=1
                return -1
                
            for row in range(data.rowCount()):
                Id = data.item(row, txn_id_idx).text()
                if data.item(row, txn_type_col_idx).text().upper() == "READ":
                    read_count[idx_finder(Id, x_labels)]+=1
                elif data.item(row, txn_type_col_idx).text().upper() == "WRITE":
                    write_count[idx_finder(Id, x_labels)]+=1
            # Set the width of each bar
            bar_width = 0.35
            
            # Calculate the x-axis locations for the bar graphs
            x = np.arange(len(x_labels))
            x_shifted = x + bar_width
            
            # Create a figure and an axis object
            fig, ax = plt.subplots()
            
            # Create the first bar graph
            ax.bar(x, read_count, bar_width, label='Bar Graph 1')
            
            # Create the second bar graph
            ax.bar(x_shifted, write_count, bar_width, label='Bar Graph 2')
            
            # Set the x-axis tick labels and their positions
            ax.set_xticks(x_shifted - bar_width/2)
            ax.set_xticklabels(x_labels)
                    
            ax.grid(color='green', linestyle='--', linewidth=0.5)
            ax.set_xlabel('Transaction "id"')
            ax.set_ylabel('Frequency')
            
            legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='orange', label='WRITE instructions'),
            plt.Rectangle((0, 0), 1, 1, color='blue', label='READ instructions')
            ]
            ax.legend(handles=legend_elements, fontsize='large')
            
            # Create a canvas and add the figure to it
            canvas = FigureCanvas(fig)
            canvas.draw()
            return canvas, x, read_count, write_count
        
        except Exception:
            QMessageBox.information(None, "FATAL ERROR", "The column name is not as expected! Rename the column name and then import the file again!")    
    
    def address_breakdown(self, data) -> (FigureCanvas, list, list, list):
        try:
            address_col_idx = self.get_column_index("Address", data)
            txn_type_col_idx = self.get_column_index("Txn_type", data)
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            addresses = []
            x_labels = []
            read_count = []
            write_count = []
            
            for row in range(data.rowCount()):
                addresses.append(data.item(row, address_col_idx).text())
                
            frequency_count = Counter(addresses)
            for number, frequency in frequency_count.items():
                x_labels.append(number)
                read_count.append(0)
                write_count.append(0)
                
            def idx_finder(address, address_list) -> int:
                idx = 0
                for i in address_list:
                    if address == i:
                        return idx
                    idx+=1
                return -1
                
            for row in range(data.rowCount()):
                Address = data.item(row, address_col_idx).text()
                if data.item(row, txn_type_col_idx).text().upper() == "READ":
                    read_count[idx_finder(Address, x_labels)]+=1
                elif data.item(row, txn_type_col_idx).text().upper() == "WRITE":
                    write_count[idx_finder(Address, x_labels)]+=1
            # Set the width of each bar
            bar_width = 0.35
            
            # Calculate the x-axis locations for the bar graphs
            x = np.arange(len(x_labels))
            x_shifted = x + bar_width
            
            # Create a figure and an axis object
            fig, ax = plt.subplots()
            
            # Create the first bar graph
            ax.bar(x, read_count, bar_width, label='Bar Graph 1')
            
            # Create the second bar graph
            ax.bar(x_shifted, write_count, bar_width, label='Bar Graph 2')
            
            # Set the x-axis tick labels and their positions
            ax.set_xticks(x_shifted - bar_width/2)
            ax.set_xticklabels(x_labels, rotation=90)
            #ax.set_xticklabels(x_labels)
                    
            ax.grid(color='green', linestyle='--', linewidth=0.5)
            ax.set_xlabel('Address Usage')
            ax.set_ylabel('Frequency')
            
            legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color='orange', label='WRITE instructions'),
            plt.Rectangle((0, 0), 1, 1, color='blue', label='READ instructions')
            ]
            ax.legend(handles=legend_elements, fontsize='large')
            
            # Create a canvas and add the figure to it
            canvas = FigureCanvas(fig)
            canvas.draw()
            return canvas, x, read_count, write_count
        
        except Exception:
            pass    