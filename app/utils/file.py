import magic
from pathlib import Path

from io import BytesIO

import requests


def download(url):
    # 이미지 넣는 코드부분
    # 그림파일형태의 이미지 가져옴
    response = requests.get(url)
    binary_data = response.content
    temp_file = BytesIO()
    temp_file.write(binary_data)
    temp_file.seek(0)

    return temp_file


def get_buffer_ext(buffer):
    buffer.seek(0)
    mime_info = magic.from_buffer(buffer.read(),mime=True)
    return mime_info.split('/')[-1]