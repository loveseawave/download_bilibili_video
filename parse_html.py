"""这个python文件的目的是通过re正则表达式包解析html"""
import re


def parse_html(html):
    cid = re.findall('"cid":(\\d+),', html)[0]
    session = re.findall('"session":"(.*?)"', html)[0]
    # title = re.findall('<h1 title=".*?" class="video_title"', html)[0].replace(" ", "")
    title = re.findall('<h1 data-title="(.*?)"', html)[0].replace(" ", '')
    return [cid, session, title]
