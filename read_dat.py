#%%
import os
import re
import numpy as np
import pandas as pd
import openpyxl
import glob
from pathlib import Path
class Site:
    def __init__(self,site_name,begin_date):
        self.site_name = site_name
        self.begin_date = begin_date
        self.dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'result')#実行ファイルがあるフォルダの「result」フォルダ
        self.setFilelist()
        self.ny_block = 55#鉛直方向yの最大ブロック数。
        self.setNRows()#行数設定
        self.df = pd.DataFrame()#空のデータフレーム。中身は日付インデックスだけ。
    
    #出力対象のファイル名リストを設定
    def setFilelist(self):
        dat_list = [os.path.basename(dat_file) for dat_file in glob.glob('result\*'+ self.site_name +'*.dat')]
        drop_list = ['dpla','sqp','sqn','spla']#とりあえずいらない項目
        drop_idx = []
        #リストのうち、いらない要素のインデックスの要素を削除する無名関数
        dellist = lambda items,indices: [item for idx,item in enumerate(items) if idx not in indices]

        #必要な計算項目（ファイル名）のみを抽出
        for drp_f in drop_list:
            for dat_f in dat_list:
                if re.search(drp_f,dat_f):
                    drop_idx.append(dat_list.index(dat_f))

        self.file_list = dellist(dat_list,drop_idx)
    
    #計算結果の行数を設定（site_tt.datを利用）
    def setNRows(self):
        file_path = os.path.join(self.dir_path,'site_tt.dat')
        counter = 0
        with open(file_path,'r') as f:
            line = f.readline()
            while line:
                counter += 1
                line = f.readline()
        self.n_rows = counter

    #開始日付からデータ数分の連続時間をデータフレームに追加
    def setDate(self):
        periods = self.n_rows
        self.df['date'] = pd.date_range(self.begin_date,periods = periods,freq='H')  

    #表層ブロックの番号データフレームにセット（site_tt.datを利用）
    def setBlockNum(self):
        temp_list = []
        file_path = os.path.join(self.dir_path,'site_tt.dat')
        with open(file_path,'r') as f:
            line = f.readline()
            while line:#読み込み行が空になったらループ終了
                temp_list.append(line[8:10])#8~10文字目が表層ブロック番号
                line = f.readline()
        temp_arry = np.array([int(value) for value in temp_list])
        col_names = "surface_block"
        self.df[col_names] = temp_arry
    
    #計算結果に対応する水深データをデータフレームにセット（site_tt.datを利用）
    def setDepth(self):
        temp_list = []
        file_path = os.path.join(self.dir_path,'site_tt.dat')
        with open(file_path,'r') as f:
            line = f.readline()
            while line:#読み込み行が空になったらループ終了
                temp_list.append(line[-825:])#後ろから825文字目以降が水深
                line = f.readline()
        temp_arry = self.list_to_2Darry(temp_list,self.n_rows,self.ny_block)#ここで、データセット数×55の配列
        col_names = ["depth_"+str(i) for i in range(1,self.ny_block+1)]#カラム番号のリスト1～55
        temp_df = pd.DataFrame(data = temp_arry,columns = col_names)
        self.df = pd.concat([self.df,temp_df],axis=1)

    #計算結果をデータフレームにセット
    def setData(self,cal_item):
        temp_list = []
        file_path = os.path.join(self.dir_path,cal_item)
        with open(file_path,'r') as f:
            line = f.readline()
            while line:#読み込み行が空になったらループ終了
                temp_list.append(line[26:850])#後ろから825文字目以降が水深
                line = f.readline()
        temp_arry = self.list_to_2Darry(temp_list,self.n_rows,self.ny_block)#ここで、データセット数×55の配列

        #site_tt.datなどのcal_item →　re.sub()で「_」以前と「.dat」を削除
        cal_item = re.sub(r'^.*?_(.*).dat',r'\1',cal_item)
        col_names = [cal_item+'_'+str(i) for i in range(1,self.ny_block+1)]#カラム番号のリスト1～55
        temp_df = pd.DataFrame(data = temp_arry,columns = col_names)
        self.df = pd.concat([self.df,temp_df],axis=1)     
    

    #計算結果と水深を2次元のnd.arrayにする。setDepthとsetDataで使用。
    def list_to_2Darry(self,list_str,rows_arry,cols_arry):
        list_matrix = [str.split() for str in list_str]#空白で区切り、ネストしたリストへ。
        list_float = [float(value) for child_list in list_matrix for value in child_list]
        return np.array(list_float).reshape(rows_arry,cols_arry)


#%%
def main():
    site_list = ['siteA_']#   site_list = ['siteB_','siteC_','siteD_','siteE_']
 
    begin_date = '20181201'
    for site in site_list:
        export_site = Site(site,begin_date)

        export_site.setDate()
        export_site.setBlockNum()
        export_site.setDepth()

        for file_cal in export_site.file_list:
            export_site.setData(file_cal)
            
        save_path = os.path.join(Path(__file__).parent,site +'.xlsx')
        export_site.df.to_excel(save_path,index=False)
#%%
if __name__ == '__main__':
    main()



# %%
