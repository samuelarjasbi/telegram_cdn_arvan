import requests


def callApi(endpoint = ""):
    url = f'https://napi.arvancloud.ir/cdn/4.0/domains/{endpoint}'
    # url = requests.utils.quote(url)
    headers = {
        'Accept': 'application/json',
        'Authorization': 'apikey 6f87e9ae-b958-51ee-8384-e692bd1fb0bd'
    }
    
    response = requests.get(url, headers=headers)
    return response

# if response.status_code == 200:
#     # for i in response.json()["data"]:
#     #     print(i["domain"])
#     print(response.json())
# else:
#     print(f"Error: {response.status_code} - {response.text}")
    
def bytes_to_gb(bytes):
    gb = bytes / (1024 ** 3)
    return gb
    
def get_servers():
    response = callApi()
    domains=[]
    for i in response.json()["data"]:
        domains.append(i['domain'])
    return domains

def server_status(server_name):
    response = callApi(f"{server_name}/reports/traffics?period=30d")
    return response.json()
    

def server_info(server_name):
    response = callApi(f'{server_name}')
    return response.json()

def point_data(server_name):
    response_info = callApi(f'{server_name}')
    response_status = callApi(f"{server_name}/reports/traffics?period=30d")
    
    info = response_info.json()
    status = response_status.json()
    
    out = f"🌐<b>Domain :</b> {info['data']['domain']} \n🎛️<b>plan level:</b> {info['data']['plan_level']} \n📈<b>Total Used Traffic:</b> {bytes_to_gb(int(status['data']['statistics']['traffics']['total']))}"
    return out
# print(server_info('mrhosting.sbs'))
# print(server_status("somebyte.sbs"))