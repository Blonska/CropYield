import pandas as pd
import numpy as np


class YieldEnergyComponent:

    def _Read_data(self,file_path):
        read_data = pd.read_excel(file_path, sep=' ')
        if read_data.empty:
            raise Exception('Data is empty')
        return read_data


    def Parcing_data(self,dataframe,yot,kt,lt,mt):
        #pd.DataFrame=self._Read_data(file_path)
        self.yot = dataframe['yot']
        self.kt = dataframe['kt']
        self.lt = dataframe['lt']
        self.mt = dataframe['mt']
        return yot,kt,lt,mt
        

    def _TAY(self,Di,Mi):
        '''tay - number of days from the start of the growing season
           Mi - numders month the end of the growing season
           Di - the day of the month the end of the growing season'''

        tay = Di + 30.5 * (Mi - 5) + 10.5
        return tay


    def _XT1(self,Di,Mi):
        '''
        xt1 - the average multi-year sum of active air temperatures for vegetation(Polissya)
        '''

        xt1 = 2829.4 / (1 + 7.7 * np.exp(-0.029 * self._TAY(Di,Mi) - 1.62))
        return xt1


    def _XT2(self,Di,Mi):
        '''
        xt2 - the average multi-year sum of active air temperatures for vegetation(Steppe and Forest-steppe)
        '''

        xt2 = 2712.7 / (1 + 72.9 * np.exp(-0.03 * self._TAY(Di,Mi) - 1.61))
        return xt2


    def YT(self,yb,yot,kt,lt,mt,Mi,Di,region):
        '''yt - energy component of performance
           yb - maximum productivity of culture
           yot,kt,lt,mt - model parameters'''

        if region =='Полісся':
            region=self._XT1(Di,Mi)
        else:
            region=self._XT2(Di,Mi)
        yt = (yb * yot * np.exp(-kt * ((region-lt) ** 2))) / (1 + (100 - yot) * np.exp(-mt * (region - lt)))
        return yt


object = YieldEnergyComponent()
print(object.Parcing_data('D:/ТаблицяБ1.xlsx'))



  

        

      