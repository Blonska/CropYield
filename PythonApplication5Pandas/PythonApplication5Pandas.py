import pandas as pd
import numpy as np


class YieldEnergyComponent:

    def _Read_data(self,file_path):
        read_data = pd.read_excel(file_path, sep=' ')
        if read_data.empty:
            raise Exception('Data is empty')
        return read_data


    def _Parcing_data(self,dataframe,uyb,lyb,yot,kt,lt,mt,Di,Mi):
        #pd.DataFrame=self._Read_data(file_path)
        self.lyb = dataframe['lyb']
        self.uyb = dataframe['uyb']
        self.yot = dataframe['yot']
        self.kt = dataframe['kt']
        self.lt = dataframe['lt']
        self.mt = dataframe['mt']
        self.Di = dataframe['Di']
        self.Mi = dataframe['Mi']
        return lyb,uyb,yot,kt,lt,mt,Di,Mi
        

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
        yb = lambda x: self._Parcing_data['uyb'] if x=='upper limit' else self._Parcing_data['lyb']
        region = lambda x: self._XT1(Di,Mi) if _XT1=='Полісся' else self._XT2(Di,Mi)
        yt = (yb * yot * np.exp(-kt * ((region - lt) ** 2))) / (1 + (100 - yot) * np.exp(-mt * (region - lt)))
        return yt

class YieldSoilComponent:

    def _Read_data(self,file_path):
        read_data = pd.read_excel(file_path, sep=' ')
        if read_data.empty:
            raise Exception('Data is empty')
        return read_data

    def _Parcing_data(self,dataframe,lkf,lkwt,lks,lkl,lkd,lki,lkh,lkw,ukf,ukwt,uks,ukl,ukd,uki,ukh,ukw):
        self.lkf = dataframe['lkf']
        self.lkwt = dataframe['lkwt']
        self.lks = dataframe['lks']
        self.lkl = dataframe['lkl']
        self.lkd = dataframe['lkd']
        self.lki = dataframe['lki']
        self.lkh = dataframe['lkh']
        self.lkw = dataframe['lkw']
        self.ukf = dataframe['ukf']
        self.ukwt = dataframe['ukwt']
        self.uks = dataframe['uks']
        self.ukl = dataframe['ukl']
        self.ukd = dataframe['ukd']
        self.uki = dataframe['uki']
        self.ukh = dataframe['ukh']
        self.ukw = dataframe['ukw']
        return lkf,lkwt,lks,lkl,lkd,lki,lkh,lkw,ukf,ukwt,uks,ukl,ukd,uki,ukh,ukw

    def _Parcing_data1(self,dataframe,mpg,kpg,lpg,yopg,mpw,kpw,lpw,yopw,mpd,kpd,lpd,yopd,mph,kph,lph,yoph,mpk,kpk,lpk,yopk,mpp,kpp,lpp,yopp):
        self.mpg = dataframe['mpg']
        self.kpg = dataframe['kpg']
        self.lpg = dataframe['lpg']
        self.yopg = dataframe['yopg']
        self.mpw = dataframe['mpw']
        self.kpw = dataframe['kpw']
        self.lpw = dataframe['lpw']
        self.yopw = dataframe['yopw']
        self.mpd = dataframe['mpd']
        self.kpd = dataframe['kpd']
        self.lpd = dataframe['lpd']
        self.yopd = dataframe['yopd']
        self.mph = dataframe['mph']
        self.kph = dataframe['kph']
        self.lph = dataframe['lph']
        self.yoph = dataframe['yoph']
        self.mpk = dataframe['mpk']
        self.kpk = dataframe['kpk']
        self.lpk = dataframe['lpk']
        self.yopk = dataframe['yopk']
        self.mpp = dataframe['mpp']
        self.kpp = dataframe['kpp']
        self.lpp = dataframe['lpp']
        self.yopp = dataframe['yopp']
        return mpg,kpg,lpg,yopg,mpw,kpw,lpw,yopw,mpd,kpd,lpd,yopd,mph,kph,lph,yoph,mpk,kpk,lpk,yopk,mpp,kpp,lpp,yopp


    def _XP_Polissya_Sod_Podzolized_Soils(self,dataframe,pdopn,pdopv,pdozpn,pdozpv,pdosn,pdosv,pdolsn,pdolsv,pdossn,pdossv,pdovsn,pdovsv,pdohn,pdohv):
        '''The value of soil indicators Polissya zone - sod-podzolized soils:
        pdopn - sandy soils(lower limit)
        pdopv - sandy soils(upper limit)
        pdozpn - bind-sandy soils(lower limit)
        pdozpv - bind-sandy soils(upper limit)
        pdosn - sandy loam sand(lower limit)
        pdosv - sandy loam sand(upper limit)
        pdolsn - loam sand soils(lower limit)
        pdolsv - loam sand soils(upper limit)
        pdossn - sandy clay loam soils(lower limit)
        pdossv - sandy clay loam soils(upper limit)
        pdovsn -  silty clay loam soils(lower limit)
        pdovsv - silty clay loam soils(upper limit)
        pdohn - clay soils(lower limit)
        pdohn - clay soils(upper limit)
        '''

        self.pdopn = dataframe['ПДОПН']
        self.pdopv = dataframe['ПДОПВ']
        self.pdozpn = dataframe['ПДОЗПН']
        self.pdozpv = dataframe['ПДОЗПВ']
        self.pdosn = dataframe['ПДОСН']
        self.pdosv = dataframe['ПДОСВ']
        self.pdolsn = dataframe['ПДОЛСН']
        self.pdolsv = dataframe['ПДОЛСВ']
        self.pdossn = dataframe['ПДОССН']
        self.pdossv = dataframe['ПДОССВ']
        self.pdovsn = dataframe['ПДОВСН']
        self.pdovsv = dataframe['ПДОВСВ']
        self.pdohn = dataframe['ПДОГН']
        self.pdohv = dataframe['ПДОГВ']
        return pdopn,pdopv,pdozpn,pdozpv,pdosn,pdosv,pdolsn,pdolsv,pdossn,pdossv,pdovsn,pdovsv,pdohn,pdohv
   

    def _XP_Polissya_Sod_Podzolized_Gley_Soils(self,dataframe,pdohpn,pdohpv,pdohzpn,pdohzpv,pdohsn,pdohsv,pdohlsn,pdohlsv,pdohssn,pdohssv,pdohvsn,pdohvsv,pdohhn,pdohhv):
        '''The value of soil indicators Polissya zone - sod-podzolized gley soils:
        pdohpn - sandy soils(lower limit)
        pdohpv - sandy soils(upper limit)
        pdohzpn - bind-sandy soils(lower limit)
        pdohzpv - bind-sandy soils(upper limit)
        pdohsn - sandy loam sand(lower limit)
        pdohsv - sandy loam sand(upper limit)
        pdohlsn - loam sand soils(lower limit)
        pdohlsnv - loam sand soils(upper limit)
        pdohssn - sandy clay loam soils(lower limit)
        pdohssv - sandy clay loam soils(upper limit)
        pdohvsn -  silty clay loam soils(lower limit)
        pdohvsv - silty clay loam soils(upper limit)
        pdohhn - clay soils(lower limit)
        pdohhn - clay soils(upper limit)
        '''
    
        self.pdohpn = dataframe['ПДОГПН']
        self.pdohpv = dataframe['ПДОГПВ']
        self.pdohzpn = dataframe['ПДОГЗПН']
        self.pdohzpv = dataframe['ПДОГЗПВ']
        self.pdohsn = dataframe['ПДОГСН']
        self.pdohsv = dataframe['ПДОГСВ']
        self.pdohlsn = dataframe['ПДОГЛСН']
        self.pdohlsv = dataframe['ПДОГЛСВ']
        self.pdohssn = dataframe['ПДОГССН']
        self.pdohssv = dataframe['ПДОГССВ']
        self.pdohvsn = dataframe['ПДОГВСН']
        self.pdohvsv = dataframe['ПДОГВСВ']
        self.pdohhn = dataframe['ПДОГГН']
        self.pdohhv = dataframe['ПДОГГВ']
        return pdohpn,pdohpv,pdohzpn,pdohzpv,pdohsn,pdohsv,pdohlsn,pdohlsv,pdohssn,pdohssv,pdohvsn,pdohvsv,pdohhn,pdohhv


    def _XP_Polissya_Sod_Podzoliс_Soils(self,dataframe,pdphpn,pdphpv,pdphzpn,pdphzpv,pdphsn,pdphsv,pdphlsn,pdphlsv,pdphssn,pdphssv,pdphvsn,pdphvsv,pdphhn,pdphhv):
        '''The value of soil indicators Polissya zone - sod-podzolic soils:
        pdphpn - sandy soils(lower limit)
        pdphpv - sandy soils(upper limit)
        pdphzpn - bind-sandy soils(lower limit)
        pdphzpv - bind-sandy soils(upper limit)
        pdphsn - sandy loam sand(lower limit)
        pdphsv - sandy loam sand(upper limit)
        pdphlsn - loam sand soils(lower limit)
        pdphlsv - loam sand soils(upper limit)
        pdphssn - sandy clay loam soils(lower limit)
        pdphssv - sandy clay loam soils(upper limit)
        pdphvsn -  silty clay loam soils(lower limit)
        pdphvsv - silty clay loam soils(upper limit)
        pdphhn - clay soils(lower limit)
        pdphhv - clay soils(upper limit)
        '''

        self.pdphpn = dataframe['ПДПГПН']
        self.pdphpv = dataframe['ПДПГПВ']
        self.pdphzpn = dataframe['ПДПГЗПН']
        self.pdphzpv = dataframe['ПДПГЗПВ']
        self.pdphsn = dataframe['ПДПГСН']
        self.pdphsv = dataframe['ПДПГСВ']
        self.pdphlsn = dataframe['ПДПГЛСН']
        self.pdphlsv = dataframe['ПДПГЛСВ']
        self.pdphssn = dataframe['ПДПГССН']
        self.pdphssv = dataframe['ПДПГССВ']
        self.pdphvsn = dataframe['ПДПГВСН']
        self.pdphvsv = dataframe['ПДПГВСВ']
        self.pdphhn = dataframe['ПДПГГН']
        self.pdphhv = dataframe['ПДПГГВ']
        return pdphpn,pdphpv,pdphzpn,pdphzpv,pdphsn,pdphsv,pdphlsn,pdphlsv,pdphssn,pdphssv,pdphvsn,pdphvsv,pdphhn,pdphhv
       

    def _XP_Polissya_Meadow_Soils(self,dataframe,plhpn,plhpv,plhzpn,plhzpv,plhsn,plhsv,plhlsn,plhlsv,plhssn,plhssv,plhvsn,plhvsv,plhhn,plhhv):
        '''The value of soil indicators Polissya zone - meadow soils:
        plhpn - sandy soils(lower limit)
        plhpv - sandy soils(upper limit)
        plhzpn - bind-sandy soils(lower limit)
        plhzpv - bind-sandy soils(upper limit)
        plhsn - sandy loam sand(lower limit)
        plhsv - sandy loam sand(upper limit)
        plhlsn - loam sand soils(lower limit)
        plhlsv - loam sand soils(upper limit)
        plhssn - sandy clay loam soils(lower limit)
        plhssv - sandy clay loam soils(upper limit)
        plhvsn -  silty clay loam soils(lower limit)
        plhvsv - silty clay loam soils(upper limit)
        plhhn - clay soils(lower limit)
        plhhv - clay soils(upper limit)
        '''

        self.plhpn = dataframe['ПЛГПН']
        self.plhpv = dataframe['ПЛГПВ']
        self.plhzpn = dataframe['ПЛГЗПН']
        self.plhzpv = dataframe['ПЛГЗПВ']
        self.plhsn = dataframe['ПЛГСН']
        self.plhsv = dataframe['ПЛГСВ']
        self.plhlsn = dataframe['ПЛГЛСН']
        self.plhlsv = dataframe['ПЛГЛСВ']
        self.plhssn = dataframe['ПЛГССН']
        self.plhssv = dataframe['ПЛГССВ']
        self.plhvsn = dataframe['ПЛГВСН']
        self.plhvsv = dataframe['ПЛГВСВ']
        self.plhhn = dataframe['ПЛГГН']
        self.plhhv = dataframe['ПЛГГВ']
        return plhpn,plhpv,plhzpn,plhzpv,plhsn,plhsv,plhlsn,plhlsv,plhssn,plhssv,plhvsn,plhvsv,plhhn,plhhv


    def _XP_Forest_Steppe_Gray_Forest_Soils(self,dataframe,lslpn,lslpv,lslzpn,lslzpv,lslsn,lslsv,lsllsn,lsllsv,lslssn,lslssv,lslvsn,lslvsv,lslhn,lslhv):
        '''The value of soil indicators Forest Steppe zone - gray forest soils:
        lslpn - sandy soils(lower limit)
        lslpv - sandy soils(upper limit)
        lslzpn - bind-sandy soils(lower limit)
        lslzpv - bind-sandy soils(upper limit)
        lslsn - sandy loam sand(lower limit)
        lslsv - sandy loam sand(upper limit)
        lsllsn - loam sand soils(lower limit)
        lsllsv - loam sand soils(upper limit)
        lslssn - sandy clay loam soils(lower limit)
        lslssv - sandy clay loam soils(upper limit)
        lslvsn -  silty clay loam soils(lower limit)
        lslvsv - silty clay loam soils(upper limit)
        lslhn - clay soils(lower limit)
        lslhn - clay soils(upper limit)
        '''

        self.lslpn = dataframe['ЛСЛПН']
        self.lslpv = dataframe['ЛСЛПВ']
        self.lslzpn = dataframe['ЛСЛЗПН']
        self.lslzpv = dataframe['ЛСЛЗПВ']
        self.lslsn = dataframe['ЛСЛСН']
        self.lslsv = dataframe['ЛСЛСВ']
        self.lsllsn = dataframe['ЛСЛЛСН']
        self.lsllsv = dataframe['ЛСЛЛСВ']
        self.lslssn = dataframe['ЛСЛССН']
        self.lslssv = dataframe['ЛСЛССВ']
        self.lslvsn = dataframe['ЛСЛВСН']
        self.lslvsv = dataframe['ЛСЛВСВ']
        self.lslhn = dataframe['ЛСЛГН']
        self.lslhv = dataframe['ЛСЛГВ']
        return lslpn,lslpv,lslzpn,lslzpv,lslsn,lslsv,lsllsn,lsllsv,lslssn,lslssv,lslvsn,lslvsv,lslhn,lslhv


    def _XP_Forest_Steppe_Dark_Gray_Podzolized_Soils(self,dataframe,ltsopn,ltsopv,ltsozpn,ltsozpv,ltsosn,ltsosv,ltsolsn,ltsolsv,ltsossn,ltsossv,ltsovsn,ltsovsv,ltsohn,ltsohv):
        '''The value of soil indicators Forest Steppe zone - dark gray podzolized soils:
        ltsopn - sandy soils(lower limit)
        ltsopv - sandy soils(upper limit)
        ltsopn - bind-sandy soils(lower limit)
        ltsopv - bind-sandy soils(upper limit)
        ltsosn - sandy loam sand(lower limit)
        ltsosv - sandy loam sand(upper limit)
        ltsolsn - loam sand soils(lower limit)
        ltsolsv - loam sand soils(upper limit)
        ltsossn - sandy clay loam soils(lower limit)
        ltsossv - sandy clay loam soils(upper limit)
        ltsovsn -  silty clay loam soils(lower limit)
        ltsovsv - silty clay loam soils(upper limit)
        ltsohn - clay soils(lower limit)
        ltsohv - clay soils(upper limit)
        '''

        self.ltsopn = dataframe['ЛТСОПН']
        self.ltsopv = dataframe['ЛТСОПВ']
        self.ltsopn = dataframe['ЛТСОЗПН']
        self.ltsozpv = dataframe['ЛТСОЗПВ']
        self.ltsosn = dataframe['ЛТСОСН']
        self.ltsosv = dataframe['ЛТСОСВ']
        self.ltsolsn = dataframe['ЛТСОЛСН']
        self.ltsolsv = dataframe['ЛТСОЛСВ']
        self.ltsossn = dataframe['ЛТСОССН']
        self.ltsossv = dataframe['ЛТСОССВ']
        self.ltsovsn = dataframe['ЛТСОВСН']
        self.ltsovsv = dataframe['ЛТСОВСВ']
        self.ltsohn = dataframe['ЛТСОГН']
        self.ltsohv = dataframe['ЛТСОГВ']
        return ltsopn,ltsopv,ltsozpn,ltsozpv,ltsosn,ltsosv,ltsolsn,ltsolsv,ltsossn,ltsossv,ltsovsn,ltsovsv,ltsohn,ltsohv


    def _XP_Forest_Steppe_Сhernozems_Podzolized_Soils(self,dataframe,lchopn,lchopv,lchozpn,lchozpv,lchosn,lchosv,lcholsn,lcholsv,lchossn,lchossv,lchovsn,lchovsv,lchohn,lchohv):
        '''The value of soil indicators Forest Steppe zone - chernozems podzolized soils:
        lchopn - sandy soils(lower limit)
        lchopv - sandy soils(upper limit)
        lchozpn - bind-sandy soils(lower limit)
        lchozpv - bind-sandy soils(upper limit)
        lchosn - sandy loam sand(lower limit)
        lchosv - sandy loam sand(upper limit)
        lcholsn - loam sand soils(lower limit)
        lcholsv - loam sand soils(upper limit)
        lchossn - sandy clay loam soils(lower limit)
        lchossv - sandy clay loam soils(upper limit)
        lchovsn -  silty clay loam soils(lower limit)
        lchovsv - silty clay loam soils(upper limit)
        lchohn - clay soils(lower limit)
        lchohv - clay soils(upper limit)
        '''

        self.lchopn = dataframe['ЛЧОПН']
        self.lchopv = dataframe['ЛЧОПВ']
        self.lchozpn = dataframe['ЛЧОЗПН']
        self.lchozpv = dataframe['ЛЧОЗПВ']
        self.lchosn = dataframe['ЛЧОСН']
        self.lchosv = dataframe['ЛЧОСВ']
        self.lcholsn = dataframe['ЛЧОЛСН']
        self.lcholsv = dataframe['ЛЧОЛСВ']
        self.lchossn = dataframe['ЛЧОССН']
        self.lchossv = dataframe['ЛЧОССВ']
        self.lchovsn = dataframe['ЛЧОВСН']
        self.lchovsv = dataframe['ЛЧОВСВ']
        self.lchohn = dataframe['ЛЧОГН']
        self.lchohv = dataframe['ЛЧОГВ']
        return lchopn,lchopv,lchozpn,lchozpv,lchosn,lchosv,lcholsn,lcholsv,lchossn,lchossv,lchovsn,lchovsv,lchohn,lchohv


    def _XP_Forest_Steppe_Сhernozems_Typical_Soils(self,dataframe,lchtpn,lchtpv,lchtzpn,lchtzpv,lchtsn,lchtsv,lchtlsn,lchtlsv,lchtssn,lchtssv,lchtvsn,lchtvsv,lchthn,lchthv):
        '''The value of soil indicators Forest Steppe zone - chernozems typical soils:
         lchtpn - sandy soils(lower limit)
         lchtpv - sandy soils(upper limit)
         lchtzpn - bind-sandy soils(lower limit)
         lchtzpv - bind-sandy soils(upper limit)
         lchtsn - sandy loam sand(lower limit)
         lchtsv - sandy loam sand(upper limit)
         lchtlsn - loam sand soils(lower limit)
         lchtlsv - loam sand soils(upper limit)
         lchtssn - sandy clay loam soils(lower limit)
         lchtssv - sandy clay loam soils(upper limit)
         lchtvsn -  silty clay loam soils(lower limit)
         lchtvsv - silty clay loam soils(upper limit)
         lchthn - clay soils(lower limit)
         lchthv - clay soils(upper limit)
        '''

        self.lchtpn = dataframe['ЛЧТПН']
        self.lchtpv = dataframe['ЛЧТПВ']
        self.lchtzpn = dataframe['ЛЧТЗПН']
        self.lchtzpv = dataframe['ЛЧТЗПВ']
        self.lchtsn = dataframe['ЛЧТСН']
        self.lchtsv = dataframe['ЛЧТСВ']
        self.lchtlsn = dataframe['ЛЧТЛСН']
        self.lchtlsv = dataframe['ЛЧТЛСВ']
        self.lchtssn = dataframe['ЛЧТССН']
        self.lchtssv = dataframe['ЛЧТССВ']
        self.lchtvsn = dataframe['ЛЧТВСН']
        self.lchtvsv = dataframe['ЛЧТВСВ']
        self.lchthn = dataframe['ЛЧТГН']
        self.lchthv = dataframe['ЛЧТГВ']
        return lchtpn,lchtpv,lchtzpn,lchtzpv,lchtsn,lchtsv,lchtlsn,lchtlsv,lchtssn,lchtssv,lchtvsn,lchtvsv,lchthn,lchthv
   

    def _XP_Steppe_Сhernozems_Ordinary_Soils(self,dataframe,schzpn,schzpv,schzzpn,schzzpv,schzsn,schzsv,chzlsn,schzlsv,schzssn,schzssv,schzvsn,schzvsv,schzhn,schzhv):
        '''The value of soil indicators Steppe zone - chernozems ordinary soils:
         schzpn - sandy soils(lower limit)
         schzpv - sandy soils(upper limit)
         schzzpn - bind-sandy soils(lower limit)
         schzzpv - bind-sandy soils(upper limit)
         schzsn - sandy loam sand(lower limit)
         schzsv - sandy loam sand(upper limit)
         schzlsn - loam sand soils(lower limit)
         schzlsv - loam sand soils(upper limit)
         schzssn - sandy clay loam soils(lower limit)
         schzssv - sandy clay loam soils(upper limit)
         schzvsn -  silty clay loam soils(lower limit)
         schzvsv - silty clay loam soils(upper limit)
         schzhn - clay soils(lower limit)
         schzhv - clay soils(upper limit)
        '''

        self.schzpn = dataframe['СЧЗПН']
        self.schzpv = dataframe['СЧЗПВ']
        self.schzzpn = dataframe['СЧЗЗПН']
        self.schzzpv = dataframe['СЧЗЗПВ']
        self.schzsn = dataframe['СЧЗСН']
        self.schzsv = dataframe['СЧЗСВ']
        self.schzlsn = dataframe['СЧЗЛСН']
        self.schzlsv = dataframe['СЧЗЛСВ']
        self.schzssn = dataframe['СЧЗССН']
        self.schzssv = dataframe['СЧЗССВ']
        self.schzvsn = dataframe['СЧЗВСН']
        self.schzvsv = dataframe['СЧЗВСВ']
        self.schzhn = dataframe['СЧЗГН']
        self.schzhv = dataframe['СЧЗГВ']
        return schzpn,schzpv,schzzpn,schzzpv,schzsn,schzsv,chzlsn,schzlsv,schzssn,schzssv,schzvsn,schzvsv,schzhn,schzhv


    def _XP_Steppe_Сhernozems_Southern_Soils(self,dataframe,schppn,schppv,schpzpn,schpzpv,schpsn,schpsv,schplsn,schplsv,schpssn,schpssv,schpvsn,schpvsv,schphn,schphv):
        '''The value of soil indicators Steppe zone - chernozems southern soils:
        schppn - sandy soils(lower limit)
        schppv - sandy soils(upper limit)
        schpzpn - bind-sandy soils(lower limit)
        schpzpv - bind-sandy soils(upper limit)
        schpsn - sandy loam sand(lower limit)
        schpsv - sandy loam sand(upper limit)
        schplsn - loam sand soils(lower limit)
        schplsv - loam sand soils(upper limit)
        schpssn - sandy clay loam soils(lower limit)
        schpssv - sandy clay loam soils(upper limit)
        schpvsn -  silty clay loam soils(lower limit)
        schpvsv - silty clay loam soils(upper limit)
        schphn - clay soils(lower limit)
        schphv - clay soils(upper limit)
        '''

        self.schppn = dataframe['СЧППН']
        self.schppv = dataframe['СЧППВ']
        self.schpzpn = dataframe['СЧПЗПН']
        self.schpzpv = dataframe['СЧПЗПВ']
        self.schpsn = dataframe['СЧПСН']
        self.schpsv = dataframe['СЧПСВ']
        self.schplsn = dataframe['СЧПЛСН']
        self.schplsv = dataframe['СЧПЛСВ']
        self.schpssn = dataframe['СЧПССН']
        self.schpssv = dataframe['СЧПССВ']
        self.schpvsn = dataframe['СЧПВСН']
        self.schpvsv = dataframe['СЧПВСВ']
        self.schphn = dataframe['СЧПГН']
        self.schphv = dataframe['СЧПГВ']
        return schppn,schppv,schpzpn,schpzpv,schpsn,schpsv,schplsn,schplsv,schpssn,schpssv,schpvsn,schpvsv,schphn,schphv


    def _XP_Dry_Steppe_Chestnut_Soils(self,dataframe,sskpn,sskpv,sskzpn,sskzpv,ssksn,ssksv,ssklsn,ssklsv,sskssn,sskssv,sskvsn,sskvsv,sskhn,sskhv):
        '''The value of soil indicators Dry Steppe zone - chestnut soils:
        sskpn - sandy soils(lower limit)
        sskpv - sandy soils(upper limit)
        sskzpn - bind-sandy soils(lower limit)
        sskzpv - bind-sandy soils(upper limit)
        ssksn - sandy loam sand(lower limit)
        ssksv - sandy loam sand(upper limit)
        ssklsn - loam sand soils(lower limit)
        ssklsv - loam sand soils(upper limit)
        sskssn - sandy clay loam soils(lower limit)
        sskssv - sandy clay loam soils(upper limit)
        sskvsn -  silty clay loam soils(lower limit)
        sskvsv - silty clay loam soils(upper limit)
        sskhn - clay soils(lower limit)
        sskhv - clay soils(upper limit)
        '''

        self.sskpn = dataframe['ССКПН']
        self.sskpv = dataframe['ССКПВ']
        self.sskzpn = dataframe['ССКЗПН']
        self.sskzpv = dataframe['ССКЗПВ']
        self.ssksn = dataframe['ССКСН']
        self.ssksv = dataframe['ССКСВ']
        self.ssklsn = dataframe['ССКЛСН']
        self.ssklsv = dataframe['ССКЛСВ']
        self.sskssn = dataframe['ССКССН']
        self.sskssv = dataframe['ССКССВ']
        self.sskvsn = dataframe['ССКВСН']
        self.sskvsv = dataframe['ССКВСВ']
        self.sskhn = dataframe['ССКГН']
        self.sskhv = dataframe['ССКГВ']
        return sskpn,sskpv,sskzpn,sskzpv,ssksn,ssksv,ssklsn,ssklsv,sskssn,sskssv,sskvsn,sskvsv,sskhn,sskhv
     
    
    def _XP_Dry_Steppe_Dark_Chestnut_Soils(self,dataframe,sstkpn,sstkpv,sstkzpn,sstkzpv,sstksn,sstksv,sstklsn,sstklsv,sstkssn,sstkssv,sstkvsn,sstkvsv,sstkhn,sstkhv):
        '''The value of soil indicators Dry Steppe zone - dark chestnut soils:
        sstkpn - sandy soils(lower limit)
        sstkpv - sandy soils(upper limit)
        sstkzpn - bind-sandy soils(lower limit)
        sstkzpv - bind-sandy soils(upper limit)
        sstksn - sandy loam sand(lower limit)
        sstksv - sandy loam sand(upper limit)
        sstklsn - loam sand soils(lower limit)
        sstklsv - loam sand soils(upper limit)
        sstkssn - sandy clay loam soils(lower limit)
        sstkssv - sandy clay loam soils(upper limit)
        sstkvsn -  silty clay loam soils(lower limit)
        sstkvsv - silty clay loam soils(upper limit)
        sstkhn - clay soils(lower limit)
        sstkhv - clay soils(upper limit)
        '''

        self.sstkpn = dataframe['ССТКПН']
        self.sstkpv = dataframe['ССТКПВ']
        self.sstkzpn = dataframe['ССТКЗПН']
        self.sstkzpv = dataframe['ССТКЗПВ']
        self.sstksn = dataframe['ССТКСН']
        self.sstksv = dataframe['ССТКСВ']
        self.sstklsn = dataframe['ССТКЛСН']
        self.sstklsv = dataframe['ССТКЛСВ']
        self.sstkssn = dataframe['ССТКССН']
        self.sstkssv = dataframe['ССТКССВ']
        self.sstkvsn = dataframe['ССТКССН']
        self.sstkvsv = dataframe['ССТКВСВ']
        self.sstkhn = dataframe['ССТКГН']
        self.sstkhv = dataframe['ССТКГВ']
        return self.sstkpn,self.sstkpv,self.sstkzpn,self.sstkzpv,self.sstksn,self.sstksv,self.sstklsn,self.sstklsv,self.sstkssn,self.sstkssv,self.sstkvsn,self.sstkvsv,self.sstkhn,self.sstkhv


    def YP(self,nf,nl,ns,nd,kf,kwt,kl,ks,kd,ki,kh,kw,yb,yop,kpg,xpg,lpg,mpg,kpw,xpw,lpw,mpw,kpd,xpd,lpd,mpd,kph,xph,lph,mph,kpk,xpk,lpk,mpk,kpp,xpp,lpp,mpp):
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
        kf = lambda x: self._Parcing_data['ukf'] if x=='upper limit' else self._Parcing_data['lkf']
        kwt = lambda x: self._Parcing_data['ukw'] if x=='upper limit' else self._Parcing_data['lkw']
        kl = lambda x: self._Parcing_data['ukl'] if x=='upper limit' else self._Parcing_data['lkl']
        ks = lambda x: self._Parcing_data['uks'] if x=='upper limit' else self._Parcing_data['lks']
        kd = lambda x: self._Parcing_data['ukd'] if x=='upper limit' else self._Parcing_data['lkd']
        ki = lambda x: self._Parcing_data['uki'] if x=='upper limit' else self._Parcing_data['lki']
        kh = lambda x: self._Parcing_data['ukh'] if x=='upper limit' else self._Parcing_data['lkh']
        kw = lambda x: self._Parcing_data['ukw'] if x=='upper limit' else self._Parcing_data['lkw']

        if xp == 'ПДОПН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdopn)
        elif xp=='ПДОПВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdopv)
        elif xp=='ПДОЗПН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdozpn) 
        elif xp=='ПДОПВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdozpv) 
        elif xp=='ПДОСН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdosn) 
        elif xp=='ПДОСВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdosv) 
        elif xp=='ПДОЛСН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdolsn) 
        elif xp=='ПДОЛСВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdolsv)  
        elif xp=='ПДОССН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdossn) 
        elif xp=='ПДОССВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdossv) 
        elif xp=='ПДОВСН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdovsn) 
        elif xp=='ПДОВСВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdovsv)  
        elif xp=='ПДОГН':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdohn) 
        elif xp=='ПДОГВ':
            xp=self._XP_Polissya_Sod_Podzolized_Soils(dataframe,pdohv)  
       
        yp = (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kpg * ((xpg - lpg) ** 2))) / (1 + (100 - yopg) * np.exp(-mpg * (xp - lpg))) + (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kpw * ((xpw - lpw) ** 2))) / (1 + (100 - yopw) * np.exp(-mpw * (xpw - lpw))) + (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kpd * ((xpd - lpd) ** 2))) / (1 + (100 - yop) * np.exp(-mpd * (xpd - lpd))) + (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kph * ((xph - lph) ** 2))) / (1 + (100 - yoph) * np.exp(-mph * (xph - lph))) + (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kpk * ((xpk - lpk) ** 2))) / (1 + (100 - yopk) * np.exp(-mpk * (xpk - lpk))) + (nf * nl * ns * nd * kf * kwt * ks * kl * kd * ki * kh * kw * yb * yop * np.exp(-kpp * ((xpp - lpp) ** 2))) / (1 + (100 - yopp) * np.exp(-mpp * (xpp - lpp)))
        return yp


  

        

      
