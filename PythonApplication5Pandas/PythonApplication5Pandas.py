import pandas as pd
import numpy as np
import copy


class YieldEnergyComponent:

    def _read_data(self,data):
        read_data = pd.read_excel(data, sep=' ')
        if read_data.empty:
            raise Exception('Data is empty')
        return read_data

    #ТаблицяБ11,ТаблицяБ21,ТаблицяБ31
    def _parcing_data(self,data,culture=None,param=None,border=None):
        self.data1 = self._read_data(data)
        if not culture==None:
            self.data1= self.data1.loc[self.data1['Культура'] == culture]
        if not param==None:
            self.data1=self.data1.loc[self.data1['Параметр'].isin([param])]
        if not border==None:
            self.data1=self.data1.loc[self.data1['Межа'].isin([border])]
        return self.data1
    
    #data from ТаблицяБ21
    def _tay(self,data=None,Di=None,Mi=None,culture=None,border=None):
        if Di==None:
            Di=self._parcing_data(data,culture,'Di',border)
        if Mi==None:
            Mi=self._parcing_data(data,culture,'Mi',border)
        '''tay - number of days from the start of the growing season
           Mi - numders month the end of the growing season
           Di - the day of the month the end of the growing season'''

        tay = Di.iat[0,3] + 30.5 * ((Mi.iat[0,3]) - 5) + 10.5
        return tay


    def _xt1(self,data=None,Di=None,Mi=None,culture=None,border=None):
        '''
        xt1 - the average multi-year sum of active air temperatures for vegetation(Polissya)
        '''

        xt1 = 2829.4 / (1 + 7.7 * np.exp(-0.029 * self._tay(data,Di,Mi,culture,border) - 1.62))
        return xt1


    def _xt2(self,data=None,Di=None,Mi=None,culture=None,border=None):
        '''
        xt2 - the average multi-year sum of active air temperatures for vegetation(Steppe and Forest-steppe)
        '''

        xt2 = 2712.7 / (1 + 72.9 * np.exp(-0.03 * self._tay(data,Di,Mi,culture,border) - 1.61))
        return xt2


    def YT(self,data=None,data1=None,Mi=None,Di=None,culture=None,border=None,yb=None,yot=None,kt=None,lt=None,mt=None,region=None):
        '''yt - energy component of performance
           yb - maximum productivity of culture
           yot,kt,lt,mt - model parameters'''
        if yb==None:
            yb=self._parcing_data(data1,culture,'yb',border)
        if yot==None:
            yot=self._parcing_data(data1,culture,'yot',border)
        if lt==None:
            lt=self._parcing_data(data1,culture,'lt',border)
        if mt==None:
            mt=self._parcing_data(data1,culture,'mt',border)
        reg = lambda : self._xt1(data,Di,Mi,culture,border) if region=='Полісся' else self._xt2(data,Di,Mi,culture,border)
        yt = (yb * yot * np.exp(-kt * ((reg() - lt) ** 2))) / (1 + (100 - yot) * np.exp(-mt * (reg() - lt)))
        return yt

class YieldSoilComponent:

    #ТаблицяБ41
    def _parcing_data1(self,data,culture=None,soilparam=None,param=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not culture==None:
            self.data1 = self.data1.loc[self.data1['Культура'] == culture]
        if not soilparam==None:
            self.data1 = self.data1.loc[self.data1['Грунтовий показник'].isin([soilparam])]
        if not param==None:
            self.data1 =self.data1.loc[self.data1['Параметр'].isin([param])]
        return self.data1

    #ТаблицяБ5
    def _parcing_data2(self,data,zone=None,soil_type=None,granulometric_composition=None,border=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not zone==None:
            self.data1= self.data1.loc[self.data1['Зона'] == zone]
        if not soil_type==None:
            self.data1=self.data1.loc[self.data1['Тип грунту'].isin([soil_type])]
        if not granulometric_composition==None and border==None:
            self.data1=self.data1.loc[self.data1['Гранулометричний склад '].isin([granulometric_composition])]
        if not border==None:
            self.data1=self.data1.loc[self.data1['Межа'].isin([border]) ]
        return self.data1

    #ТаблицяБ61
    def _parcing_data3(self,data,soilparam=None,param1=None,param2=None,param3=None,param4=None,param5=None,hama1=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not soilparam==None:
            self.data1=self.data1.loc[self.data1['Грунтовий показник'] == soilparam]
        if not param1==None:
            self.data1=self.data1.loc[self.data1['Поживні речовини'].isin([param1])]
        if not param2==None:
            self.data1=self.data1.loc[self.data1['Вода в грунті'].isin([param2])]
        if not param3==None:
            self.data1=self.data1.loc[self.data1['Кореневмісний об. грунту '].isin([param3])]
        if not param4==None:
            self.data1=self.data1.loc[self.data1['Повітря в грунті'].isin([param4])]
        if not param5==None:
            self.data1=self.data1.loc[self.data1['Відсутність шкідливих для рослин речовин'].isin([param5])]
        if not hama1==None:
            self.data1=self.data1.loc[self.data1['Гама1'].isin([hama1]) ]
        return self.data1

    #ТаблицяБ62
    def _parcing_data4(self,data,soilparam=None,G=None,Eh=None,d=None,H=None,P=None,K=None,pH=None,h=None,W=None,hama2=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not soilparam==None:
            self.data1= self.data1.loc[self.data1['Грунтовий показник'] == soilparam]
        if not G==None:
            self.data1=self.data1.loc[self.data1['G'].isin([G])]
        if not Eh==None:
            self.data1=self.data1.loc[self.data1['Eh'].isin([Eh])]
        if not d==None:
            self.data1=self.data1.loc[self.data1['D'].isin([d])]
        if not H==None:
            self.data1=self.data1.loc[self.data1['H'].isin([H])]
        if not P==None:
            self.data1=self.data1.loc[self.data1['P'].isin([P])]
        if not K==None:
            self.data1=self.data1.loc[self.data1['K'].isin([K])]
        if not pH==None:
            self.data1=self.data1.loc[self.data1['pH'].isin([pH])]
        if not h==None:
            self.data1=self.data1.loc[self.data1['h'].isin([h])]
        if not W==None:
            self.data1=self.data1.loc[self.data1['W'].isin([W])]
        if not hama2==None:
            self.data1=self.data1.loc[self.data1['Гама2'].isin([hama2])]
        return self.data1

    #ТаблицяБ6
    def _parcing_data5(self,data,param=None,diraction=None,mark1=None,medaction=None,mark2=None,hama3=None):
         self.data1 = YieldEnergyComponent._read_data(self,data)
         if not param==None:
             self.data1= self.data1.loc[self.data1['Показник'] == param]
         if not diraction==None:
             self.data1=self.data1.loc[self.data1['Прямі заходи'].isin([diraction])]
         if not mark1==None:
             self.data1=self.data1.loc[self.data1['Бали1'].isin([mark1])]
         if not medaction==None:
             self.data1=self.data1.loc[self.data1['Опосередковані заходи'].isin([medaction])]
         if not mark2==None:
             self.data1=self.data1.loc[self.data1['Бали2'].isin([mark2])]
         if not hama3==None:
             self.data1=self.data1.loc[self.data1['Гама3'].isin([hama3])]
         return self.data1
    
    def _hama(hama1=None,hama2=None,hama3=None):
        if hama1==None:
            hama1=self._parcing_data3(data,soilparam,param,param2,param3,param4,param5,'Гама1')
        if hama2==None:
            hama2=self._parcing_data4(data,soilparam,G,Eh,d,H,P,K,pH,h,W,'Гама2')
        if hama3==None:
            hama3=self._parcing_data5(data,param,diraction,mark1,medaction,mark2,'Гама')
        hama=1 / 3 * (hama1 + hama2 + hama3)
        return hama

    def YP(self,nf,nl,ns,nd,kf,kwt,kl,ks,kd,ki,kh,kw,yb,yop,kp,xp,lp,mp):
        '''nf - number of damages due to freezing
           nl - number of damages for crumble grains?
           ns - number of damages due to hailstones 
           nd - number of damages due to drought
           kf  - аmendment in case of frost
           kwt - coefficient of unfavorable conditions of the summer-autumn period and wintering for winter crops
           ks - amendment in case of hail
           kl - amendment for crumble grains?
           kd - amendment for drought
           ki - amendment for illness
           kh - amendment for pests
           kw - amendment on weeds
           yb - maximum productivity of culture
           yop,kp,lp,mp - parameters of the model of tolerance
           xp - meaning of soil indicators
        '''
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if yb==None:
            yb=YieldEnergyComponent._parcing_data(data,culture,'yb',border)
        if yop==None:
            yop=self._parcing_data1(data,culture,soilparam,'yop')
        if kp==None:
            kp=self._parcing_data1(data,culture,soilparam,'kp')
        if lp==None:
            kp=self._parcing_data1(data,culture,soilparam,'lp')
        if mp==None:
            kp=self._parcing_data1(data,culture,soilparam,'mp')

        #xp(_parcing_data2)ТаблицяБ5
        yp = hama * (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kp * ((xp - lp) ** 2))) / (1 + (100 - yop) * np.exp(-mp * (xp - lp)))
        return yp

class WeighSoilComponent:

    #ТаблицяБ7
    def _parcing_data(self,data,param=None,alfa1=None,alfa2=None,param1=None,mark1=None,param2=None,mark2=None,alfa3=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not param==None:
            self.data1= self.data1.loc[self.data1['Параметр продуктивності '] == param]
        if not alfa1==None:
            self.data1=self.data1.loc[self.data1['Alfa f1'].isin([alfa1])]
        if not alfa2==None:
            self.data1=self.data1.loc[self.data1['Alfa f2'].isin([alfa2])]
        if not param1==None:
            self.data1=self.data1.loc[self.data1['Заходи безпосереднього впливу'].isin([alfa3])]
        if not mark1==None:
            self.data1=self.data1.loc[self.data1['Бали1'].isin([mark1])]
        if not param2==None:
            self.data1=self.data1.loc[self.data1['Заходи опосередкованого впливу'].isin([param1])]
        if not mark2==None:
            self.data1=self.data1.loc[self.data1['Бали2'].isin([param2])]
        if not alfa3==None:
            self.data1=self.data1.loc[self.data1['Alfa f3'].isin([Alfa3])]
        return self.data1

    def _alfa(self,data=None,alfa1=None,alfa2=None,alfa3=None):
        if alfa1==None:
            alfa1=self.data1[self.data1['Alfa f1'] == alfa1]
        if alfa2==None:
            alfa2=self.data1[self.data1['Alfa f2'] == alfa2]
        if alfa3==None:
            alfa3=self.data1[self.data1['Alfa f3'] == alfa3]
        alfa=1 / 3 * (alfa1 + alfa2 + alfa3)
        return alfa

    def YP(self,nf,nl,ns,nd,kf,kwt,kl,kd,ki,kh,kw,alfal,alfag,alfat,alfab,yl,yg,yt,yb):
         yp = nf * nl * ns * nd * kf * kwt * kl * kd * ki * kh * kw * (alfal * yl + alfag * yg + alfat * yt + alfab * yb)
         return yp

class CumulativeSoilComponent:
     #ТаблицяБ8
     def _parcing_data(self,data,param=None,units=None,value=None,typeofsoil=None,xij=None,xij2=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not param==None:
            self.data1= self.data1.loc[self.data1['Показник'] == param]
        if not units==None:
            self.data1=self.data1.loc[self.data1['Одиниці виміру'].isin([units])]
        if not value==None:
            self.data1=self.data1.loc[self.data1['Значення'].isin([value])]
        if not typeofsoil==None:
            self.data1=self.data1.loc[self.data1['Тип грунту'].isin([typeofsoil])]
        return self.data1

     def _q(self,xij=None,xij2=None):
         if xij==None:
            xij=self.data1.loc[self.data1['xij'] == xij]
         if xij2==None:
            xij2=self.data1.loc[self.data1['xij2'] == xij2]
         if xij < 2 * xij2:
             return 1 - (np.abs(xij2 - xij) / xij2)
         else:
             return 0

     def YS(self,nf,nl,ns,nd,kf,kwt,kl,kd,ki,kh,kw,yb,q):
         ys = (nf * nl * ns * nd * kf * kwt * kl * kd * ki * kh * kw * yb * 0.08 * np.exp(-1.66 * (self._q(xij,xij2)- 0.24) ^ 2))/(0.01 + 0.92 * np.exp(-4.992 * (self._q(xij,xij2) - 0.24)))
         return ys

class Productivityofland:
     #ТаблицяБ9
     def _parcing_data(self,data,culture=None,param=None,value=None):
        self.data1 = YieldEnergyComponent._read_data(self,data)
        if not culture==None:
            self.data1= self.data1.loc[self.data1['Культура'] == culture]
        if not param==None:
            self.data1=self.data1.loc[self.data1['Параметр'].isin([param])]
        if not value==None:
            self.data1=self.data1.loc[self.data1['Значення параметра'].isin([value])]
        return self.data1

     def YE(self,data,Cs=None,Cl=None,yl=None,ys=None,culture=None,value=None):
        if Cs==None:
            yop=self._parcing_data(data,culture,'Cs',value)
        if Cs==None:
            yop=self._parcing_data(data,culture,'Cl',value)
        ye = Cs * ys + Cl * yl
        return ye

     def P(self,ye,yb,nf,nl,ns,nd,kf,kwt,kl,kd,ki,kh,kw):
         p = ye / (nf * nl * ns * nd * kf * kwt * kl * kd * ki * kh * kw * yb)
         return p
    

object = WeighSoilComponent()
print(object._parcing_data(data='D:\ТаблицяБ7.xlsx'))

#if __name__ == "__main__":
    #yield_soil_component = YieldSoilComponent()
    #data = yield_soil_component._read_data('D:\Зона.xlsx')
    #new_data = data.loc[data["Зона"] == 'Поліська']
    #print(new_data.loc[new_data['Тип грунту'] == 'Дернові опідзолені'])
    #new_data1 = data.loc[(data['Зона'] == 'Поліська')  & data['Тип грунту'].isin(['Дернові опідзолені']) & data['Гранулометричний склад '].isin(['Піщані']) & data['Межа'].isin(['Нижня']) ]
    #print(new_data1)




  

        

      
