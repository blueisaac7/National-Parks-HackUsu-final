import datetime
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
#import streamlit as st


class ParkAnalysis:
    def __init__(self):
        # navigate to the folder containing the CSV file
        park_folder_path = 'data/monthlyVisitations'
        w_folder_path = 'data/monthlyWeatherNormals'

        # creates a list of the csv files
        park_csv_lst = os.listdir(park_folder_path)
        park_csv_lst = sorted(park_csv_lst)
        w_csv_lst = os.listdir(w_folder_path)
        w_csv_lst = sorted(w_csv_lst)

        # creates a list of the park names
        self.park_names = []
        for park_name in park_csv_lst:
            park_name = park_name[:-4]
            self.park_names.append(park_name)
            
        #a list of pretty names
        self.pretty_names = ['Acadia', 'American Samoa', 'Arches', 'Badlands', 'Big Bend', 'Biscayne', 'Black Canyon', 'Bryce Canyon',
        'Canyon Lands', 'Capitol Reef', 'Carlsbad Caverns', 'Channel Islands', 'Congaree', 'Crater Lake', 'Cuyahoga Valley', 'Death Valley',
        'Denali', 'Dry Tortugas', 'Everglades', 'Gates of the Arctic', 'Gateway Arch', 'Glacier', 'Glacier Bay', 'Grand Canyon',
        'Grand Teton', 'Great Basin', 'Great Sand Dunes', 'Great Smokey Mountains', 'Guadalupe Mountains', 'Haleakala', 'Hawaii Volcanoes',
        'Hot Springs', 'Indiana Dunes', 'Isle Royale', 'Joshua Tree', 'Katmai', 'Kenai Fjords', 'Kings Canyon', 'Kobuk Valley', 'Lake Clark',
        'Lassen Volcanic', 'Mammoth Cave', 'Mesa Verde', 'Mount Rainer', 'New River Gorge', 'North Cascades', 'Olympic', 'Petrified Forest',
        'Pinnacles', 'Redwood', 'Rocky Mountain', 'Saguaro', 'Sequoia', 'Shenandoah', 'Theodore Roosevelt', 'Virgin Islands', 'Voyageurs',
        'White Sands', 'Wind Cave', 'Wolf Trap', 'Yellowstone', 'Yosemite', 'Zion']

        # list of month names
        self.months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'AnnualTotal']

        self.realmonths =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        # creates a dictionary of park names and visitor tables
        self.visitor_df_dct = {}
        i = 0
        for park_csv in park_csv_lst:
            file_path = os.path.join(park_folder_path, park_csv)

            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                rows = list(csvreader)

            del rows[:3]

            df = pd.DataFrame(rows[1:], columns=rows[0])
            df = df.drop(df.index[-1])
            df = df.drop(df.columns[-1], axis=1)

            for month in self.months:
                df[month] = df[month].replace(',', '', regex=True)

            self.visitor_df_dct[self.park_names[i]] = df
            i += 1

        # creates a dictionary of park names and weather tables
        self.weather_df_dct = {}
        j = 0
        for w_csv in w_csv_lst:
            file_path = os.path.join(w_folder_path, w_csv)

            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                rows = list(csvreader)

            w_df = pd.DataFrame(rows[1:], columns=rows[0])
            w_df = w_df[['LATITUDE','LONGITUDE','month','MLY-TAVG-NORMAL','MLY-PRCP-NORMAL']]
            w_df = w_df.rename(columns={'month': 'MONTH', 'MLY-TAVG-NORMAL': 'TEMP', 'MLY-PRCP-NORMAL': 'PRCP'})

            self.weather_df_dct[self.park_names[j]] = w_df
            j += 1

        url_names = []
        for idx in range(len(self.weather_df_dct.keys())):
            url_names += [f'<a target="root" href="/park?name={list(self.weather_df_dct.keys())[idx]}">{self.pretty_names[idx]}</a>']

        self.parks_df_dct = {
            "Name": url_names,
            "RealName": self.pretty_names,
            "Latitude": [self.weather_df_dct[name]['LATITUDE'][0] for name in self.weather_df_dct.keys()],
            "Longitude": [self.weather_df_dct[name]['LONGITUDE'][0] for name in self.weather_df_dct.keys()]
        }

    # function calculates best months to visit the park
    def best_months(self, park, min_temp, max_temp, prcp):
        month_avgs = []
        i=0

        for month in self.months:
            self.visitor_df_dct[park][month] = self.visitor_df_dct[park][month].astype(int)
            visitor_average = self.visitor_df_dct[park][month].mean()
            month_avgs.append(visitor_average)

        month_avgs.pop(-1)

        self.weather_df_dct[park]['TEMP'] = [float(a.strip(' ')) for a in self.weather_df_dct[park]['TEMP'].tolist()]
        temp_list = self.weather_df_dct[park]['TEMP'].tolist()

        self.weather_df_dct[park]['PRCP'] = [float(a.strip(' ')) for a in self.weather_df_dct[park]['PRCP'].tolist()]
        prcp_list = self.weather_df_dct[park]['PRCP'].tolist()

        prcp_range = max(prcp_list)-min(prcp_list)
        prcp_mid = min(prcp_list) + (prcp_range/2)

        if (prcp=='Low'):
            prcp_done = min(prcp_list)
        elif(prcp=='Medium-Low'):
            prcp_done = min(prcp_list) + (prcp_range/4)
        elif(prcp=='Medium'):
            prcp_done = min(prcp_list) + (prcp_range/2)
        elif(prcp=='Medium-High'):
            prcp_done = prcp_mid + (prcp_range/4)
        else:
            prcp_done = max(prcp_list)

        sorted_months = sorted(month_avgs)

        contenders = []
        for i in range(12):
            if min_temp < temp_list[i] < max_temp and prcp_list[i] < prcp_done:
                contenders.append(sorted_months[i])
            else:
                continue
        indices = [month_avgs.index(value) for value in contenders]

        top_3 = []
        for index in indices:
            top_3.append(self.realmonths[index])
        if len(top_3) == 3:
            top_3.insert(0,"Your top 3 months to visit " + self.pretty_names[self.park_names.index(park)] + " are")
            return top_3
        elif len(top_3) > 3:
            num = len(top_3)
            #top_3.pop(-(num-3))
            top_3.insert(0,"Your top 3 months to visit " + self.pretty_names[self.park_names.index(park)] + " are")
            return top_3[0:4]
        elif len(top_3) < 3:
            num = len(top_3)
            if num == 1:
                top_3.insert(0,'Your weather requirements of temperature and precipitation allow for only one month.')
            elif num == 2:
                top_3.insert(0,'Your requirements of temperature and precipitation allow for only two months.')
            else:
                top_3.insert(0,'Your requirements do not allow for any months to be chosen')
        return top_3

    current_month = datetime.datetime.now().month

    def best_parks(self, min_temp, max_temp, prcp):
        now_month = self.months[self.current_month - 1]
        avgs = []
        avg = 0
        for key, value in self.visitor_df_dct.items():
            for i in range(3):
                avg += int(value['MAR'][i])
            avg = avg / 3
            if (int(value['MAR'][0]) != 0):
                avg = avg / int(value['MAR'][0])
            avgs.append(avg)

        temp_list = []
        for key, value in self.weather_df_dct.items():
            temp = [float(a.strip(' ')) for a in value['TEMP'].tolist()]
            temp_val = temp[2]
            temp_list.append(temp_val)

        prcp_list = []
        for key, value in self.weather_df_dct.items():
            prcp = [float(a.strip(' ')) for a in value['PRCP'].tolist()]
            prcp_val = prcp[2]
            prcp_list.append(prcp_val)


        prcp_range = max(prcp_list)-min(prcp_list)
        prcp_mid = min(prcp_list) + (prcp_range/2)

        if (prcp=='Low'):
            prcp_done = min(prcp_list)
        elif(prcp=='Medium-Low'):
            prcp_done = min(prcp_list) + (prcp_range/4)
        elif(prcp=='Medium'):
            prcp_done = min(prcp_list) + (prcp_range/2)
        elif(prcp=='Medium-High'):
            prcp_done = prcp_mid + (prcp_range/4)
        else:
            prcp_done = max(prcp_list)

        sorted_avgs = sorted(avgs)

        rank = [avgs.index(value) for value in sorted_avgs]

        park_contenders = []
        for i in range(62):
            if min_temp < temp_list[i] < max_temp and prcp_list[i] < prcp_done:
                park_contenders.append(self.pretty_names[rank[i]])
            else:
                continue
        if len(park_contenders) == 0:
            park_contenders.append("No Months fit your criteria")
        return park_contenders[0:5]

    def line_chart(self, park):
        avgs = []
        avg = 0
        data_frame = self.visitor_df_dct[park]
        for j in range(12):
            for i in range(3):
                avg += int(data_frame[self.months[j]][i])
            avg = avg / 3
            avgs.append(avg)
        return avgs

    def get_pretty(self,name):
        loc = self.park_names.index(name)
        return self.pretty_names[loc]