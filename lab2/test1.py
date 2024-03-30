import os
import pandas as pd

directory = 'C:\\Users\\vladi\\PycharmProjects\\DataAnalysis\\lab2\\csv_files'

def extract(directory):
    files = os.listdir(directory)
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    main_df = pd.DataFrame()
    for i in range(len(files)):
        file_path = os.path.join(directory, files[i])
        df = pd.read_csv(file_path, header = 1, names = headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df['area'] = i+1

        df['Year'] = df['Year'].str.replace('<tt><pre>', '')
        df = df.drop(df[df['Year'] == '</pre></tt>'].index)
        df['Year'] = df['Year'].astype(int)

        main_df = pd.concat([main_df, df])
    return main_df

def change_area(df):
    names = {1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська", 6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська",
             9: "Київська", 10: "Кіровоградська", 11: "Луганська", 12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська", 16: "Рівенська", 17: "Сумська",
             18: "Тернопільська", 19: "Харківська", 20: "Херсонська'", 21: "Хмельницька", 22: "Черкаська'", 23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим"}
    for i in range(1,28):
        df["area"] = df["area"].replace(names)
    return df

def min_vhi(df, area_name, year):
    filtered_df = df[(df['area'] == area_name) & (df['Year'] == year)]
    minimum_vhi = filtered_df['VHI'].min()
    return filtered_df[filtered_df['VHI'] == minimum_vhi]

def max_vhi(df, area_name, year):
    filtered_df = df[(df['area'] == area_name) & (df['Year'] == year)]
    maximum_vhi = filtered_df['VHI'].max()
    return filtered_df[filtered_df['VHI'] == maximum_vhi]

def range_vhi(df, area_name, start, end):
    for i in range(start, end + 1):


'''(df.VHI <= 15)'''
'''def extreme(df, area_name, percent):
    df_drought = df[(df['area'] == area_name)]
    years = list(df['Year'].unique())
    res = []
    for year in years:
        if not df[(df['Year'] == year) & (df.VHI <= percent)].empty:
            res.append(year)
    return res'''

df = change_area(extract(directory))
#print(min_vhi(df, "Херсонська", 2004))
#print(max_vhi(df, "Херсонська", 2004))
#print(df)
#print(extreme(df, 'Херсонська', 15))


'''df = change_area(extract(directory))
print(df.head(10))'''