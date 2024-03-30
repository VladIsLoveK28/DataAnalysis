import urllib.request
import datetime
import os

def download():
    folder_path = 'C:\\Users\\vladi\\PycharmProjects\\DataAnalysis\\lab2\\csv_files'
    print('Downloading VHI files...')
    for i in range(1,28):
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
download()