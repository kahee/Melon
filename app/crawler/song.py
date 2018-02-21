import requests

from bs4 import BeautifulSoup, NavigableString

def song_list_crawler(keyword):
    url = 'https://www.melon.com/search/song/index.htm'
    params = {
        'q': keyword,
        'section': 'song',
    }
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')
    tr_list = soup.select('form#frm_defaultList table > tbody > tr')

    result = []
    for tr in tr_list:
        song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
        title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
        artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
            strip=True)
        album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

        result.append(
            {'song_id': song_id,
             'title': title,
             'artist': artist,
             'album': album,
             }
        )

    return result


def song_detail_crawler(song_id):
    url = f'https://www.melon.com/song/detail.htm'
    params = {
        'songId': song_id,
    }
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    div_entry = soup.find('div', class_='entry')
    title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
    artist = div_entry.find('div', class_='artist').get_text(strip=True)

    # 앨범, 발매일, 장르...에 대한 Description list
    dl = div_entry.find('div', class_='meta').find('dl')

    # isinstance(인스턴스, 클래스(타입))
    # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))

    div_lyrics = soup.find('div', id='d_video_summary')

    if div_lyrics:
        lyrics_list = []
        for item in div_lyrics:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())
        lyrics = ''.join(lyrics_list)

    else:
        lyrics = ''

    genre = description_dict.get('장르')

    result_dict = dict()

    result_dict['title'] = title
    result_dict['genre'] = genre
    result_dict['lyrics'] = lyrics

    return result_dict
