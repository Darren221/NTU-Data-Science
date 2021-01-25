######################## googlemaps #########################
# https://github.com/googlemaps/google-maps-services-python #
# Install:                                                  #
# $ pip3 install -U googlemaps                              #
#############################################################
import sys, json, pandas, googlemaps
from time import sleep

df = pandas.read_csv('全國4大超商資料集.csv',encoding = 'utf-8')
df['分公司地址'] = df['分公司地址'].str.replace('巿','市').replace('台北市','臺北市').replace('臺北縣','新北市').replace('台北縣','新北市').replace('桃園縣','桃園市').replace('臺中縣','臺中市').replace('臺南縣','臺南市').replace('高雄縣','高雄市').replace('苗栗市','苗栗縣').replace('彰化市','彰化縣').replace('臺','台')

df['lng'] = 0.0
df['lat'] = 0.0
gmaps = googlemaps.Client(key='AIzaSyDG_xzhPo7GPwxue1e6hlnTo4K1qekLK6Y')

for i in range(df.shape[0]):
    temp = str(df.iloc[i]['分公司地址'])
    temp = temp.replace('０','0').replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9')
    temp = temp.replace('一百','1').replace('二百','2').replace('三百','3').replace('四百','4').replace('五百','5').replace('六百','6').replace('七百','7').replace('八百','8').replace('九百','9')
    temp = temp.replace('一十','1').replace('二十','2').replace('三十','3').replace('四十','4').replace('五十','5').replace('六十','6').replace('七十','7').replace('八十','8').replace('九十','9')
    temp = temp.replace('零','0').replace('一','1').replace('二','2').replace('三','3').replace('四','4').replace('五','5').replace('六','6').replace('七','7').replace('八','8').replace('九','9')
    temp = temp.replace('1樓','').replace('地下1層','').replace('地下2層','').replace('地下3層','').replace('地下第1層','').replace('地下第2層','').replace('地下第3層','').replace('地下室','')
    df.iloc[i, df.columns.get_loc('分公司地址')] = temp
    
    sleep(0.05)
    geocode_result = gmaps.geocode(temp)
    if len(geocode_result) > 0:
        # longitude
        df.iloc[i, df.columns.get_loc('lng')] = geocode_result[0]['geometry']['location']['lng']
        # latitude
        df.iloc[i, df.columns.get_loc('lat')] = geocode_result[0]['geometry']['location']['lat']
        print(df.iloc[i]['分公司地址'][:3], end=',')
        print(df.iloc[i]['lng'], end=',')
        print(df.iloc[i]['lat'])
    else:
        print('ERROR!!!!!:', i)
    if i % 20 == 1:
        sys.stdout.flush()

df.to_csv('./addr.csv', index=False)
