class Stats:
    def get_column_index(self, header_text, data) -> int:
        for col in range(data.columnCount()):
            header = data.horizontalHeaderItem(col).text()
            if header == header_text:
                return col
        return -1
        
    def read_write_count(self, data) -> str:
        try:
            readCount = 0
            writeCount = 0
            read_write_col = self.get_column_index("Txn_type", data)
            for i in range(data.rowCount()):
                if data.isRowHidden(i):
                    pass
                else:
                    if data.item(i,read_write_col).text().upper() == 'READ':
                        readCount = readCount+1
                    else:
                        writeCount = writeCount+1
            return 'Total Read: {} and Write: {} instructions'.format(readCount, writeCount)
        
        except AttributeError:
            pass
        
    def data_bytes_transfer_avg(self, data) -> int:
        try:
            total_bytes = 0
            count_bytes = 0
            data_bytes_col = self.get_column_index("Number of data bytes", data)
            for i in range(data.rowCount()):
                if data.isRowHidden(i):
                    pass
                else:
                    total_bytes = total_bytes+int(data.item(i, data_bytes_col).text())
                    count_bytes = count_bytes+1
            return total_bytes/count_bytes
        
        except AttributeError:
            pass
        
    def txn_time_diff_avg(self, data) -> int:
        try:
            total_txn_time_diff = 0
            total_count = 0
            end_time_col = self.get_column_index("Txn End time (ns)", data)
            for i in range(data.rowCount()):
                if data.isRowHidden(i):
                    pass
                else:
                    total_txn_time_diff = total_txn_time_diff + (int(data.item(i, end_time_col).text())-int(data.item(i, end_time_col-1).text()))
                    total_count = total_count+1
            return total_txn_time_diff/total_count
        
        except AttributeError:
            pass
        
    def total_fixed_incr(self, data) -> str:
        try:
            total_fixed = 0
            total_incr = 0
            address_type_col = self.get_column_index("Address_type", data)
            for i in range(data.rowCount()):
                if data.isRowHidden(i):
                    pass
                else:
                    if data.item(i, address_type_col).text().upper() == "FIXED":
                        total_fixed = total_fixed+1
                    else:
                        total_incr = total_incr+1
                    
            return 'Total Fixed: {} and INCR: {} instructions'.format(total_fixed, total_incr)
        
        except AttributeError:
            pass
        
    def bandwidthInfo(self, data) -> str:
        try:
            end_time_col = self.get_column_index("Txn End time (ns)", data)
            total_bytes_col = self.get_column_index("Number of data bytes", data)
            total_bytes = 0
            rows = 0
            for row in range(data.rowCount()):
                if data.isRowHidden(row):
                    pass
                else:
                    rows = rows + 1
                    end_time = int(data.item(row, end_time_col).text())
                    total_bytes = total_bytes + int(data.item(row, total_bytes_col).text())
            
            band_address = rows/(end_time-int(data.item(0,end_time_col-1).text()))
            band_data = total_bytes/(end_time-int(data.item(0,end_time_col-1).text()))
            
            return 'Bandwidth of address usage: {:.2f}\nBandwidth of data transfers: {:.2f}'.format(band_address, band_data)
        
        except AttributeError:
            pass