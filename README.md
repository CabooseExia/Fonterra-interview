# Fonterra-interview
create insights to protien martket in Thailand

yea so for the first part, I want to see the distribution of proteins, carbs and fats eaten by the people in thailand

second, i want to see the distribution of sources of protein in thailand - i might need to find more data online.... no we good

third i gotta see what the culture is like there, do they even gym bruh

data finding:
https://inmu2.mahidol.ac.th/thaifcd/home.php -> no info on quantity
https://www.globaldietarydatabase.org/ -> looks like we gna use this


1. planning for grouping to see distributions:

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



2. now i want to check the distribution. I think i'll focus on 2018 as it is the most recent. 

current groups of interest are:
v05	Beans and legumes
v06	Nuts and seeds
v08	Whole grains
v09	Total processed meats
v10	Unprocessed red meats
v11	Total seafoods
v12	Eggs
v13	Cheese
v14	Yoghurt (including fermented milk)

weird those with no total have mean.

ok... i know i can prob automate this. but imma brute force this. 



3. from searching online, there is some gymming culture? but only in like specific cities. Can't really say much