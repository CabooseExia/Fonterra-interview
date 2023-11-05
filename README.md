# Fonterra-interview
create insights to protien martket in Thailand

yea so for the first part, I want to see the distribution of proteins, carbs and fats in thailand

second, i want to see the distribution of sources of protein in thailand - i might need to find more data online....

third i gotta see what the culture is like there, do they even gym bruh

data finding:
https://inmu2.mahidol.ac.th/thaifcd/home.php -> no info on quantity
https://www.globaldietarydatabase.org/ -> looks like we gna use this


planning for grouping to see distributions:

Consulted Mal, thanks Mal
6 groups
1. Protien
2. Carbs
3. Fats
4. Vitamins (gna ignore)
5. Minerals (gna ignore)
6. Water (gna ignore)

the units are all messed up, i want to convert it to Grams/day, but looking at the si-units for some of the groups, 
vitamins and minerals i prob won't care about because its all milligrams and micrograms and they dont have protein in them anyways , 
water can only care about total_milk later on as the rest do not have protein


total proteins is alr nice

bruh carbs:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7230657/#:~:text=3.2.-,Energy%20Intake,1566%20kcal%2Fd%20for%20women.
men 2k/day (rounded)
woman 1.5k/day (rounded)
need to take % of that times 0.129598 to get grams/day
carbs should be settled
gender distribution in thailand is about 50.6% to 49.4%, i'll just round to 50/50

bruh fats???
ok looks like majority of it should be saturated and unsaturated
saturated is settled...
unsaturated...
found 4 
v28	Monounsaturated fatty acids
v29	Total omega-6 fat
v30	Seafood omega-3 fat
v31	Plant omega-3 fat

['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'median', 'upperci_95', 'lowerci_95']


my combined df will have these columns:
['superregion2', 'iso3', 'age', 'female', 'urban', 'edu', 'year', 'varnum', 'v22_type', 'v22_type_desc', 'p_median', 'p_upperci_95', 'p_lowerci_95', 'c_median', 'c_upperci_95', 'c_lowerci_95', 'f_median', 'f_upperci_95', 'f_lowerci_95']


for age, index is:
['0-11 mo.', '12-23 mo.', '2-5 years', '6-10 years', '11-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85-89 years', '90-94 years', '95+ years]