import re
import requests

from bs4 import BeautifulSoup, NavigableString


__all__ = (
    'song_list_crawler',
    'song_detail_crawler',
)


def song_list_crawler(keyword):
    from song.models import Song
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
        if tr.select_one('td:nth-of-type(3) a.fc_gray'):
            if tr.select_one('td:nth-of-type(3) a.fc_gray'):
                title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            else:
                title = tr.select_one('td:nth-of-type(3) > div > div > span').get_text(strip=True)

        artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
            strip=True)
        album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

        result.append(
            {'song_id': song_id,
             'title': title,
             'artist': artist,
             'album': album,
             'is_exist': Song.objects.filter(song_id=song_id).exists(),
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

    # 앨범, 발매일, 장르...에 대한 Description list
    dl = div_entry.find('div', class_='meta').find('dl')

    # isinstance(인스턴스, 클래스(타입))
    # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))

    div_lyrics = soup.find('div', id='d_video_summary')

    # 가사가 없는 경우 분기
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

    p = re.compile(r'javascript:melon.link.goAlbumDetail[(]\'(\d+)\'[)]')
    first_dd = dl.find('dd')
    album_id = p.search(str(first_dd)).group(1)

    artist_href = div_entry.find('a', class_='artist_name').get('href')
    p = re.compile(r'javascript:melon.link.goArtistDetail[(]\'(\d+)\'[)]')
    artist_id = p.search(str(artist_href)).group(1)
    result_dict = dict()
    result_dict['title'] = title
    result_dict['genre'] = genre
    result_dict['lyrics'] = lyrics
    result_dict['album_id'] = album_id
    result_dict['artist_id'] = artist_id

    return result_dict
