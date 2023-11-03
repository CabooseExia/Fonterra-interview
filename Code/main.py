import pdb
import pandas as pd
import csv
import xlwings as xw
import os

### Paths ###
main_path = "C://Users//caboo//Documents//Fonterra-interview//data"
gdd_data_path = f'{main_path}//GDD_FinalEstimates_01102022//Country-level estimates'
### Paths ###

#### constants ####
Locations = ["THA",] #Thailand
Protein = ["v23",]
Carbs = ["v22",]
Fats = ['v28', 'v29', 'v30', 'v31']
Impt_files = Protein + Carbs + Fats
#### constants ####




def general_dict_maker(file, coords): #donzo
    dict = {}
    df = file.range(coords).value 
    for entry in df:
        dict[entry[1]] = entry[0]
    return dict


def dict_maker(): #basic setup for later cleaning
    codebook_path = "C://Users//caboo//Documents//Fonterra-interview//data//GDD_FinalEstimates_01102022//GDD 2018 Codebook_Jan 10 2022.xlsx"
    codebook = xw.Book(codebook_path).sheets['Stratum-level characteristics']

    ### for age
    global age_dict 
    age_dict = general_dict_maker(codebook, "G3:H25")

    ### for edu_level
    global edu_level_dict
    edu_level_dict = general_dict_maker(codebook, "J3:K6")

    ### for residence
    global resi_dict
    resi_dict = general_dict_maker(codebook, "M3:N5")

    ### for gender
    global gender_dict
    gender_dict = general_dict_maker(codebook, "P3:Q5")


def location_selecter(csv_name):
    csv_dir = f'{gdd_data_path}//{csv_name}'
    output_location = f'{gdd_data_path}//data_at_location//{csv_name}'
    data_at_location = open(f'{output_location}', 'w', newline='')
    writer = csv.writer(data_at_location)

    with open(csv_dir, 'r') as csv_file:
        csv_read = csv.reader(csv_file)
        for row in csv_read:
            if row[1] in Locations:
                # data_by_location.append(row) #keep all data? i feel like some can throw away... maybe clean more later
                writer.writerow(row)
        data_at_location.close()

        





if __name__ == "__main__":
    dict_maker()

    
    # pdb.set_trace()
    raw_files = os.listdir(gdd_data_path)
    for file in raw_files:
        if file[0:3] in Impt_files:
            location_selecter(file)

    print("it ran")

