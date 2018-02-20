import re

import requests
from bs4 import BeautifulSoup, NavigableString


def get_detail(artist_id):
    url = 'https://www.melon.com/artist/detail.htm'
    params = {
        'artistId': artist_id
    }
    response = requests.get(url, params)
    print(response.url)

    soup = BeautifulSoup(response.text, 'lxml')

    # award_history
    div_section_atistinfo01 = soup.find('div', class_="section_atistinfo01")
    if not div_section_atistinfo01 == None:
        dl = div_section_atistinfo01.find('dl', class_='list_define')
        award_history = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]


    # _introduction = {}
    div_section_atistinfo02 = soup.find('div', class_="section_atistinfo02")
    if not div_section_atistinfo02 == None:
        div = div_section_atistinfo02.find('div', id='d_artist_intro')
        introduction_list = list()
        for i in div:
            if i.name == 'br':
                introduction_list.append('\n')
            elif type(i) is NavigableString:
                introduction_list.append(i.strip())

        introduction = ''.join(introduction_list)
        print(introduction)

    # _activity_information = {}
    div_section_atistinfo03 = soup.find('div', class_="section_atistinfo03")
    if not div_section_atistinfo03 == None:
        dl = div_section_atistinfo03.find('dl', class_='list_define')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        '''
        iterable은 멤버를 하나씩 반환 할 수 있는 object 를 의미한다. 
        '''
        # 나중에 info 에 여기있는 정보를 넣어주면 될꺼같다
        it = iter(items)
        activity_information = dict(zip(it, it))
        print(activity_information)

    # _personal_information
    div_section_atistinfo04 = soup.find('div', class_="section_atistinfo04")
    if not div_section_atistinfo04 == None:
        dl = div_section_atistinfo04.find('dl', class_='list_define')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        li = iter(items)
        personal_information = dict(zip(li, li))
        print(personal_information)

    # _related_information
    div_section_atistinfo05 = soup.find('div', class_="section_atistinfo05")

    if not div_section_atistinfo05 == None:
        button_sns = div_section_atistinfo05.find_all('button')
        address = [re.search(r".*\('(.*?)?'", item.get('onclick')).group(1) for item in button_sns]
        sns_name = [item.get_text() for item in button_sns]
        related_information_first = dict(zip(sns_name, address))
        dl = div_section_atistinfo05.find('dl', class_='list_define')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        it = iter(items)
        # 딕셔너리두개를 한개로 병합  Unpacking Generalizations
        related_information_second = dict(zip(it, it))
        related_information = {**related_information_first, **related_information_second}
        print(related_information)

    # 기본 info 이미지, 이름, 본명
    wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
    url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')

    # 이미지가 없을 경우에는 url 주소가 없는 것처럼
    if url_img_cover == "http://cdnimg.melon.co.kr":
        url_img_cover = ""
    name_div = wrap_dtl_atist.select_one('p.title_atist').text[5:]
    name = re.search(r'(\w+)\s', name_div).group(1)
    real_name = re.search(r'\((\w+)\)', name_div).group(1)

    print(url_img_cover)
    print(name)
    print(real_name)
    print(artist_id)


if __name__ == '__main__':
    webtoon = get_detail(560205)
