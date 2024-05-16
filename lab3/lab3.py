from spyre import server

import pandas as pd
import urllib2
import json

class StockExample(server.App):
    title = "NOAA data visualization"
    
    inputs = [{'type': 'dropdown',
               'label': 'NOAA data dropdown',
               'options': [{'label': 'VCI', 'value': 'VCI'},
                           {'label': 'TCI', 'value': 'TCI'},
                           {'label': 'VHI', 'value': 'VHI'}],
               'key': 'ticker',
               'action_id': 'update_data'},
              
              {'type': 'dropdown',
              'label': 'Areas',
              'options': [{'label': 'Cherkasy', 'value': 'Cherkasy'},
                          {'label': 'Chernihiv', 'value': 'Chernihiv'},
                          {'label': 'Chernivtsi', 'value': 'Chernivtsi'},
                          {'label': 'Crimea', 'value': 'Crimea'},
                          {'label': "Dnipropetrovs'k", 'value': "Dnipropetrovs'k"},
                          {'label': "Donets'k", 'value': "Donets'k"},
                          {'label': "Ivano-Frankivs'k", 'value': "Ivano-Frankivs'k"},
                          {'label': 'Kharkiv', 'value': 'Kharkiv'},
                          {'label': 'Kherson', 'value': 'Kherson'},
                          {'label': "Khmel'nyts'kyy", 'value': "Khmel'nyts'kyy"},
                          {'label': 'Kiev', 'value': 'Kiev'},
                          {'label': 'Kiev City', 'value': 'Kiev City'},
                          {'label': 'Kirovohrad', 'value': 'Kirovohrad'},
                          {'label': "Luhans'k", 'value': "Luhans'k"},
                          {'label': "L'viv", 'value': "L'viv"},
                          {'label': 'Mykolayiv', 'value': 'Mykolayiv'},
                          {'label': 'Odessa', 'value': 'Odessa'},
                          {'label': 'Poltava', 'value': 'Poltava'},
                          {'label': 'Rivne', 'value': 'Rivne'},
                          {'label': "Sevastopol'", 'value': "Sevastopol'"},
                          {'label': 'Sumy', 'value': 'Sumy'},
                          {'label': "Ternopil'", 'value': "Ternopil'"},
                          {'label': 'Transcarpathia', 'value': 'Transcarpathia'},
                          {'label': 'Vinnytsya', 'value': 'Vinnytsya'},
                          {'label': 'Volyn', 'value': 'Volyn'},
                          {'label': 'Zaporizhzhya', 'value': 'Zaporizhzhya'},
                          {'label': 'Zhytomyr', 'value': 'Zhytomyr'}],
              'key': 'ticker',
              'action_id': 'update_data'}]
    
    inputs = [dict(type = 'text',
                   key = 'range,',
                   label = 'date-ranges',
                   value = '9-10',
                   action_id = 'simple_html_output')]
    
    def getHTML(self, params):
        range = params['range']
        return range