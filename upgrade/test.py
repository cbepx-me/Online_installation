import os
import time
import requests


source = "source/"

retry_config = {
    'total': 3,
    'backoff_factor': 0.5,
    'status_forcelist': [500, 502, 503, 504],
    'allowed_methods': ['GET', 'HEAD']
}

mirrors = [
    {
        "name": "localhost",
        "url": "http://127.0.0.1/source/update_info.json",
        "region": "local"
    },
    {
        "name": "GitHub",
        "url": "https://github.com/cbepx-me/Online_installation/blob/main/software_list.json",
        "region": "Global"
    },
    {
        "name": "GitCode (China)",
        "url": "https://gitcode.com/cbepx/install/blob/main/software_list.json",
        "region": "CN"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}

if os.name != "nt":
    mirrors.pop(0)
fallback_mirror = mirrors[0]
speeds = []
for mirror in mirrors:
    try:
        start = time.time()
        response = requests.get(mirror["url"], timeout=3, headers=headers, stream=True)
        response.close()
        end = time.time() - start
        if response.status_code == 404:
            print(f"Mirror {mirror['name']} accessible but file update_info.json not found (404)")
            end = float('inf')
        elif response.status_code != 200:
            print(f"Mirror {mirror['name']} returned error code: {response.status_code}")
            end = float('inf')
    except:
        end = float('inf')
    speeds.append((end, mirror))
speeds.sort(key=lambda x: x[0])
info_url = speeds[0][1]["url"] if speeds[0][0] != float('inf') else fallback_mirror["url"]
server_url = info_url[:-23] + source
info_url = server_url + "update_info.json"
print(f"Use the downloaded server: {server_url}")