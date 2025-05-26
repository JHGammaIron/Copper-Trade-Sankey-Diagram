import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import comtradeapicall
import os




st.set_page_config(page_title="Copper Trade Sankey", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-size: 18px !important;
        }

        div[data-testid="stMultiselect"] > label,
        div[data-testid="stSelectbox"] > label {
            white-space: normal !important;
            overflow-wrap: break-word !important;
            display: block !important;
        }

        div[data-testid="stSidebar"] {
            min-width: 320px;
        }

        .block-container {
            max-width: 100% !important;
        }
        .stMultiSelect [data-baseweb="select"] span {
        max-width: 800px;
        # white-space: normal;
        overflow: visible;
        text-overflow: clip;
        }

        .stMultiSelect [data-baseweb="select"] > div > div {
            /* max-height: 200px;
            /* overflow-y: auto; */
        }
    </style>
""", unsafe_allow_html=True)





st.title("Copper Trade Sankey Diagram")

# import os
# import sys

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except AttributeError:
#         base_path = os.path.abspath(os.path.dirname(__file__))
#     return os.path.join(base_path, relative_path)

# csv_file_name = "(2)_copper_May_19.csv"
# # csv_file_name = "copper_all_May_19.csv"
# # csv_file_name = "Copper_3_Types_(2603_7403_7404)_All_Years.csv"
# csv_path = resource_path(csv_file_name)


# try:
#     all_df = pd.read_csv(csv_path)
# except FileNotFoundError:
#     print(f"Error: CSV file not found at {csv_path}")
# except Exception as e:
#     print(f"An error occurred while loading the CSV: {e}")

# all_df = pd.read_csv('./(2)_copper_May_19.csv')


all_options = ['Copper ores and concentrates',
 'Nails, tacks, drawing pins, corrugated nails, staples (not those of heading no. 8305) and the like, of iron or steel, with heads of other material or not, but excluding articles with heads of copper',
 'Copper and articles thereof',
 'Copper mattes; cement copper (precipitated copper)',
 'Copper; unrefined, copper anodes for electrolytic refining',
 'Copper; refined and copper alloys, unwrought',
 'Copper; waste and scrap',
 'Copper; master alloys',
 'Copper; powders and flakes',
 'Copper; bars, rods and profiles',
 'Copper wire',
 'Copper plates, sheets and strip; of a thickness exceeding 0.15mm',
 'Copper foil (whether or not printed or backed with paper, paperboard, plastics or similar backing materials) of a thickness (excluding any backing) not exceeding 0.15mm',
 'Copper tubes and pipes',
 'Copper; tube or pipe fittings (e.g. couplings, elbows, sleeves)',
 'Copper; stranded wire, cables, plaited bands and the like, not electrically insulated',
 'Copper, nails, tacks, drawing pins, staples (not those of heading no. 8305) and the like, of copper or iron or steel with heads of copper; screws bolts, nuts, screws hooks, rivets, cotters, washers',
 'Nails, tacks, drawing pins, staples (not those of heading no. 8305) and the like, of copper or iron or steel with heads of copper; screws bolts, nuts, screws hooks, rivets, cotters, washers of copper',
 'Copper; table, kitchen or other household articles and parts thereof; pot scourers, scouring, polishing pads, gloves and the like; sanitary ware and parts thereof',
 'Table, kitchen or other household articles and parts thereof, of copper; pot scourers, scouring, polishing pads, gloves and the like, of copper; sanitary ware and parts thereof, of copper',
 'Copper; articles thereof n.e.c. in chapter 74',
 'Copper; articles thereof n.e.c.']

# all_options = sorted(all_df['cmdDesc'].unique().tolist())
copper_type = st.multiselect("Select Copper Types", all_options, default=['Copper ores and concentrates', 'Copper; refined and copper alloys, unwrought', 'Copper; waste and scrap'])


"""
**Note:** Data unavailable for China in 2024
"""
# year_min = int(all_df['refYear'].min())
# year_max = int(all_df['refYear'].max())
# year_range = st.slider("Select Year Range", year_min, year_max, (2023, 2023))
# selected_years = list(range(year_range[0], year_range[1] + 1))

year_min = 1962
year_max = 2024
year_range = st.slider("Select Year Range", year_min, year_max, (2023, 2023))
selected_years = list(range(year_range[0], year_range[1] + 1))

# start, end = year_range
# if end - start > max_range:
#     st.error(f"Please select a range of at most {max_range} years. Currently selected: {end - start} years")
# else:
#     st.success(f"Selected range: {start} to {end}")



top_n = st.number_input("Number of Countries to Display (Ranked by Export Quantity)", min_value=0, max_value=50, value=5)

all_countries = ['Afghanistan', 'Africa CAMEU region, nes', 'Ã…land Islands ', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 
'Antarctica', 'Antigua and Barbuda', 'Arab Rep. of Yemen (...1990)', 'Areas, nes', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belgium-Luxembourg (...1998)', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 
 'Bolivia (Plurinational State of)', 'Bonaire', 'Bosnia Herzegovina', 'Botswana', 'Bouvet Island', 'Br. Antarctic Terr.', 'Br. Indian Ocean Terr.',
  'Br. Virgin Isds', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Bunkers', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'CACM, nes', 'Cambodia', 'Cameroon', 
  'Canada', 'Caribbean, nes', 'Cayman Isds', 'Central African Rep.', 'Chad', 'Channel Islands ', 'Chile', 'China', 'China, Hong Kong SAR', 'China, Macao SAR',
   'Christmas Isds', 'Cocos Isds', 'Colombia', 'Comoros', 'Congo', 'Cook Isds', 'Costa Rica', "CÃ´te d'Ivoire", 'Croatia', 'Cuba', 'CuraÃ§ao', 'Cyprus', 'Czechia', 
   'Czechoslovakia (...1992)', "Dem. People's Rep. of Korea", 'Dem. Rep. of Germany (...1990)', 'Dem. Rep. of the Congo', 'Dem. Rep. of Vietnam (...1974)', 
   'Dem. Yemen (...1990)', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Rep.', 'East and West Pakistan (...1971)', 'Eastern Europe, nes', 'Ecuador', 'Egypt', 
   'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Ethiopia (...1992)', 'Europe EFTA, nes', 'Europe EU, nes', 'Faeroe Isds', 
   'Falkland Isds (Malvinas)', 'Fed. Rep. of Germany (...1990)', 'Fiji', 'Finland', 'Fr. South Antarctic Terr.', 'France', 'Free Zones', 'French Guiana (Overseas France)',
    'French Polynesia', 'FS Micronesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe (Overseas France)', 
    'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 
    'Hungary', 'Iceland', 'India', 'India (...1974)', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man ', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan',
     'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'LAIA, nes', "Lao People's Dem. Rep.", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 
     'Liechtenstein ', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Isds', 'Martinique (Overseas France)', 
     'Mauritania', 'Mauritius', 'Mayotte (Overseas France)', 'Metropolitan France', 'Mexico', 'Midway Islands', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 
     'Mozambique', 'Myanmar', 'N. Mariana Isds', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles (...2010)', 'Netherlands Antilles and Aruba (...1985)',
      'Neutral Zone', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Isds', 'North America and Central America, nes', 'North Macedonia', 
      'Northern Africa, nes', 'Norway', 'Norway, excluding Svalbard and Jan Mayen', 'Oceania, nes', 'Oman', 'Other Africa, nes', 'Other Asia, nes', 'Other Europe, nes', 
      'Pacific Isds (...1991)', 'Pakistan', 'Palau', 'Panama', 'Panama, excl.Canal Zone (...1977)', 'Panama-Canal-Zone (...1977)', 'Papua New Guinea', 'Paraguay', 
      'Peninsula Malaysia (...1963)', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico ', 'Qatar', 'Rep. of Korea', 'Rep. of Moldova', 
      'Rep. of Vietnam (...1974)', 'Rest of America, nes', 'RÃ©union (Overseas France)', 'Rhodesia Nyas (...1964)', 'Romania', 'Russian Federation', 'Rwanda', 
      'Ryukyu Isd', 'Sabah (...1963)', 'Saint BarthÃ©lemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Kitts, Nevis and Anguilla (...1980)', 'Saint Lucia',
       'Saint Maarten', 'Saint Martin (French part) ', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe',
       'Sarawak', 'Saudi Arabia', 'Senegal', 'Serbia', 'Serbia and Montenegro (...2005)', 'Seychelles', 'Sierra Leone', 'Sikkim, Protectorate of India (...1974)', 
       'Singapore', 'Slovakia', 'Slovenia', 'Solomon Isds', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'South Sudan', 
       'Southern African Customs Union (...1999)', 'Spain', 'Special Categories', 'Sri Lanka', 'State of Palestine', 'Sudan', 'Sudan (...2011)', 'Suriname', 
       'Svalbard and Jan Mayen Islands ', 'Sweden', 'Switzerland ', 'Switzerland', 'Syria', 'Taiwan, Province of China', 'Tajikistan', 'Tanganyika (...1964)',
        'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'TÃ¼rkiye', 'Turkmenistan', 'Turks and Caicos Isds', 'Tuvalu', 
        'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United Rep. of Tanzania', 'United States Minor Outlying Islands', 'United States of America',
         'Uruguay', 'US Misc. Pacific Isds', 'US Virgin Isds (...1980)', 'USA', 'USA and Puerto Rico (...1980)', 'USSR (...1990)', 'Uzbekistan', 'Vanuatu', 'Venezuela', 
         'Viet Nam', 'Wake Island', 'Wallis and Futuna Isds', 'Western Asia, nes', 'Western Sahara', 'World', 'Yemen', 'Yugoslavia (...1991)', 'Zambia', 
         'Zanzibar and Pemba Isd (...1964)', 'Zimbabwe']
# all_countries = sorted(set(all_df['reporterDesc'].unique().tolist() + all_df['partnerDesc'].unique().tolist()))
countries_to_keep = st.multiselect("Add Country", all_countries)




# metric = st.selectbox("Select Metric", ['primaryValue', 'netWgt'])

metric_options = st.selectbox("Select Metric", ['Trade Value (USD)', 'Net Weight (kg)'])

if metric_options == 'Trade Value (USD)':
    metric = 'primaryValue'
else:
    metric = 'netWgt'

desc_to_code_map = {
    'Copper ores and concentrates' : 2603,
    'Nails, tacks, drawing pins, corrugated nails, staples (not those of heading no. 8305) and the like, of iron or steel, with heads of other material or not, but excluding articles with heads of copper' : 7317,
    'Copper and articles thereof' : 74,
    'Copper mattes; cement copper (precipitated copper)' : 7401,
    'Copper; unrefined, copper anodes for electrolytic refining' : 7402,
    'Copper; refined and copper alloys, unwrought' : 7403,
    'Copper; waste and scrap' : 7404,
    'Copper; master alloys' : 7405,
    'Copper; powders and flakes' : 7406,
    'Copper; bars, rods and profiles' : 7407,
    'Copper wire' : 7408,
    'Copper plates, sheets and strip; of a thickness exceeding 0.15mm' : 7409,
    'Copper foil (whether or not printed or backed with paper, paperboard, plastics or similar backing materials) of a thickness (excluding any backing) not exceeding 0.15mm' : 7410,
    'Copper tubes and pipes' : 7411,
    'Copper; tube or pipe fittings (e.g. couplings, elbows, sleeves)' : 7412,
    'Copper; stranded wire, cables, plaited bands and the like, not electrically insulated' : 7413,
    'Copper, nails, tacks, drawing pins, staples (not those of heading no. 8305) and the like, of copper or iron or steel with heads of copper; screws bolts, nuts, screws hooks, rivets, cotters, washers' : 7414,
    'Nails, tacks, drawing pins, staples (not those of heading no. 8305) and the like, of copper or iron or steel with heads of copper; screws bolts, nuts, screws hooks, rivets, cotters, washers of copper' : 7415,
    'Copper; table, kitchen or other household articles and parts thereof; pot scourers, scouring, polishing pads, gloves and the like; sanitary ware and parts thereof' : 7416,
    'Table, kitchen or other household articles and parts thereof, of copper; pot scourers, scouring, polishing pads, gloves and the like, of copper; sanitary ware and parts thereof, of copper' : 7417,
    'Copper; articles thereof n.e.c. in chapter 74' : 7418,
    'Copper; articles thereof n.e.c.' : 7419,
}

subscription_key = os.getenv("API_KEY")


## Create list of dataframes filtering for relevant entries
def create_dataframes(selected_years, copper_type):
# def create_dataframes(new_df, selected_years, copper_type):
  # df = new_df
  multi_df = []
  max_interval = 12
  for i in range(0, len(selected_years), max_interval):

    # [my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)]

      temp_years = selected_years[i:i + max_interval]

      multi_df.append(comtradeapicall.getFinalData(
                subscription_key=subscription_key,
                typeCode='C',
                freqCode='A',
                clCode='HS',
                
                # period='2024',
                period= ','.join(map(str, temp_years)),
                reporterCode=None,
                cmdCode= ','.join(str(desc_to_code_map[ct]) for ct in copper_type),
                # cmdCode=str(desc_to_code_map[copper_type]),
                flowCode='X',
                partnerCode=0,

                # partnerCode=None,
                partner2Code=0,
                customsCode=None,
                motCode=None,
                maxRecords=250000,
                # format_output='CSV',
                format_output='JSON',
                aggregateBy=None,
                breakdownMode='classic',
                # breakdownMode='plus',
                countOnly=None,
                includeDesc=True
            )
      )
  df = pd.concat(multi_df, axis=0, ignore_index=True)
  df = df[df['partnerDesc'] == "World"]
  df = df[df['flowDesc'] == "Export"]
  df = df[df['refYear'].isin(selected_years)]
  df = df[df['cmdDesc'].isin(copper_type)]
  dataframes.append(df)

  # df = new_df
  multi_df = []
  for i in range(0, len(selected_years), max_interval):
      temp_years = selected_years[i:i + max_interval]
      multi_df.append(comtradeapicall.getFinalData(
                subscription_key=subscription_key,
                typeCode='C',
                freqCode='A',
                clCode='HS',
                
                # period='2024',
                period= ','.join(map(str, temp_years)),
                reporterCode=None,
                cmdCode=','.join(str(desc_to_code_map[ct]) for ct in copper_type),
                flowCode='M',
                partnerCode=0,

                # partnerCode=None,
                partner2Code=0,
                customsCode=None,
                motCode=None,
                maxRecords=250000,
                # format_output='CSV',
                format_output='JSON',
                aggregateBy=None,
                breakdownMode='classic',
                # breakdownMode='plus',
                countOnly=None,
                includeDesc=True
            )
      )
  df = pd.concat(multi_df, axis=0, ignore_index=True)
  df = df[df['partnerDesc'] == "World"]
  df = df[df['flowDesc'] == "Import"]
  df = df[df['refYear'].isin(selected_years)]
  df = df[df['cmdDesc'].isin(copper_type)]
  dataframes.append(df)


## Filter countries from Dataframe in list 'groupby_df'
def replace_with_other(entity, groupby_df, index):
  for i, country in enumerate(groupby_df):
    if country in countries_to_keep:
        continue
    global dataframes
    dataframes[index].loc[dataframes[index][entity] == country, entity] = "Other"


## Collect countries to be excluded
def filter_countries(dataframe, entity, dataframe_index):
    groupby_df = dataframe.groupby(entity)[metric].sum()
    groupby_df = groupby_df.sort_values(ascending=False)
    groupby_df = groupby_df.index[top_n:].tolist()
    replace_with_other(entity, groupby_df, dataframe_index)


## Identify Top Ranking Countries by Export Quantity
def identify_top_ranking_countries(dataframes):
  filter_countries(dataframes[0], 'reporterDesc', 0)
  filter_countries(dataframes[1], 'reporterDesc', 1)

## Create labels (nodes in Sankey Diagram)
def create_labels(dataframes, labels, sizes):
    new_labels = list(set(dataframes[0]['reporterDesc'].tolist()))
    labels.extend(new_labels)
    sizes.append(len(labels))

    new_labels = copper_type
    labels.extend(new_labels)
    sizes.append(len(labels))

    new_labels = list(set(dataframes[1]['reporterDesc'].tolist()))
    labels.extend(new_labels)
    sizes.append(len(labels))


selected_years = list(range(year_range[0], year_range[1] + 1))

source = []
target = []
values = []

aggregate_source = []
aggregate_target = []
aggregate_values = []



dataframes = []

# new_df = all_df

create_dataframes(selected_years, copper_type)
# create_dataframes(new_df, selected_years, copper_type)

identify_top_ranking_countries(dataframes)

sizes = [0]
labels = []

create_labels(dataframes, labels, sizes)


## Set parameters to Sankey Diagram (source,target,value)
for index, row in dataframes[0].iterrows():
    for i in range(sizes[0], sizes[1]):
      if row['reporterDesc'] == labels[i]:
          source.append(i)
          break
    for j in range(sizes[1], sizes[2]):
      if row['cmdDesc'] == labels[j]:
          target.append(j)
          break
    values.append(row[metric])

for index, row in dataframes[1].iterrows():
    for i in range(sizes[1], sizes[2]):
      if row['cmdDesc'] == labels[i]:
          source.append(i)
          break
    for j in range(sizes[2], sizes[3]):
      if row['reporterDesc'] == labels[j]:
          target.append(j)
          break
    values.append(row[metric])


## Aggregate values
df = pd.DataFrame({'source': source, 'target': target, 'value': values})
df_aggregate = df.groupby(['source', 'target'], as_index=False).sum()

aggregate_source = df_aggregate['source'].tolist()
aggregate_target = df_aggregate['target'].tolist()
aggregate_values = df_aggregate['value'].tolist()



## Create Sankey Diagram

fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        align="right",
    ),
    link=dict(
        arrowlen=15,
        source=aggregate_source,
        target=aggregate_target,
        value=aggregate_values
    )
))


#Change Diagram Title
fig.update_layout(
    title_text="Top Countries By Exports/Imports of Copper (Country -> Copper Type -> Country)" + " based on " + metric,
    font=dict(
        size=20,
        color="black"
    ),
    width=1300,
    height=800,
    hoverlabel=dict(
        font_size=20
    )
)

st.plotly_chart(fig, use_container_width=True)

"""**"Other"**, is a category representing an aggregation of all countries whose trade volume are ranked below the top ranking countries (also specified above), over all types of selected copper types.

**Layers** are ordered from left to right, with export flows from the left layer to the middle layer, and import flows from the middle layer to the right layer.
"""