import json
import requests
import pandas    as pd
import geopandas as gpd

from shapely.geometry import Polygon, Point, MultiPolygon



req_prt_1    = 'https://search-maps.yandex.ru/v1/?text='
req_prt_2    = '&type=biz'
req_prt_3    = '&results='
req_prt_4    = '&lang=ru_RU'
req_prt_5    =  '&apikey='

cnst_company = 'SimpleWine'
cnst_res_nmb = str(100)
cnst_api_key = '60fb580e-e9bd-44f6-9575-8f77fae0467e'



request_href = ''.join([ req_prt_1, cnst_company,
                         req_prt_2,
                         req_prt_3, cnst_res_nmb,
                         req_prt_4,
                         req_prt_5, cnst_api_key])

r            = requests.get(request_href)
data         = r.json()

df11 = pd.json_normalize(data['features'])


df11 = df11[['properties.name', 'geometry.type', 'geometry.coordinates', 'properties.description', 'properties.CompanyMetaData.address', 'properties.CompanyMetaData.Hours.text']]
df11[['coordinates_lon', 'coordinates_lat']] = df11['geometry.coordinates'].apply(pd.Series)

df11.to_csv('wineries.csv', index = False, encoding = 'utf-8-sig')


with open('Moscow.geojson', encoding = 'utf-8') as f:
    moscow = json.load(f)

coord_list = []

for objj in moscow['features']:
    objj_list = []

    for obj in objj['geometry']['coordinates'][0][0]:
        objj_list.append(tuple(obj))

    coord_list.append(objj_list)

with open('Moscow.geojson', encoding='utf-8') as f:
    moscow = json.load(f)

df_msk = pd.DataFrame(columns = ['id', 'name', 'poly'])
for i in range(125):
    df_msk.loc[len(df_msk.index)] = [moscow['features'][i]['properties']['cartodb_id'],
                                     moscow['features'][i]['properties']['name'], Polygon(coord_list[i])]
    
df_msk.to_csv('msk_data.csv', index = False, encoding = 'utf-8-sig')
