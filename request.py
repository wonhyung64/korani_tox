#%%
import requests


#%%
url = "https://ecolife.me.go.kr/openapi/ServiceSvl"
url = "https://ecolife.me.go.kr"

response = requests.get(url)
response.status_code

param = {
    "ServiceName" : "chmstryProductList",
    "AuthKey" : "335E75X9K7O9PCIVFO5JP77551QG15X1",
    "prdtarmCd" : "01",
    }
response = requests.post(url, json=param)

response.text


#%%
#%%
import yaml
import requests
import xml.etree.ElementTree as ET
import pandas as pd


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

cfg_path = "./config.yaml"
cfg_url = load_config(cfg_path)['URL']
cfg_ch7 = load_config(cfg_path)['Ch7']
cfg_ch3 = load_config(cfg_path)['Ch3']

headers = {  # for XML format
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    # "Cache-Control": "no-cache",  # 캐시 방지
    # "Pragma": "no-cache"
}

params = {**cfg_ch3['init_index']}

response = requests.get(url=cfg_url, params=params, headers=headers)
root = ET.fromstring(response.content)

total_count = int(root.find('.//count').text)  # 총 결과 수 추출
page_size = params.get('PageCount', 20)  # PageCount가 없으면 기본 20으로 설정, Max가 20개.
total_pages = (total_count // page_size) + (1 if total_count % page_size > 0 else 0)

product_data = []

for page in range(1, total_pages + 1):
    print(f"Processing Page {page}/{total_pages}...")

    params['PageNum'] = page  # 페이지 번호 업데이트
    response = requests.get(url=cfg_url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data on page {page}")
        continue

    root = ET.fromstring(response.content)

    items = root.findall('.//row')  # 'row' 태그에서 각 제품 정보를 찾음
    if not items:
        print(f"No data found on page {page}")
        continue

    for item in items:
        product_data.append({
            '제품마스터번호': item.find('prdt_mstr_no').text if item.find('prdt_mstr_no') is not None else 'N/A',
            '제품군코드': item.find('prdtarm_cd').text if item.find('prdtarm_cd') is not None else 'N/A',
            '제품명(국문)': item.find('prdtnm_kor').text if item.find('prdtnm_kor') is not None else 'N/A',
            '제품분류명': item.find('prdtarm').text if item.find('prdtarm') is not None else 'N/A',
            '종류': item.find('knd').text if item.find('knd') is not None else 'N/A',
            # '바코드정보': item.find('barcd_info').text if item.find('barcd_info') is not None else 'N/A',
            # '안전인증번호': item.find('slfsfcfst_no').text if item.find('slfsfcfst_no') is not None else 'N/A'
        })

df = pd.DataFrame(product_data)

csv_file_path = "/root/default/DS_PLUS/data/product_data.csv"
df.to_csv(csv_file_path, index=False)


#%%
