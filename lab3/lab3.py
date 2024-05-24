from spyre import server

import os
import urllib.request
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from importlib import reload

folder_path = 'csv_files'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def download(i):
    filename_pattern = "NOAA_ID{}_".format(i)
    file_check = [file for file in os.listdir(folder_path) if file.startswith(filename_pattern)]
    if file_check:
        return
    
    print('Downloading VHI files...')
    url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(i)
    wp = urllib.request.urlopen(url)
    text = wp.read()
    now = datetime.datetime.now()
    date_and_time = now.strftime("%d_%m_%Y_%H-%M-%S")
    province_n = i
    file_path = os.path.join(folder_path, 'NOAA_ID{}_{}.csv'.format(province_n, date_and_time))
    with open(file_path, 'wb') as out:
        out.write(text)
    print('\nVHI files are downloaded!')

for i in range(1, 28):
    download(i)

def read_csv(folder_path):
    files = os.listdir(folder_path)
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    main_df = pd.DataFrame()
    for i in range(len(files)):
        file_path = os.path.join(folder_path, files[i])
        df = pd.read_csv(file_path, header=1, names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df['empty'] = df['empty'].apply(lambda x: 0 if pd.isnull(x) else x)

        df['area'] = i + 1

        df['Year'] = df['Year'].str.replace('<tt><pre>', '')
        df = df.drop(df[df['Year'] == '</pre></tt>'].index)
        df['Year'] = df['Year'].astype(int)

        main_df = pd.concat([main_df, df])
    return main_df

names = {1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська", 6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська",
         9: "Київська", 10: "Кіровоградська", 11: "Луганська", 12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська", 16: "Рівенська", 17: "Сумська",
         18: "Тернопільська", 19: "Харківська", 20: "Херсонська", 21: "Хмельницька", 22: "Черкаська", 23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим"}

class StockExample(server.App):
    title = "NOAA data visualization"

    df = read_csv(folder_path)
    df = df.replace({'area': names})  

    inputs = [{"type": "dropdown",
               "label": "NOAA data dropdown",
               "options": [{"label": "VCI", "value": "VCI"},
                           {"label": "TCI", "value": "TCI"},
                           {"label": "VHI", "value": "VHI"}],
               "key": "ticker",
               "action_id": "update_data"},

              {"type": "dropdown",
               "label": "Region",
               "options": [{"label": f"{names[i]}", "value": names[i]} for i in range(1, 26)],
               "key": "region",
               "action_id": "update_data"},

              {"type": "text",
               "label": "Weeks",
               "key": "weeks",
               "value": "1-52",
               "action_id": "update_data"},

              {"type": "text",
               "label": "Years",
               "key": "years",
               "value": "1994-2004",
               "action_id": "update_data"}]

    controls = [{"type": "button", "label": "Update", "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [{"type": "table",
                "id": "table",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True},

               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}]

    def getData(self, params):
        pattern = r'\d+-\d+$'
        if not re.match(pattern, params["weeks"]) or not re.match(pattern, params["years"]):
            return pd.DataFrame()

        self.ticker = params["ticker"]
        self.region = params["region"]
        self.week = params["weeks"].split("-")
        self.year = params["years"].split("-")

        if self.ticker == "VCI":
            columns = ["Year", "Week", "VCI"]
        elif self.ticker == "TCI":
            columns = ["Year", "Week", "TCI"]
        elif self.ticker == "VHI":
            columns = ["Year", "Week", "VHI"]

        data = self.df[(self.df['area'] == self.region) &
                       (self.df["Week"] >= int(self.week[0])) &
                       (self.df['Week'] <= int(self.week[1])) &
                       (self.df["Year"] >= int(self.year[0])) &
                       (self.df['Year'] <= int(self.year[1]))][columns]
        return data

    def getPlot(self, params):
        data_for_plot = self.getData(params)
        if data_for_plot.empty:
            return plt.gcf()

        plt.figure(figsize=(20, 10))
        plt.title(f"{self.ticker} values for {self.region} region")
        sns.heatmap(data_for_plot.pivot(index="Week", columns='Year', values=self.ticker), annot=True)
        return plt.gcf()

app = StockExample()
app.launch(port=9093)
