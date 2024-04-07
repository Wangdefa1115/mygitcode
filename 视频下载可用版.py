import time

import m3u8
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

url = 'https://testvod-xinyi.21tb.com/0c1e0490bbd771ed90990764a0fd0102/8be61bf973b805122ec7f94871ad71f3-ld-encrypt-stream.m3u8?MtsHlsUriToken=TXRzSGxzVXJpVG9rZW5fY3FybF82MDkyYmY4N2E0ZTc0MTQwYWQ5ZTA3MGQzZTc2ZTIxNQ=='

save_name= r'205数据清洗案例3-多维度合并查询.mp4'

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
}
    

# def get_real_url(url):
#     playlist = m3u8.load(uri=url, headers=headers)
    
#     return playlist.playlists[0].absolute_uri


def AESDecrypt(cipher_text, key, iv):
    '''AES解密'''
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def download_m3u8_video(url, save_name):
    # real_url = get_real_url(url)#获取m3u8的地址
    playlist = m3u8.load(uri=url, headers=headers)
    key = requests.get(playlist.keys[-1].uri, headers=headers).content

    n = len(playlist.segments)
    size = 0
    start = time.time()
    for i, seg in enumerate(playlist.segments, 1):
        r = requests.get(seg.absolute_uri, headers=headers)
        data = r.content
        data = AESDecrypt(data, key=key, iv=key)
        size += len(data)
        with open(save_name, "ab" if i != 1 else "wb") as f:
            f.write(data)
        print(
            f"\r下载进度({i}/{n})，已下载：{size/1024/1024:.2f}MB，下载已耗时：{time.time()-start:.2f}s", end=" ")


download_m3u8_video(url, save_name)