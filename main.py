import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash
import plotly.io as pio
from dash import dash_table
import os
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)

pd.options.mode.chained_assignment = None

paf = 'edit here'
name = 'items.csv'
file_path = os.path.join(paf, name)


# program to calculate usage of liquors
# read in csv to master data frame
ddf = pd.read_csv(file_path, header=1)

# read master dataframe into main frame
df = ddf
df = df.drop('SKU', axis=1)
# Remove the "$" character from the "Net" and "Gross" columns
df['Net'] = df['Net'].replace('\$', '', regex=True)
df['Gross'] = df['Gross'].replace('\$', '', regex=True)
# Convert commas to period
df['Net'] = df['Net'].replace('\,', '', regex=True)
df['Gross'] = df['Gross'].str.replace('\,', '', regex=True)


# Convert the "Net" and "Gross" columns to float
df['Net'] = df['Net'].astype(float)
df['Gross'] = df['Gross'].astype(float)


# group mainframe into sub-frames
# "FOOD", "ALCOHOL", "WINE", "DRAFT BEER", "NON ALCOHOL", "MERCH--TSHIRTS", "MERCH-- MUGS"
grouped = df.groupby('Report Category')

# Iterate over the groups and create a new DataFrame for each group
for name, group in grouped:
    new_df = pd.DataFrame(group)

# set dataframes from food
food_df = grouped.get_group('FOOD')

# drop size from food as its empty and only for alcohol
food_df = food_df.drop('Size', axis=1)

alc_df = grouped.get_group('ALCOHOL')
wine_df = grouped.get_group('WINE')
draftbeer_df = grouped.get_group('DRAFT BEER')
beer_df = grouped.get_group('BEER')
nalc_df = grouped.get_group('NON ALCOHOL')
shirt_df = grouped.get_group('MERCH--TSHIRTS')
mug_df = grouped.get_group('MERCH-- MUGS')
gift_df = grouped.get_group('GIFT CARDS & CERTS')

# load alcohol into data frame
# csv containing cocktail names used by pos are imported
# and then their item column is put into list
cocktails_dff = pd.read_csv('cocktails.csv')
cocktails_item = cocktails_dff['Item'].tolist()

gin_dff = pd.read_csv('gin.csv')
gin_items = gin_dff['Item'].tolist()

whiskey_dff = pd.read_csv('whiskey.csv')
whiskey_items = whiskey_dff['Item'].tolist()


rum_dff = pd.read_csv('rum.csv')
rum_items = rum_dff['Item'].tolist()


vodka_dff = pd.read_csv('vodka.csv')
vodka_items = vodka_dff['Item'].tolist()


tequila_dff = pd.read_csv('tequila.csv')
tequila_items = tequila_dff['Item'].tolist()


otherliq = pd.read_csv('otherliquor.csv')
otherliq_items = otherliq['Item'].tolist()


mocktail_dff = pd.read_csv('nalc.csv')
mocktail_items = mocktail_dff['Item'].tolist()


sodajuice_dff = pd.read_csv('bev.csv')
bev_items = sodajuice_dff['Item'].tolist()

secret_items = ['Fool\'s Gold', 'Smoke &  Embers', 'Satellite', 'Martinique Swizzle', 'Puka Punch',
                'Blackbeard\'s Ghost', 'Zombie', 'Port Light']
# after putting it into a list, we will compare locations in our alcohol subframe
# parsing through our item lists we then set a new column in df['type']
#alc_df = alc_df.loc[:'type'] = 'other'
alc_df = alc_df.copy()
alc_df.loc[:, 'type'] = 'other'

alc_df.loc[alc_df['Item'].isin(whiskey_items), 'type'] = "whiskey"
alc_df.loc[alc_df['Item'].isin(mocktail_items), 'type'] = "mocktail"
alc_df.loc[alc_df['Item'].isin(vodka_items), 'type'] = "vodka"
alc_df.loc[alc_df['Item'].isin(gin_items), 'type'] = "gin"
alc_df.loc[alc_df['Item'].isin(rum_items), 'type'] = "rum"
alc_df.loc[alc_df['Item'].isin(tequila_items), 'type'] = "tequila"
alc_df.loc[alc_df['Item'].isin(cocktails_item), 'type'] = "cocktail"
alc_df.loc[alc_df['Item'].isin(secret_items), 'type'] = "secret"

# we then group by type
grouped = alc_df.groupby('type')

vodka_df = grouped.get_group('vodka')
whiskey_df = grouped.get_group('whiskey')
gin_df = grouped.get_group('gin')
rum_df = grouped.get_group('rum')
tequila_df = grouped.get_group('tequila')
cocktail_df = grouped.get_group('cocktail')
mocktail_df = grouped.get_group('mocktail')
other_df = grouped.get_group('other')
secret_df = grouped.get_group('secret')
# this grouping will leave cocktail names out
# program currently designed to track main usage
mrMakai = pd.DataFrame({'Item': ['Mr. Makai'], 'Size': ['DOUBLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0],
                        'Net': [0],
                        'Gross': [0], 'type': ['cocktail']})
mrMakaii = pd.DataFrame({'Item': ['Mr. Makai WITHOUT mug'], 'Size': ['DOUBLE'], 'Report Category': ['ALCOHOL'],
                         'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['cocktail']})
punch = pd.DataFrame({'Item': ['Punch To The Skull'], 'Size': ['DOUBLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0],
                      'Net': [0], 'Gross': [0], 'type': ['cocktail']})
punchwo = pd.DataFrame({'Item': ['Punch to the Skull WITHOUT jar'], 'Size': ['DOUBLE'], 'Report Category': ['ALCOHOL'],
                        'Qty': [0], 'Net': [0], 'Gross': [0], 'type': ['cocktail']})
cocktail_df = cocktail_df.append(punch, ignore_index=True)
cocktail_df = cocktail_df.append(punchwo, ignore_index=True)
cocktail_df = cocktail_df.append(mrMakai, ignore_index=True)
cocktail_df = cocktail_df.append(mrMakaii, ignore_index=False)
alcdataframes = [vodka_df, whiskey_df, gin_df, rum_df, tequila_df, cocktail_df, mocktail_df, other_df]
# set qty column to oz
for df in alcdataframes:

    df['Ounce'] = df.apply(lambda row: row['Qty'] * 3 if row['Size'] == 'DOUBLE' else row['Qty'] * 1.5,
                           axis=1)
    for i, row in df.iterrows():

        if row['Size'] == 'DOUBLE':
            df.at[i, 'Size'] = 'SINGLE'
        if pd.isna(row['Size']):
            df.at[i, 'Size'] = 'SINGLE'

    df = df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()

vodka_df = vodka_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
whiskey_df = whiskey_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
gin_df = gin_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
rum_df = rum_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
tequila_df = tequila_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
cocktail_df = cocktail_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
mocktail_dff = mocktail_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()
other_df = other_df.groupby(['Item', 'Size'])['Ounce', 'Qty', 'type', 'Net', 'Gross'].sum().reset_index()


# Load entrees.csv into a dataframe
entreess_df = pd.read_csv('entrees.csv')

# Get a list of all the items in the entrees.csv file
entree_items = entreess_df['Item'].tolist()
side_items = ['Bok Choy', 'Makai Mac Salad', 'Seismic Fries', 'SautÃ©ed Mixed Veggies', 'Pineapple Koolslaw',
              'Rice Side', 'Side Salad']

dessert_items = ['Banana Pudding', 'Kilauea Cake', 'Brulee', 'Coconut Gelato', 'Hula Pie Gelato', 'Mango Sorbet',
                 'Vanilla Ice Cream', 'Banana Pudding TOGO', 'Strawberry Passion Brulee']

kids_items = ['Kids Teriyaki Chicken', 'Buttered Macaroni', 'Chicken Tenders']
kids_items += ["Kid's Burger", "Kid's Corn Dog", "Kid's Pork Slider"]

pupu_items = ['Coconut Prawns', 'Hawaiian BBQ Pork Sliders', 'Spam Musubi', 'Aloha Boston Clam-Chowder- Cup',
              'Pulled Pork Island Nacho', 'Poke Stack', 'Edamame Bowl', 'Crab Rangoon', 'Ahi Sliders',
              'Chicken Lettuce Wraps', 'Sweet Chili Wings', 'Aloha Boston Clam-Chowder- Bowl',
              'Pupu Platter', 'Teriyaki Prawn Skewers', 'Guava-Soy Beef Skewers', 'Tofu Lettuce Wraps',
              'Teriyaki Vegetable Skewers']
pupu_items += ["Makai Surf n' Turf Skewer Combo"]
# Add a new column to food_df called 'type' and set it to 'pupu' by default
food_df['type'] = 'other'


# Set the 'type' column to 'entree' for rows where the 'Item' column is in the list of entree items
food_df.loc[food_df['Item'].isin(entree_items), 'type'] = 'entree'
food_df.loc[food_df['Item'].isin(side_items), 'type'] = 'side'
food_df.loc[food_df['Item'].isin(dessert_items), 'type'] = 'dessert'
food_df.loc[food_df['Item'].isin(kids_items), 'type'] = 'kids'
food_df.loc[food_df['Item'].isin(pupu_items), 'type'] = 'pupu'

foodgrouped = food_df.groupby('type')
for name, group in foodgrouped:
    new_df = pd.DataFrame(group)

entrees_df = foodgrouped.get_group('entree')
side_df = foodgrouped.get_group('side')
dessert_df = foodgrouped.get_group('dessert')
pupu_df = foodgrouped.get_group('pupu')
kids_df = foodgrouped.get_group('kids')

# sort data frames by qty
dataframes = [entrees_df, side_df, kids_df, dessert_df, pupu_df]
entrees_df = entrees_df.sort_values('Qty', ascending=False)
side_df = side_df.sort_values('Qty', ascending=False)
kids_df = kids_df.sort_values('Qty', ascending=False)
dessert_df = dessert_df.sort_values('Qty', ascending=False)
pupu_df = pupu_df.sort_values('Qty', ascending=False)
# ['vodka', 'whiskey', 'gin', 'rum', 'mocktail', 'cocktail', 'tequila']
vodka_df = vodka_df.sort_values('Qty', ascending=False)
whiskey_df = whiskey_df.sort_values('Qty', ascending=False)
gin_df = gin_df.sort_values('Qty', ascending=False)
rum_df = rum_df.sort_values('Qty', ascending=False)
tequila_df = tequila_df.sort_values('Qty', ascending=False)
mocktail_df = mocktail_df.sort_values('Qty', ascending=False)
cocktail_df = cocktail_df.sort_values('Qty', ascending=False)

# dataframe for juice/syrup trackage
juice_df = pd.DataFrame()
juice_df['Item'] = ['lime', 'pineapple', 'lemon', 'guava', 'blood', 'orange']
juice_df['Ounce'] = 0
syrups_df = pd.DataFrame()
syrups_df['Item'] = ['simple', 'hibiscus', 'coco', 'cindem', 'orangemang', 'passion', 'dragon',
                     'orgeat', 'finestorgeat', 'finestpassion', 'vanilla', 'lychee', 'grenadine']
syrups_df['Ounce'] = 0

# define missing values and add to df
new_row = pd.DataFrame({'Item': ['Neisson'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['rum'], 'Ounce': [0]})
rum_df = rum_df.append(new_row, ignore_index=True)
# define missing values and add to df
nnew_row = pd.DataFrame({'Item': ['pierreFerrand'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
nnew_rrow = pd.DataFrame({'Item': ['tripleSec'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
falernum = pd.DataFrame({'Item': ['falernum'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
apricot = pd.DataFrame({'Item': ['apricot'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
amaro = pd.DataFrame({'Item': ['amaro'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
aspdram = pd.DataFrame({'Item': ['dram'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
elderflower = pd.DataFrame({'Item': ['elderflower'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
macadamia = pd.DataFrame({'Item': ['macadamia'], 'Size': ['SINGLE'], 'Report Category': ['ALCOHOL'], 'Qty': [0], 'Net': [0],
                        'Gross': [0], 'type': ['other'], 'Ounce': [0]})
other_df = other_df.append(nnew_row, ignore_index=True)
other_df = other_df.append(nnew_rrow, ignore_index=True)
other_df = other_df.append(falernum, ignore_index=True)
other_df = other_df.append(apricot, ignore_index=True)
other_df = other_df.append(amaro, ignore_index=True)
other_df = other_df.append(aspdram, ignore_index=True)
other_df = other_df.append(elderflower, ignore_index=True)
other_df = other_df.append(macadamia, ignore_index=True)

for index, row in cocktail_df.iterrows():
    if row['Item'] == '1944 MAI TAI':
        qty = row['Qty']
        syrups_df.loc[syrups_df['Item'] == 'simple', 'Ounce'] += qty * .25
        syrups_df.loc[syrups_df['Item'] == 'orgeat', 'Ounce'] += qty * .25
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * 1
        rum_df.loc[(rum_df['Item'] == 'Plantation Xaymaca') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        rum_df.loc[(rum_df['Item'] == 'Neisson') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'pierreFerrand') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5

    if row['Item'] == 'Painkiller':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Pusser\'s Navy') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 2
        syrups_df.loc[syrups_df['Item'] == 'coco', 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * 4
        juice_df.loc[juice_df['Item'] == 'orange', 'Ounce'] += qty * 1

    if row['Item'] == 'Dragon\'s Bite':
        qty = row['Qty']
        vodka_df.loc[(vodka_df['Item'] == 'Luna Sea') & (vodka_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 2
        syrups_df.loc[syrups_df['Item'] == 'dragon', 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1

    if row['Item'] == 'Lychee Martini':
        qty = row['Qty']
        vodka_df.loc[(vodka_df['Item'] == 'Tito\'s') & (vodka_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 2.5
        syrups_df.loc[syrups_df['Item'] == 'lychee', 'Ounce'] += qty * 1.5

    if row['Item'] == 'Courageous Koi':
        qty = row['Qty']
        whiskey_df.loc[(rum_df['Item'] == 'Jack Daniels') & (whiskey_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        whiskey_df.loc[(rum_df['Item'] == 'Bulleit Rye') & (whiskey_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'simple', 'Ounce'] += qty * .5
        syrups_df.loc[syrups_df['Item'] == 'orgeat', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1

    if row['Item'] == 'Mermaid\'s Kiss':
        qty = row['Qty']
        whiskey_df.loc[(whiskey_df['Item'] == 'Maker\'s Mark') & (whiskey_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        syrups_df.loc[syrups_df['Item'] == 'grenadine', 'Ounce'] += qty * .5
        syrups_df.loc[syrups_df['Item'] == 'simple', 'Ounce'] += qty * .25
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * .5

    if row['Item'] == 'Starry Daze':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Plantation Light Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        syrups_df.loc[syrups_df['Item'] == 'simple', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * .75

    if row['Item'] == 'Hawaiian MAI TAI':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Plantation Light Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.77
        rum_df.loc[(rum_df['Item'] == 'Plantation Dark Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.77
        syrups_df.loc[syrups_df['Item'] == 'finestorgeat', 'Ounce'] += qty * .445
        juice_df.loc[juice_df['Item'] == 'guava', 'Ounce'] += qty * 1.335
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * 1.335
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * .75
        other_df.loc[(other_df['Item'] == 'tripleSec') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .445

    if row['Item'] == 'Walking Dead':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Plantation Light Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        rum_df.loc[(rum_df['Item'] == 'Plantation Dark Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'finestorgeat', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'simple', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'finestpassion', 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'tripleSec') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1

    if row['Item'] == 'Makai Margarita':
        qty = row['Qty']
        tequila_df.loc[(tequila_df['Item'] == 'Luna Azul') & (tequila_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        syrups_df.loc[syrups_df['Item'] == 'hibiscus', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * .75
        other_df.loc[(other_df['Item'] == 'tripleSec') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75

    if row['Item'] == 'Saturn':
        qty = row['Qty']
        gin_df.loc[(gin_df['Item'] == 'Venus Blend No. 1') & (gin_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        syrups_df.loc[syrups_df['Item'] == 'passion', 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .5
        syrups_df.loc[syrups_df['Item'] == 'orgeat', 'Ounce'] += qty * .25
        other_df.loc[(other_df['Item'] == 'falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5

    if row['Item'] == 'The Bonzer':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Lemon Hart 1804') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 2
        other_df.loc[(other_df['Item'] == 'falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'dram') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'coco', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'cindem', 'Ounce'] += qty * .25

    if row['Item'] == 'Juicy Fruit':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Don Q Gold') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        other_df.loc[(other_df['Item'] == 'falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'apricot') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'orangemang', 'Ounce'] += qty * 1

    if row['Item'] == 'Blood Moon':
        qty = row['Qty']
        gin_df.loc[(gin_df['Item'] == 'Venus Blend No. 1') & (gin_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        other_df.loc[(other_df['Item'] == 'amaro') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'Licor 43') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'blood', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'cindem', 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * .25

    if row['Item'] == 'Mr. Makai':
        qty = row['Qty']
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'dragon', 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'Luxardo Amaretto') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        rum_df.loc[(rum_df['Item'] == 'Lemon Hart 151') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        rum_df.loc[(rum_df['Item'] == 'Plantation 5 year') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        rum_df.loc[(rum_df['Item'] == 'Smith & Cross') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75

    if row['Item'] == 'That One':
        qty = row['Qty']
        gin_df.loc[(gin_df['Item'] == 'Tanqueray') & (gin_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'elderflower') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'pierreFerrand') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1

    if row['Item'] == 'Kahanamoku':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Whalers Vanilla') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * .75
        syrups_df.loc[syrups_df['Item'] == 'coco', 'Ounce'] += qty * .5
        rum_df.loc[(rum_df['Item'] == 'Lemon Hart Blackpool Spiced') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
    if row['Item'] == 'Scorpion Bowl':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Plantation Dark Rum') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 3
        other_df.loc[(other_df['Item'] == 'Jacques Bonet Brandy') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 3
        rum_df.loc[(rum_df['Item'] == 'Denizen Merchant reserve') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        rum_df.loc[(rum_df['Item'] == 'Denizen Vatted Dark') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        rum_df.loc[(rum_df['Item'] == 'Lemon Hart 151') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        gin_df.loc[(gin_df['Item'] == 'New Amsterdam') & (gin_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        other_df.loc[(other_df['Item'] == 'Falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 3
        juice_df.loc[juice_df['Item'] == 'orange', 'Ounce'] += qty * 3
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * 3
        syrups_df.loc[syrups_df['Item'] == 'passion', 'Ounce'] += qty * 1.5
        syrups_df.loc[syrups_df['Item'] == 'finestorgeat', 'Ounce'] += qty * 1.5
    if row['Item'] == 'Punch to the Skull':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Denizen Aged White') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        other_df.loc[(other_df['Item'] == 'Aperol') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1.5
        other_df.loc[(other_df['Item'] == 'Falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        other_df.loc[(other_df['Item'] == 'pierreFerrand') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1.5
    if row['Item'] == 'Punch to the Skull WITHOUT jar':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Denizen Aged White') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'Aperol') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'Falernum') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        other_df.loc[(other_df['Item'] == 'pierreFerrand') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * 1
    if row['Item'] == 'Unusual Suspects':
        qty = row['Qty']
        rum_df.loc[(rum_df['Item'] == 'Real McCoy 5 yr') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        rum_df.loc[(rum_df['Item'] == 'Plantation OFTD') & (rum_df['Size'] == 'SINGLE'), 'Ounce'] += qty * 1
        other_df.loc[(other_df['Item'] == 'dram') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .25
        other_df.loc[(other_df['Item'] == 'macadamia') & (other_df['Size'] == 'SINGLE'), 'Ounce'] += qty * .5
        syrups_df.loc[syrups_df['Item'] == 'coco', 'Ounce'] += qty * .75
        syrups_df.loc[syrups_df['Item'] == 'vanilla', 'Ounce'] += qty * .25
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * .75

for index, row in mocktail_df.iterrows():
    if row['Item'] == 'POG Spritzer':
        qty = row['Qty']
        syrups_df.loc[syrups_df['Item'] == 'passion', 'Ounce'] += qty * 1.5
        juice_df.loc[juice_df['Item'] == 'guava', 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'orange', 'Ounce'] += qty * .75
    if row['Item'] == 'Hibiscus Lei':
        qty = row['Qty']
        syrups_df.loc[syrups_df['Item'] == 'hibiscus', 'Ounce'] += qty * 1.5
        juice_df.loc[juice_df['Item'] == 'lime', 'Ounce'] += qty * 1
        syrups_df.loc[syrups_df['Item'] == 'coco', 'Ounce'] += qty * 1.5

    if row['Item'] == 'Freaky Tiki':
        qty = row['Qty']
        syrups_df.loc[syrups_df['Item'] == 'hibiscus', 'Ounce'] += qty * 1.5
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .5
        juice_df.loc[juice_df['Item'] == 'guava', 'Ounce'] += qty * 1.5
    if row['Item'] == 'Pineapple Surf':
        qty = row['Qty']
        syrups_df.loc[syrups_df['Item'] == 'orangemang', 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'lemon', 'Ounce'] += qty * .75
        juice_df.loc[juice_df['Item'] == 'pineapple', 'Ounce'] += qty * 3


#fig = px.bar(vodka_df, x='Item', y='liter', color='Item')


fooddataframe_names = ['entrees', 'sides', 'kids', 'desserts', 'pupu', 'cocktail', 'mocktail']
alcdataframe_names = ['vodka', 'whiskey', 'gin', 'rum', 'tequila', 'other', 'syrup', 'juice']

# create a dictionary mapping dataframe names to dataframes

vodka_df['liter'] = round(vodka_df['Ounce'] / 33.814, 2)
rum_df['liter'] = round(rum_df['Ounce'] / 33.814, 2)
tequila_df['liter'] = round(tequila_df['Ounce'] / 33.814, 2)
whiskey_df['liter'] = round(whiskey_df['Ounce'] / 33.814, 2)
gin_df['liter'] = round(gin_df['Ounce'] / 33.814, 2)
other_df['liter'] = round(other_df['Ounce'] / 33.814, 2)
vodka_df['750'] = round(vodka_df['Ounce'] / 25.3605, 2)
rum_df['750'] = round(rum_df['Ounce'] / 25.3605, 2)
tequila_df['750'] = round(tequila_df['Ounce'] / 25.3605, 2)
whiskey_df['750'] = round(whiskey_df['Ounce'] / 25.3605, 2)
gin_df['750'] = round(gin_df['Ounce'] / 25.3605, 2)
other_df['750'] = round(other_df['Ounce'] / 25.3605, 2)

vodka_ff = vodka_df.groupby(vodka_df['Item'])

syrups_df['deli'] = syrups_df['Ounce']/32
# Print the resulting DataFrame
# fig = px.bar(vodka_df, x='Item', y='liter', color='Item')
# fig.show()


# liquors_df = [vodka_df, rum_df, tequila_df, whiskey_df, tequila_df]
liquors_df = [vodka_df, rum_df, tequila_df, whiskey_df, gin_df, other_df]

df_combined = pd.concat(liquors_df)
df_combined = df_combined.groupby('Item')[['Ounce', 'liter',
                                           '750']].sum().reset_index().sort_values('Ounce', ascending=False)


    # Display the resulting dataframe

dataframe_dict = {'entrees': entrees_df, 'Sides': side_df, 'Kids Meal': kids_df, 'Desserts': dessert_df, 'Pupu': pupu_df,
                  'vodka': vodka_df, 'whiskey': whiskey_df, 'gin': gin_df, 'rum': rum_df, 'mocktail': mocktail_df,
                  'cocktail': cocktail_df, 'tequila': tequila_df, 'other': other_df, 'syrup': syrups_df,
                  'juice': juice_df, 'combo': df_combined, 'beer': beer_df, 'draft beer': draftbeer_df,
                  'wine': wine_df, 'Secret Menu': secret_df}
tequila_df_grouped = tequila_df.groupby(['Item'], as_index=False).sum()[['Ounce', '750', 'liter']]
tequila_df_grouped = tequila_df.join(tequila_df_grouped, lsuffix='_original', rsuffix='_grouped')



#app = dash.Dash()
app = dash.Dash()

table = dash_table.DataTable(
    id='liquors-table',
    columns=[
        {"name": "Item", "id": "Item", "deletable": False, "selectable": True},
        {"name": "Ounce", "id": "Ounce", "deletable": False, "selectable": True},
        {"name": "liter", "id": "liter", "deletable": False, "selectable": True},
        {"name": "fliter", "id": "750", "deletable": False, "selectable": True},
    ],
    style_cell={
        'minWidth': '0px', 'maxWidth': '80px',
        'whiteSpace': 'normal'
    },
    style_table={
        'maxHeight': '600px',
        'overflowY': 'scroll',
        'width': '600px',
        'fontSize': '20px'
    },
    data=[]
)

# create dropdown
options = [{'label': key, 'value': key} for key in dataframe_dict.keys()]
dropdown = html.Div([dcc.Dropdown(id='dataframe-select', options=options, value='entrees', style={'width': '200px'})])
column_dropdown = html.Div([dcc.Dropdown(id='column-select', options=[], value='Qty', style={'width': '200px'})])
option = [{'label': key, 'value': key} for key in dataframe_dict.keys() if key in ['vodka', 'whiskey',
                                                                                  'gin', 'rum', 'tequila', 'combo',
                                                                                   'cocktail']]
dropdown_liquors = html.Div([dcc.Dropdown(id='liquors-select', options=option, value='vodka', style={'width': '200px'})])
# create dropdown for chart types
chart_types = ["line","bar"]
dropdown_chart_type = html.Div([dcc.Dropdown(id='chart-type-select',
                                             options=[{'label': i, 'value': i} for i in chart_types], value='line',
                                             style={'width': '200px'})])
# create graph
graph = dcc.Graph(id='dataframe-graph')
# update the options of second dropdown based on the selected dataframe
@app.callback(
    dash.dependencies.Output('column-select', 'options'),
    [dash.dependencies.Input('dataframe-select', 'value')])
def update_columns(value):
    df_combined = dataframe_dict[value]
    return [{'label': col, 'value': col} for col in df_combined.columns]

# Add the second dropdown to the layout
app.layout = html.Div(children= [
    html.H1("Makai Dashboard"), dropdown,
    dropdown_chart_type, column_dropdown,
    graph, dropdown_liquors, table])
# update the graph based on the selected column
@app.callback(dash.dependencies.Output('dataframe-graph', 'figure'),
              [dash.dependencies.Input('dataframe-select', 'value'),
               dash.dependencies.Input('column-select', 'value'),
               dash.dependencies.Input('chart-type-select', 'value')
               ])
def update_graph(dataframe_value, column_value,chart_value):
    if column_value is None:
        raise dash.exceptions.PreventUpdate
    df_combined = dataframe_dict[dataframe_value]
    return {
        'data': [{'x': df_combined['Item'], 'y':df_combined[column_value],'type':chart_value, 'name': column_value}],
        'layout': {'title': f'{dataframe_value} - {column_value}'}
    }
#update the table based on selected dataframe
@app.callback(
    dash.dependencies.Output('liquors-table', 'data'),
    [dash.dependencies.Input('liquors-select', 'value')])
def update_table(value):
    df_combined = dataframe_dict[value]
    return df_combined.to_dict("rows")

if __name__ == '__main__':
    app.run_server(debug=True)


