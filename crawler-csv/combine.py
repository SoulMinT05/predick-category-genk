import pandas as pd
import numpy as np
# /Users/mac/Desktop/CT312_DataMining/BTNhom_Tam/crawler-csv/digitaltoys_selenium.csv

# dochoiso_data = pd.read_csv('/Users/mac/Desktop/CT312_DataMining/BTNhom_Tam/crawler-csv/digitaltoys_selenium.csv')
dochoiso_data = pd.read_csv('crawler-csv/digitaltoys_selenium.csv')
internet_data = pd.read_csv('crawler-csv/internet_selenium.csv')
xemmualuon_data = pd.read_csv('crawler-csv/xemmualuon_selenium.csv')
thuthuat_data = pd.read_csv('crawler-csv/thuthuat_selenium.csv')
appsgame_data = pd.read_csv('crawler-csv/appsgame_selenium.csv')

combined_data = pd.concat([dochoiso_data, internet_data, xemmualuon_data, thuthuat_data, appsgame_data])

# Xuất dữ liệu đã gộp thành file CSV mới
combined_data.to_csv('data_combined_5_not-tinIcgt_test1.csv', index=False)

print("Dữ liệu đã gộp và lưu thành công!")