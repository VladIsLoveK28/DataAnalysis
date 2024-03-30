import os
import pandas as pd

directory = 'csv_files'

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
    df["area"] = df["area"].map(names)
    return df

def min_vhi(df, area_name, year):
    filtered_df = df[(df['area'] == area_name) & (df['Year'] == year)]
    minimum_vhi = filtered_df['VHI'].min()
    return filtered_df[filtered_df['VHI'] == minimum_vhi]

def max_vhi(df, area_name, year):
    filtered_df = df[(df['area'] == area_name) & (df['Year'] == year)]
    maximum_vhi = filtered_df['VHI'].max()
    return filtered_df[filtered_df['VHI'] == maximum_vhi]

def vhi_by_years_and_areas(df, areas, start_year, end_year):
    selected_data = pd.DataFrame()
    for area in areas:
        area_data = df[(df['area'] == area) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]
        selected_data = pd.concat([selected_data, area_data[['Year', 'VHI', 'area']]], axis=1)
    return selected_data

'''(df.VHI <= 15)'''
def extrim(df, area_name, percent):
    df_drought = df[(df['area'] == area_name)]
    years = list(df['Year'].unique())
    res = []
    for year in years:
        if not df[(df['Year'] == year) & (df.VHI <= percent)].empty:
            res.append(year)
    return res


df = extract(directory)
print(df.head())

#df = change_area(extract(directory))
#print(min_vhi(df, "Херсонська", 2004))
#print(max_vhi(df, "Херсонська", 2004))
#print(extreme(df, 'Херсонська', 15))

#areas = ["Волинська", "Дніпропетровська", "Донецька", "Львівська"]
#print(vhi_by_years_and_areas(df, areas, 1994, 2000))