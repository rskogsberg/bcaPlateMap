import os
import pandas as pd
import math
import numpy as np
import re
import datetime
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


class BcaPlateMapGenerator:

    def __init__(self, filename=None):
        """
        Initialize the class
        """
        self.filename = os.path.join('S:/Departments/Analytics/Chemical Analytics/Richard/bcaPlateMaps', filename)
        self.tray_dataframe = pd.read_excel(filename, skiprows=7)
        self.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.dilutionsRegex = re.compile(r'(\d\d?\d?X?)', re.I)
        self.results_dataframe_ = pd.DataFrame(columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index=self.index)
    
    def dilutions():
        self.dilutions_ = []

        for i in range(len(tray_dataframe['Notes'])):
            notes = tray_dataframe['Notes'][i].split(',')
            for j in range(len(notes)):
                self.dilutions_.append(self.dilutionsRegex.findall(notes[j]))
        return self.dilutions_

    def fill_standard_information():
        bsa = 2.000
        for i in range(1,7):
            self.results_dataframe_.loc['A', i] = str(bsa) + ' g/L'
            self.results_dataframe_.loc['B', i] = str(bsa) + ' g/L'
            bsa = bsa / 2

        self.results_dataframe_.loc['A', 7] = self.results_dataframe_.loc['B', 7] = '0.025 g/L'
        self.results_dataframe_.loc['A', 8] = self.results_dataframe_.loc['B', 8] = 'Blank'
        return self.results_dataframe_
    
    def fill_unknown_information():
        table_length = math.ceil(len(self.dilutions_) / 4)
        remainder = len(self.dilutions_) % 4
        j = 0
        sample_num = 1
        for i in range(2, table_length + 2):
            end_cell = 12 - (3*remainder)
            if i is not table_length + 1:
                k = 1
                while k < 11:
                    self.results_dataframe_.loc[self.index[i], k:k+3] = '{0}:{1}'.format(math.floor(sample_num), dilutions[j][0])
                    k += 3
                    j += 1
                    sample_num += 0.5
            elif i == table_length + 1:
                k = 1
                while k <= end_cell - 2:
                    self.results_dataframe_.loc[self.index[i], k:k+2] = '{0}:{1}'.format(math.floor(sample_num), dilutions[j][0])
                    j += 1
                    k += 3
                    sample_num += 0.5
        return self.results_dataframe_
    
    def highlight_standards(s):
        color = '#F0BF60'
        return 'background-color: %s' % color

    def highlight_samples(s):
        color = '#D8E4BC'
        return 'background-color: %s' % color

    def style_dataframe():
        styled_df = self.results_dataframe_.style.set_properties(**{'border-color':'black', 'border-collapse':'collapse'}).applymap(highlight_standards, subset=pd.IndexSlice['A':'B', 1:7]).applymap(highlight_samples, subset=pd.IndexSlice['C':'H', 1:12]).highlight_null(null_color='transparent')
        return styled_df



def hello_world(request):
    filename = request.POST['xls'].filename
    input_file = request.POST['xls'].file
    return Response()


if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_mako')
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()