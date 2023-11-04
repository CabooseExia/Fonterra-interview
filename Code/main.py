import pdb
import pandas as pd
import csv
import xlwings as xw
import os

### Paths ###
main_path = "C://Users//caboo//Documents//Fonterra-interview//data"
gdd_data_path = f'{main_path}//GDD_FinalEstimates_01102022//Country-level estimates'
cleaned_file_path = f'{gdd_data_path}//data_at_location'
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


def convert_kcal_to_gpd(csv_file_path):
    temp = f'{gdd_data_path}//data_at_location//temp.csv'
    with open(csv_file_path, 'r+') as csv_read, open(temp, 'w', newline='') as csv_out: #i didnt know you could do this... cool
        csv_read = csv.reader(csv_read)
        csv_write = csv.writer(csv_out)

        for row in csv_read:
            if row[3] == '0': # if its male
                base_cals = 2000
            elif row[3] == '1':
                base_cals = 1500
            else:
                base_cals = 1750

            med = base_cals * float(row[10]) / 100 * 0.129598 #median
            upp = base_cals * float(row[11]) / 100 * 0.129598 #upper
            low = base_cals * float(row[12]) / 100 * 0.129598 #lower

            output_row = row[0:10]
            output_row.append(med)
            output_row.append(upp)
            output_row.append(low)
            
            csv_write.writerow(output_row)

            # pdb.set_trace()
    os.remove(csv_file_path)
    os.rename(temp, csv_file_path)


def convert_milligram_to_gpd(csv_file_path):
    temp = f'{gdd_data_path}//data_at_location//temp.csv'
    with open(csv_file_path, 'r+') as csv_read, open(temp, 'w', newline='') as csv_out: #i didnt know you could do this... cool
        csv_read = csv.reader(csv_read)
        csv_write = csv.writer(csv_out)

        for row in csv_read:
       
            med = float(row[10]) * 0.001 #median
            upp = float(row[11]) * 0.001 #upper
            low = float(row[12]) * 0.001 #lower

            output_row = row[0:10]
            output_row.append(med)
            output_row.append(upp)
            output_row.append(low)
            
            csv_write.writerow(output_row)

            # pdb.set_trace()
    os.remove(csv_file_path)
    os.rename(temp, csv_file_path)



def carb_cleaner():
    cleaned_files = os.listdir(f'{gdd_data_path}//data_at_location')
    for file in cleaned_files:
        if file[0:3] in Carbs:
            convert_kcal_to_gpd(f'{gdd_data_path}//data_at_location//{file}')


def indiv_fat_cleaner(list_of_kcal, list_of_milli):
    cleaned_files = os.listdir(cleaned_file_path)
    for file in cleaned_files:
        if file[0:3] in list_of_kcal:
            convert_kcal_to_gpd(f'{gdd_data_path}//data_at_location//{file}')
        elif file[0:3] in list_of_milli:
            convert_milligram_to_gpd(f'{gdd_data_path}//data_at_location//{file}')







if __name__ == "__main__":

    #set_up
    dict_maker()

    ### for creating location specific data
    raw_files = os.listdir(gdd_data_path) # nice, we did this....
    for file in raw_files:
        if file[0:3] in Impt_files:
            location_selecter(file)


    #convert everything to grams per day and combine the fats
    #protein alr nice
    #need to do total carbs
    carb_cleaner() #donzo

    #fats is a problem. first need to make all same units then can combine
    fats_in_kcal = ['v28', 'v29']
    fats_in_milli = ['v30', 'v31']
    indiv_fat_cleaner(fats_in_kcal, fats_in_milli)


    #ok step 1: distribution. not so fast...

    print("it ran")

