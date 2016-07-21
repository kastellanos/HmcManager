import pandas as pd

class ExcelUtil(object):
    def __init__(self,output) :
        self.sheets = []
        self.file_path=None
        self.file_name=None
        self.output = output
    def add(self, sheet_index,sheet_column,sheet_data, sheet_name ):
        tmp_df = (pd.DataFrame(sheet_data,sheet_index,columns=sheet_column),sheet_name)


        self.sheets.append(tmp_df )

    def writeExcel(self):
        if len(self.sheets)>0:
            writer = pd.ExcelWriter(self.output,engine="xlsxwriter")
            for df,name in self.sheets:
                print(name)
                df.to_excel(writer,name)
            writer.save()

        else:
            print( "No data to write")