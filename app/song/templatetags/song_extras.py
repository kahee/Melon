from django import template

register = template.Library()


@register.filter(name='ellipsis_line')
def ellipsis_line(value, arg):
    # value로부터
    # arg에 주어진 line 수만큼 문자열(line) 반환

    # 주어진 multi-line string을 리스트로 분할
    lines = value.splitlines()

    # 리스트 길이가 주어진 arg(line수)보다 길경우
    if len(lines) > arg:
        # 줄바꿈 문자 단위로
        # multi-line string을 분할한 리스트를
        # arg(line수)개수까지 슬라이싱한 결과를 합침
        # 마지막 요소에는 '...'을 추가
        return '\n'.join(lines[:arg]+['...'])

    return value

