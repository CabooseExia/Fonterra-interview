import pdb
import pandas as pd
import csv
import xlwings as xw

### Paths ###
main_path = "C://Users//caboo//Documents//Fonterra-interview//data"
data_path = main_path + '//GDD_FinalEstimates_01102022'
### Paths ###

#### Vars ####
locations = ["THA",] #Thailand
#### Vars ####



def dict_maker():
    coodbook_path = "C://Users//caboo//Documents//Fonterra-interview//data//GDD_FinalEstimates_01102022//GDD 2018 Codebook_Jan 10 2022.xlsx"
    codebook = xw.Book(coodbook_path).sheets['Stratum-level characteristics']
    # print(codebook.sheet_names)
    age_dict = {}
    age_df = codebook.range("G3:H25").value 
    for entry in age_df:
        age_dict[entry[1]] = entry[0]
        pdb.set_trace()

    # print(age_df)

if __name__ == "__main__":
    pass
    dict_maker()
    # print(data_path)

