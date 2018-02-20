def get_detail(self, artist_id, refresh_html=False):
    file_path = os.path.join(DATA_DIR, f'artist_detail_{artist_id}.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            # 아티스트 목록 가져오는 html
            url = 'https://www.melon.com/artist/detail.htm'
            params = {
                'artistId': artist_id
            }
            response = requests.get(url, params)
            source = response.text
            f.write(source)
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')

        source = open(file_path, 'rt').read()
        soup = BeautifulSoup(source, 'lxml')

        # 기본 정보 _info
        wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
        url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')
        name_div = wrap_dtl_atist.select_one('p.title_atist').text[5:]
        name = re.search(r'(\w+)\s', name_div).group(1)
        real_name = re.search(r'\((\w+)\)', name_div).group(1)

        debut = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(1)').get_text(strip=True)[:10]
        birthday = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(2)').get_text(strip=True)
        artist_type = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(3)').get_text(strip=True)
        agency = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(4)').get_text(strip=True)
        award = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(5)').get_text(strip=True)
        self.artist_id = artist_id
        self.name = name
        self.real_name = real_name

        result = {'데뷔': debut,
                  '생일': birthday,
                  '활동유형': artist_type,
                  '소속사': agency,
                  '수상이력': award,
                  '이미지': url_img_cover
                  }

        self._info = result

        # _award_history
        list_define = soup.find('dl', class_="list_define").find_all("dd")
        for i in list_define:
            # 수상 (수상내역) 형식으로 변경
            award_detail = re.search(r'(.*?)\|(.*)', i.text)
            self._award_history.append(f'{award_detail.group(1)} ({award_detail.group(2)})')

        # _introduction
        div_artist_intro = soup.find('div', id="d_artist_intro")
        introduction_list = list()
        for i in div_artist_intro:
            if i.name == 'br':
                introduction_list.append('\n')
            elif type(i) is NavigableString:
                introduction_list.append(i.strip())

        introduction = ''.join(introduction_list)
        self._introduction = introduction

        # _activity_information
        dl_list_define = soup.find('div', class_="section_atistinfo03").find('dl', class_='list_define')

        activity_list = list()
        for index, i in enumerate(dl_list_define.find_all("dd")):
            activity_list.append(i.get_text(strip=True))

        activity_information = {
            "데뷔": activity_list[0],
            "활동년대": activity_list[1],
            "유형": activity_list[2],
            "장르": activity_list[3],
            "소속사명": activity_list[4],
            "소속그룹": activity_list[5]
        }
        self._activity_information = activity_information

        # _personal_information
        dl_list_define = soup.find('div', class_="section_atistinfo04").find('dl', class_='list_define')

        personal_list = list()
        for index, i in enumerate(dl_list_define.find_all("dd")):
            personal_list.append(i.get_text(strip=True))

        personal_information = {
            "본명": personal_list[0],
            "별명": personal_list[1],
            "국적": personal_list[2],
            "생일": personal_list[3],
            "별자리": personal_list[4],
            "혈액형": personal_list[5]
        }
        self._personal_information = personal_information

        # _related_information
        dl_list_define = soup.find('div', class_="section_atistinfo05")
        # sns
        buttons = dl_list_define.find_all('button', type="button")

        sns_address = list()
        for i in buttons:
            address = re.search(r".*\('(.*?)?'", i.get('onclick'))
            sns_address.append(address.group(1))

        related_information = {
            "SNS": f'트위터 ({sns_address[0]}), 페이스북 ({sns_address[1]})'
        }

        # 그외 계정들
        dd_find = dl_list_define.find('dl', class_="list_define").find_all("dd")
        other_address = list()
        for i in dd_find:
            other_address.append(i.text)
        related_information["YouTube"] = other_address[0]
        related_information["팬카페"] = other_address[1]

        self._related_information = related_information