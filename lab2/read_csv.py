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
        df['empty'] = df['empty'].apply(lambda x: 0 if pd.isnull(x) else x)

        df['area'] = i+1

        df['Year'] = df['Year'].str.replace('<tt><pre>', '')
        df = df.drop(df[df['Year'] == '</pre></tt>'].index)
        df['Year'] = df['Year'].astype(int)

        main_df = pd.concat([main_df, df])
    return main_df
    
def change_index(df):
    new_index = {
        1: 22,
        2: 24,
        3: 23,
        4: 25,
        5: 3,
        6: 4,
        7: 8,
        8: 19,
        9: 20,
        10: 21,
        11: 9,
        12: 9,
        13: 10,
        14: 11,
        15: 12,
        16: 13,
        17: 14,
        18: 15,
        19: 16,
        20: 25,
        21: 17,
        22: 18,
        23: 6,
        24: 1,
        25: 2,
        26: 7,
        27: 5
    }
    df['area'] = df['area'].map(new_index)
    return df

def extremum(df, index, year):
    min = df[(df['Year'] == year) & (df['area'] == index)]['VHI'].min()
    max = df[(df['Year'] == year) & (df['area'] == index)]['VHI'].max()
    print(f'Мінімальне значення VHI за {year} рік в регіоні {index}: {min}')
    print(f'Максимальне значення VHI за {year} рік в регіоні {index}: {max}')

def vhi_by_years_and_areas(df, areas, start_year, end_year):
    selected_data = pd.DataFrame()
    for area in areas:
        area_data = df[(df['area'] == area) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]
        selected_data = pd.concat([selected_data, area_data[['Year', 'VHI', 'area']]], axis=1)
    return selected_data

def extreme_droughts(df):
    extreme_droughts = df[df['VHI'] <= 15]
    extreme_droughts_by_year = extreme_droughts.groupby('Year')['area'].nunique()
    percent = 10 
    extreme_drought_years = extreme_droughts_by_year[extreme_droughts_by_year > (len(df['area'].unique()) * percent / 100)]

    print("Екстремальні посухи торкнулися більше {}% областей в наступні роки:".format(percent))
    print(extreme_drought_years) 

def moderate_droughts(df):
    moderate_droughts = df[df['VHI'] <= 35]
    moderate_droughts_by_year = moderate_droughts.groupby('Year')['area'].nunique()
    percent = 20
    moderate_drought_years = moderate_droughts_by_year[moderate_droughts_by_year > (len(df['area'].unique()) * percent / 100)]
    
    print("Помірні посухи торкнулися більше {}% областей в наступні роки:".format(percent))
    print(moderate_drought_years)


#df = extract(directory)
df = change_index(extract(directory))

#extremum(df, 12, 2004)

#areas = [1, 5, 12, 24]
#print(vhi_by_years_and_areas(df, areas, 1994, 2000))

#extreme_droughts(df)
moderate_droughts(df)
#print(df)