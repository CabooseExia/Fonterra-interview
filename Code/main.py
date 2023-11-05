import pdb
import pandas as pd
import csv
import xlwings as xw
import os
import matplotlib.pyplot as plt

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
Proteins = ['v05', 'v06','v08', 'v09', 'v10', 'v11', 'v12', 'v13', 'v14']
Impt_files = Protein + Carbs + Fats
#### constants ####




def general_dict_maker(file, coords): #donzo
    dict = {}
    df = file.range(coords).value 
    index = []
    for entry in df:
        dict[entry[1]] = entry[0]
        index.append(entry[0])
    # print(index)
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
        header = next(csv_read)
        writer.writerow(header)
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
    with open(csv_file_path, 'r') as csv_read, open(temp, 'w', newline='') as csv_out: #i didnt know you could do this... cool
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

def fats_combiner(): #man... ok i want to make this better so i can re-use this code for other cases... just not now... too much work, rn it shall only work for this case
    cleaned_files = os.listdir(cleaned_file_path)
    temp = f'{gdd_data_path}//data_at_location//temp.csv'
    # with open(csv_file_path, 'r+') as csv_read, open(temp, 'w', newline='') as csv_out:
    # with open(temp, 'w', newline='') as csv_out:
    #     csv_write = csv.writer(csv_out)
    # temp_data = [[]]
    # for file in cleaned_files:
    #     if file[0:3] in Fats:
    #         print(file)
    #         with open(f'{cleaned_file_path}//{file}', 'r') as csv_read:
    #             csv_read = csv.reader(csv_read)
    #             for row in csv_read:
    #                 temp_data.append
    #                 pdb.set_trace()
    v28_df = pd.read_csv(f'{cleaned_file_path}//v28_cnty.csv')
    v29_df = pd.read_csv(f'{cleaned_file_path}//v29_cnty.csv')
    v30_df = pd.read_csv(f'{cleaned_file_path}//v30_cnty.csv')
    v31_df = pd.read_csv(f'{cleaned_file_path}//v31_cnty.csv')
    v28_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'f_median', 'f_upperci_95', 'f_lowerci_95']
    v29_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'f_median', 'f_upperci_95', 'f_lowerci_95']
    v30_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'f_median', 'f_upperci_95', 'f_lowerci_95']
    v31_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'f_median', 'f_upperci_95', 'f_lowerci_95']
    # print(list(v28_df.columns[:10].tolist()))
    # test = pd.merge(v28_df, v29_df, on=list(v28_df.columns[:10].tolist()))
    # test.to_string()
    # print(v28_df)
    v28_last_3_df = v28_df.iloc[:, -3:]
    v29_last_3_df = v29_df.iloc[:, -3:]
    v30_last_3_df = v30_df.iloc[:, -3:]
    v31_last_3_df = v31_df.iloc[:, -3:]

    grams = v28_last_3_df + v29_last_3_df + v30_last_3_df + v31_last_3_df
    # print(grams)
    fats_df = pd.merge(v28_df.iloc[:, :9], grams, right_index=True, left_index=True) #god damnit i think concat works for this
    # print(fats_df)
    fats_df.to_csv(f'{cleaned_file_path}//combined_fats.csv', sep=',', index=False, encoding='utf-8')
                    

def step_1():
    #man the playing with data frames part seems fun... so much easier... should just use r honestly lol

    #i need to only care abt everyone all over the years, set to 999 for all ig
    protein_df = pd.read_csv(f'{cleaned_file_path}//v23_cnty.csv')
    protein_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_median', 'p_upperci_95', 'p_lowerci_95']
    carbs_df = pd.read_csv(f'{cleaned_file_path}//v22_cnty.csv')
    carbs_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'c_median', 'c_upperci_95', 'c_lowerci_95']
    carbs_data_df = carbs_df.iloc[:, -3:]
    fats_df = pd.read_csv(f'{cleaned_file_path}//combined_fats.csv')
    fats_data_df = fats_df.iloc[:, -3:]

    # all_df = pd.merge(protein_df, carbs_df, on=['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc'])
    all_df = pd.merge(protein_df, carbs_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, fats_data_df, right_index=True, left_index=True)
    # print(all_df)
    
    ### MARKET CHECK ###
    age_condition = all_df['age'] == 999
    sex_condition = all_df['female'] == 999
    urban_condition = all_df['urban'] == 999
    edu_condition = all_df['edu'] == 999

    step_1_df = all_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition)]
    # print(step_1_df.columns.to_list())
    step_1_df = step_1_df.drop(['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'varnum', 'v22_type', 'v22_type_desc', 'p_upperci_95', 'p_lowerci_95', 'c_upperci_95', 'c_lowerci_95', 'f_upperci_95', 'f_lowerci_95'], axis=1)
    # # print(step_1_df)
    step_1_df.set_index('year', inplace=True)
    ax = step_1_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    plt.xlabel('Year')
    plt.ylabel('Grams per day')
    plt.show()

    ### Ages? ### 
    print(age_dict)
    age_condition = all_df['age'] != 999
    sex_condition = all_df['female'] == 999
    urban_condition = all_df['urban'] == 999
    edu_condition = all_df['edu'] == 999
    year_condition = all_df['year'] == 2018

    step_1_df = all_df[(year_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (age_condition)]
    # print(step_1_df.columns.to_list())
    step_1_df = step_1_df.drop(['superregion2', 'iso3', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_upperci_95', 'p_lowerci_95', 'c_median', 'c_upperci_95', 'c_lowerci_95', 'f_median', 'f_upperci_95', 'f_lowerci_95'], axis=1)
    # pdb.set_trace()
    step_1_df['age'] = step_1_df['age'].map(age_dict)
    step_1_df.set_index('age', inplace=True)
    # step_1_df = step_1_df.reindex(['0-11 mo.', '12-23 mo.', '2-5 years', '6-10 years', '11-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85-89 years', '90-94 years', '95+ years'])
    # print(step_1_df)
    ax = step_1_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    plt.xlabel('Age')
    plt.ylabel('Grams per day')
    plt.show()


    ### GENDER ###
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] != 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2018

    # step_1_df = all_df[(year_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (age_condition)]
    # # print(step_1_df.columns.to_list())
    # step_1_df = step_1_df.drop(['superregion2', 'iso3', 'age', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_upperci_95', 'p_lowerci_95', 'c_median', 'c_upperci_95', 'c_lowerci_95', 'f_median', 'f_upperci_95', 'f_lowerci_95'], axis=1)
    # # pdb.set_trace()
    # step_1_df['female'] = step_1_df['female'].map(gender_dict)
    # step_1_df.set_index('female', inplace=True)
    # # step_1_df = step_1_df.reindex(['0-11 mo.', '12-23 mo.', '2-5 years', '6-10 years', '11-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85-89 years', '90-94 years', '95+ years'])
    # # print(step_1_df)
    # ax = step_1_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Gender')
    # plt.ylabel('Grams per day')
    # plt.show()

    ### housing type ###
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] != 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2018

    # step_1_df = all_df[(year_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (age_condition)]
    # # print(step_1_df.columns.to_list())
    # step_1_df = step_1_df.drop(['superregion2', 'iso3', 'age', 'female', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_upperci_95', 'p_lowerci_95', 'c_median', 'c_upperci_95', 'c_lowerci_95', 'f_median', 'f_upperci_95', 'f_lowerci_95'], axis=1)
    # # pdb.set_trace()
    # step_1_df['urban'] = step_1_df['urban'].map(resi_dict)
    # step_1_df.set_index('urban', inplace=True)
    # # step_1_df = step_1_df.reindex(['0-11 mo.', '12-23 mo.', '2-5 years', '6-10 years', '11-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85-89 years', '90-94 years', '95+ years'])
    # # print(step_1_df)
    # ax = step_1_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Resident type')
    # plt.ylabel('Grams per day')
    # plt.show()

    ### EDUCATION LEVEL ###
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] != 999
    # year_condition = all_df['year'] == 2018

    # step_1_df = all_df[(year_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (age_condition)]
    # # print(step_1_df.columns.to_list())
    # step_1_df = step_1_df.drop(['superregion2', 'iso3', 'age', 'female', 'urban', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_upperci_95', 'p_lowerci_95', 'c_median', 'c_upperci_95', 'c_lowerci_95', 'f_median', 'f_upperci_95', 'f_lowerci_95'], axis=1)
    # # pdb.set_trace()
    # step_1_df['edu'] = step_1_df['edu'].map(edu_level_dict)
    # step_1_df.set_index('edu', inplace=True)
    # # step_1_df = step_1_df.reindex(['0-11 mo.', '12-23 mo.', '2-5 years', '6-10 years', '11-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85-89 years', '90-94 years', '95+ years'])
    # # print(step_1_df)
    # ax = step_1_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Education level')
    # plt.ylabel('Grams per day')
    # plt.xticks(rotation=0)
    # plt.show()

def step_2():#im sorry, more spam... I am doing this like this is r...
    beans_and_legumes_df = pd.read_csv(f'{cleaned_file_path}//v05_cnty.csv')
    nuts_and_seeds_df = pd.read_csv(f'{cleaned_file_path}//v06_cnty.csv')
    whole_grains_df = pd.read_csv(f'{cleaned_file_path}//v08_cnty.csv')
    processed_meats_df = pd.read_csv(f'{cleaned_file_path}//v09_cnty.csv')
    unprocessed_meats_df = pd.read_csv(f'{cleaned_file_path}//v10_cnty.csv')
    seafoods_df = pd.read_csv(f'{cleaned_file_path}//v11_cnty.csv')
    eggs_df = pd.read_csv(f'{cleaned_file_path}//v12_cnty.csv')
    cheese_df = pd.read_csv(f'{cleaned_file_path}//v13_cnty.csv')
    yogurt_df = pd.read_csv(f'{cleaned_file_path}//v14_cnty.csv')

    beans_and_legumes_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'beans_and_legumes_median', 'beans_and_legumes_upperci_95', 'beans_and_legumes_lowerci_95','beans_and_legumes_serving', 'beans_and_legumes_s_lowerci_95', 'beans_and_legumes_s_upperci_95']
    nuts_and_seeds_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'nuts_and_seeds_median', 'nuts_and_seeds_upperci_95', 'nuts_and_seeds_lowerci_95','nuts_and_seeds_serving', 'nuts_and_seeds_s_lowerci_95', 'nuts_and_seeds_s_upperci_95']
    whole_grains_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', ' whole_grains_median', ' whole_grains_upperci_95', ' whole_grains_lowerci_95','whole_grains_serving', 'whole_grains_s_lowerci_95', 'whole_grains_s_upperci_95']
    processed_meats_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'processed_meats_median', 'processed_meats_upperci_95', 'processed_meats_lowerci_95', 'processed_meats_serving', 'processed_meats_s_lowerci_95', 'processed_meats_s_upperci_95']
    unprocessed_meats_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'v22_type', 'v22_type_desc', 'unprocessed_meats_median', 'unprocessed_meats_upperci_95', 'unprocessed_meats_lowerci_95', 'unprocessed_meats_serving', 'unprocessed_meats_s_lowerci_95', 'unprocessed_meats_s_upperci_95']
    seafoods_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'seafoods_median', 'seafoods_upperci_95', 'seafoods_lowerci_95', 'seafoods_serving', 'seafoods_s_lowerci_95', 'seafoods_s_upperci_95']
    eggs_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'eggs_median', 'eggs_upperci_95', 'eggs_lowerci_95', 'eggs_serving', 'eggs_s_lowerci_95', 'eggs_s_upperci_95']
    cheese_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'cheese_median', 'cheese_upperci_95', 'cheese_lowerci_95', 'cheese_serving', 'cheese_s_lowerci_95', 'cheese_s_upperci_95']
    yogurt_df.columns = ['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'yogurt_median', 'yogurt_upperci_95', 'yogurt_lowerci_95', 'yogurt_serving', 'yogurt_s_lowerci_95', 'yogurt_upperci_95']

    nuts_and_seeds_data_df = nuts_and_seeds_df.iloc[:, -6:]
    whole_grains_data_df = whole_grains_df.iloc[:, -6:]
    processed_meats_data_df = processed_meats_df.iloc[:, -6:]
    # unprocessed_meats_data_df = unprocessed_meats_df.iloc[:, -6:]
    seafoods_data_df = seafoods_df.iloc[:, -6:]
    eggs_data_df = eggs_df.iloc[:, -6:]
    cheese_data_df = cheese_df.iloc[:, -6:]
    yogurt_data_df =  yogurt_df.iloc[:, -6:]

    all_df = pd.merge(beans_and_legumes_df, nuts_and_seeds_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, whole_grains_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, processed_meats_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, unprocessed_meats_df, on=['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'v22_type', 'v22_type_desc'], how='left') # u are the problem...... ok my dsa2101 is coming back to me now :)
    # pdb.set_trace()
    all_df = pd.merge(all_df, seafoods_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, eggs_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, cheese_data_df, right_index=True, left_index=True)
    all_df = pd.merge(all_df, yogurt_data_df, right_index=True, left_index=True)
    # print(all_df)

    print(all_df.columns.to_list())
    # pdb.set_trace()
    cols_to_drop = ['superregion2', 'iso3', 'varnum', 'v22_type', 'v22_type_desc', 
                    'beans_and_legumes_median', 'beans_and_legumes_upperci_95', 'beans_and_legumes_lowerci_95', 'beans_and_legumes_s_lowerci_95', 'beans_and_legumes_s_upperci_95', 
                    'nuts_and_seeds_median', 'nuts_and_seeds_upperci_95', 'nuts_and_seeds_lowerci_95', 'nuts_and_seeds_s_lowerci_95', 'nuts_and_seeds_s_upperci_95',
                    ' whole_grains_median', ' whole_grains_upperci_95', ' whole_grains_lowerci_95', 'whole_grains_s_lowerci_95', 'whole_grains_s_upperci_95', 
                    'processed_meats_median', 'processed_meats_upperci_95', 'processed_meats_lowerci_95', 'processed_meats_s_lowerci_95', 'processed_meats_s_upperci_95',
                    'unprocessed_meats_median', 'unprocessed_meats_upperci_95', 'unprocessed_meats_lowerci_95', 'unprocessed_meats_s_lowerci_95', 'unprocessed_meats_s_upperci_95',
                    'seafoods_median', 'seafoods_upperci_95', 'seafoods_lowerci_95', 'seafoods_s_lowerci_95', 'seafoods_s_upperci_95', 
                    'eggs_median', 'eggs_upperci_95', 'eggs_lowerci_95', 'eggs_s_lowerci_95', 'eggs_s_upperci_95', 
                    'cheese_median', 'cheese_upperci_95', 'cheese_lowerci_95', 'cheese_s_lowerci_95', 'cheese_s_upperci_95', 
                    'yogurt_median', 'yogurt_upperci_95', 'yogurt_lowerci_95', 'yogurt_s_lowerci_95', 'yogurt_upperci_95']
    cleaned_df = all_df.drop(cols_to_drop, axis=1)
    print(cleaned_df)

    ###   main   ###
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] == 999
    # # year_condition = all_df['year'] == 2018

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition)]
    # cleaned_df = cleaned_df.drop(['age', 'female', 'urban', 'edu'], axis=1)
    # grouped = cleaned_df.groupby('year')

    # for year, data in grouped:
    #     # pdb.set_trace()
        
    #     labels = ['Beans and legumes', 'Nuts and seeds', 'Whole grains', 'Total processed meats', 'Unprocessed red meats', 'Total seafoods', 'Eggs', 'Cheese', 'Yoghurt']
    #     sizes = [data['beans_and_legumes_serving'].values[0], data['nuts_and_seeds_serving'].values[0], data['whole_grains_serving'].values[0], data['processed_meats_serving'].values[0], data['unprocessed_meats_serving'].values[0], data['seafoods_serving'].values[0], data['eggs_serving'].values[0], data['cheese_serving'].values[0], data['yogurt_serving'].values[0]]
    #     plt.figure()
    #     plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

    #     plt.title(year)

    # plt.show()


    ### 2018 age
    # age_condition = all_df['age'] != 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2018

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (year_condition)]
    # cleaned_df = cleaned_df.drop(['year', 'female', 'urban', 'edu'], axis=1)

    # cleaned_df['age'] = cleaned_df['age'].map(age_dict)
    # cleaned_df.set_index('age', inplace=True)
    # ax = cleaned_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Age')
    # plt.ylabel('Grams per day')
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.show()

    ### 2018 gender
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] != 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2010

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (year_condition)]
    # cleaned_df = cleaned_df.drop(['year', 'age', 'urban', 'edu'], axis=1)
 
    # cleaned_df['female'] = cleaned_df['female'].map(gender_dict)
    # cleaned_df.set_index('female', inplace=True)
    # ax = cleaned_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Gender')
    # plt.ylabel('Grams per day')
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.show()


    ### 2018 urban 
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] != 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2010

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (year_condition)]
    # cleaned_df = cleaned_df.drop(['year', 'age', 'female', 'edu'], axis=1)

    # cleaned_df['urban'] = cleaned_df['urban'].map(resi_dict)
    # cleaned_df.set_index('urban', inplace=True)
    # ax = cleaned_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Housing type')
    # plt.ylabel('Grams per day')
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.show()

    ### 2010 education
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] != 999
    # year_condition = all_df['year'] == 2018

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (year_condition)]
    # cleaned_df = cleaned_df.drop(['year', 'age', 'female', 'urban'], axis=1)

    # cleaned_df['edu'] = cleaned_df['edu'].map(edu_level_dict)
    # cleaned_df.set_index('edu', inplace=True)
    # ax = cleaned_df.plot(kind='bar', stacked=False, figsize=(10, 6))
    # plt.xlabel('Education Level')
    # plt.ylabel('Grams per day')
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.xticks(rotation=0)
    # plt.show()


    ###double checking
    # age_condition = all_df['age'] == 999
    # sex_condition = all_df['female'] == 999
    # urban_condition = all_df['urban'] == 999
    # edu_condition = all_df['edu'] == 999
    # year_condition = all_df['year'] == 2018

    # cleaned_df = cleaned_df[(age_condition) & (sex_condition) & (urban_condition) & (edu_condition) & (year_condition)]

    # print(beans_and_legumes_df)




if __name__ == "__main__":

    #set_up
    dict_maker()

    ##### DATA CLEANING for step 1#####
    # ### for creating location specific data
    # raw_files = os.listdir(gdd_data_path) # nice, we did this....
    # for file in raw_files:
    #     if file[0:3] in Impt_files:
    #         location_selecter(file)


    # #convert everything to grams per day and combine the fats
    # #protein alr nice
    # #need to do total carbs
    # carb_cleaner() #donzo

    # #fats is a problem. first need to make all same units then can combine
    # fats_in_kcal = ['v28', 'v29']
    # fats_in_milli = ['v30', 'v31']
    # indiv_fat_cleaner(fats_in_kcal, fats_in_milli)
    # fats_combiner()

    #ok step 1: distribution. 
    step_1() 

       ##### DATA CLEANING for step 2#####
    #step 2, what kinda proteins do ppl eat the most? 
    # raw_files = os.listdir(gdd_data_path) # nice, we did this....
    # for file in raw_files:
    #     if file[0:3] in Proteins:
    #         location_selecter(file)

    step_2()



    print("it ran")