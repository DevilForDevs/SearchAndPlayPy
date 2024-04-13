import json
import math
import re
import urllib
from urllib import parse
from urllib.request import urlopen


def txt2filename(txt):
    print('Function txt2filename:', txt)
    special_characters = ['@', '#', '$', '*', '&', '<', '>', '/', '\x08',
        '|', '?', 'CON', ' PRN', ' AUX', ' NUL', ' COM0', ' COM1', ' COM2',
        ' COM3', ' COM4', ' COM5', ' COM6', ' COM7', ' COM8', ' COM9',
        ' LPT0', ' LPT1', ' LPT2', ' LPT3', ' LPT4', ' LPT5', ' LPT6',
        ' LPT7', ' LPT8', 'LPT9', ':', '"', "'"]
    normal_string = str(txt)
    for sc in special_characters:
        normal_string = normal_string.replace(sc, '')
    return normal_string


def convert_size(size_bytes):
    print('Function convert_size:', size_bytes)
    if size_bytes == 0:
        return '0B'
    size_name = 'B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])


def seconds_to_dhms_short(total_milliseconds: int) ->str:
    print('Function seconds_to_dhms_short:', total_milliseconds)
    milliseconds = total_milliseconds % 1000
    total_seconds = total_milliseconds // 1000
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    total_hours = total_minutes // 60
    minutes = total_minutes % 60
    days = total_hours // 24
    hours = total_hours % 24
    if days == 0:
        if hours == 0:
            if minutes == 0:
                return f'{seconds}'
            else:
                return f'{minutes}:{seconds}'
        return f'{hours}:{minutes}:{seconds}:'
    else:
        return f'{days}:{hours}:{minutes}:{seconds}'


def seconds_to_dhms(total_seconds: int) ->str:
    print('Function seconds_to_dhms:', total_seconds)
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    total_hours = total_minutes // 60
    minutes = total_minutes % 60
    days = total_hours // 24
    hours = total_hours % 24
    if days == 0:
        if hours == 0:
            if minutes == 0:
                return f'{seconds} s'
            else:
                return f'{minutes} m{seconds} s.'
        return f'{hours} h{minutes} m{seconds}s.'
    else:
        return f'{days} d{hours} h{minutes} m{seconds} s'


def reels_rendere(itp):
    print('Function reels_rendere:', itp)
    reels = itp['reelShelfRenderer']['items']
    vid_list = []
    for kb in reels:
        vid = kb['reelItemRenderer']['videoId']
        title = kb['reelItemRenderer']['headline']['simpleText']
        thumbnail = kb['reelItemRenderer']['thumbnail']['thumbnails'][0]['url']
        vid_list.append({'videoId': vid, 'title': title, 'thumbnail':
            thumbnail, 'duration': 'Shorts'})
    return vid_list


def shel_rendtrer(item):
    print('Function shel_rendtrer:', item)
    itims = []
    subitem = item['shelfRenderer']['content']
    if 'verticalListRenderer' in subitem:
        ivd = subitem['verticalListRenderer']['items']
        for ivids in ivd:
            vide_id = ivids['videoRenderer']['videoId']
            title = ivids['videoRenderer']['title']['runs'][0]['text']
            thumbai = ivids['videoRenderer']['thumbnail']['thumbnails'][0][
                'url']
            dura = 'Unknown'
            if 'lengthText' in ivids:
                dura = ivids['videoRenderer']['lengthText']['simpleText']
            itims.append({'videoId': vide_id, 'title': title, 'thumbnail':
                thumbai, 'duration': dura})
    if 'horizontalListRenderer' in subitem:
        hrzitems = subitem['horizontalListRenderer']['items']
        for v in hrzitems:
            if 'gridVideoRenderer' in v:
                vid = v['gridVideoRenderer']['videoId']
                title = v['gridVideoRenderer']['title']['runs'][0]['text']
                thumbs = v['gridVideoRenderer']['thumbnail']['thumbnails'][0][
                    'url']
                itims.append({'videoId': vid, 'title': title, 'thumbnail':
                    thumbs, 'duration': 'Shorts'})
    return itims


def praser(resp):
    print('Function praser:', resp)
    raw_results = resp
    try:
        sections = raw_results['contents']['twoColumnSearchResultsRenderer'][
            'primaryContents']['sectionListRenderer']['contents']
    except KeyError:
        sections = raw_results['onResponseReceivedCommands'][0][
            'appendContinuationItemsAction']['continuationItems']
    item_renderer = None
    continuation_renderer = None
    for s in sections:
        if 'itemSectionRenderer' in s:
            item_renderer = s['itemSectionRenderer']
        if 'continuationItemRenderer' in s:
            continuation_renderer = s['continuationItemRenderer']
    if continuation_renderer:
        next_continuation = continuation_renderer['continuationEndpoint'][
            'continuationCommand']['token']
    else:
        next_continuation = None
    if item_renderer:
        videos = []
        raw_video_list = item_renderer['contents']
        for video_details in raw_video_list:
            if video_details.get('searchPyvRenderer', {}).get('ads', None):
                continue
            if 'reelShelfRenderer' in video_details:
                reels = reels_rendere(video_details)
                for i in reels:
                    videos.append(i)
            if 'shelfRenderer' in video_details:
                selts = shel_rendtrer(video_details)
                for k in selts:
                    videos.append(k)
            if 'radioRenderer' in video_details:
                continue
            if 'playlistRenderer' in video_details:
                continue
            if 'channelRenderer' in video_details:
                continue
            if 'horizontalCardListRenderer' in video_details:
                continue
            if 'didYouMeanRenderer' in video_details:
                continue
            if 'backgroundPromoRenderer' in video_details:
                continue
            if 'videoRenderer' not in video_details:
                continue
            vid_renderer = video_details['videoRenderer']
            vid_id = vid_renderer['videoId']
            vid_url = f'https://www.youtube.com/watch?v={vid_id}'
            vid_title = vid_renderer['title']['runs'][0]['text']
            vid_channel_name = vid_renderer['ownerText']['runs'][0]['text']
            vid_channel_uri = vid_renderer['ownerText']['runs'][0][
                'navigationEndpoint']['commandMetadata']['webCommandMetadata'][
                'url']
            if 'viewCountText' in vid_renderer:
                if 'runs' in vid_renderer['viewCountText']:
                    vid_view_count_text = vid_renderer['viewCountText']['runs'
                        ][0]['text']
                else:
                    vid_view_count_text = vid_renderer['viewCountText'][
                        'simpleText']
                stripped_text = vid_view_count_text.split()[0].replace(',', '')
                if stripped_text == 'No':
                    vid_view_count = 0
                else:
                    vid_view_count = int(stripped_text)
            else:
                vid_view_count = 0
            if 'lengthText' in vid_renderer:
                vid_length = vid_renderer['lengthText']['simpleText']
            else:
                vid_length = 'Unknown'
            vid_metadata = {'videoId': vid_id, 'title': vid_title,
                'duration': vid_length, 'thumbnail': vid_renderer[
                'thumbnail']['thumbnails'][0]['url']}
            videos.append(vid_metadata)
    else:
        videos = None
    return videos, next_continuation


def remove_duplicate_dicts(lst):
    print('Function remove_duplicate_dicts:', lst)
    seen = set()
    unique_dicts = []
    for d in lst:
        tuple_representation = tuple(d.items())
        if tuple_representation not in seen:
            seen.add(tuple_representation)
            unique_dicts.append(d)
    return unique_dicts


def search(term, conti):
    print('Function search:', term, conti)
    query_url = {'query': term, 'key':
        'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8', 'contentCheckOk': True,
        'racyCheckOk': True}
    endpoint_url = (
        f'https://www.youtube.com/youtubei/v1/search?{parse.urlencode(query_url)}'
        )
    query = {'context': {'client': {'clientName': 'WEB', 'clientVersion':
        '2.20200720.00.02'}}}
    if conti:
        query.update({'continuation': conti})
    baseheaders = {'User-Agent': 'Mozilla/5.0', 'accept-language':
        'en-US,en', 'Content-Type': 'application/json'}
    data = bytes(json.dumps(query), encoding='utf-8')
    if endpoint_url.lower().startswith('http'):
        request = urllib.request.Request(endpoint_url, headers=baseheaders,
            data=data, method='POST')
    else:
        raise ValueError('Invalid URL')
    response = urlopen(request)
    js = json.loads(response.read())
    print(js['refinements'])
    videos, continuta = praser(js)
    return remove_duplicate_dicts(videos), continuta


def scrap_data(vid):
    print('Function scrap_data:', vid)
    url = (
        'https://www.youtube.com/youtubei/v1/player?key=AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w&prettyPrint=false'
        )
    query = {'videoId': vid, 'params': 'CgIQBg==', 'playbackContext': {
        'contentPlaybackContext': {'html5Preference': 'HTML5_PREF_WANTS'}},
        'contentCheckOk': True, 'racyCheckOk': True}
    data = {'context': {'client': {'clientName': 'ANDROID', 'clientVersion':
        '17.31.35', 'androidSdkVersion': 30, 'userAgent':
        'com.google.android.youtube/17.31.35 (Linux; U; Android 11) gzip',
        'hl': 'en', 'timeZone': 'UTC', 'utcOffsetMinutes': 0}}}
    data.update(query)
    data2 = json.dumps(data).encode('utf8')
    headers = {'X-YouTube-Client-Name': '5', 'X-YouTube-Client-Version':
        '17.33.2', 'Origin': 'https://www.youtube.com', 'User-Agent':
        'com.google.android.youtube/17.31.35 (Linux; U; Android 11) gzip',
        'content-type': 'application/json'}
    request = urllib.request.Request(url, headers=headers, data=data2,
        method='POST')
    try:
        response = urlopen(request)
        js = json.loads(response.read())
        return js
    except urllib.error.HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))


def regex_search(pattern: str, string: str, group: int):
    print('Function regex_search:', pattern, string, group)
    regex = re.compile(pattern)
    results = regex.search(string)
    if not results:
        return False
    return results.group(group)


def contents_of_double_quotes(text):
    print('Function contents_of_double_quotes:', text)
    urls = []
    dq = re.findall('"([^"]*)"', text)
    for item in dq:
        urls.append(item)
    return urls


def find_mp4_urls(text):
    print('Function find_mp4_urls:', text)
    dq = re.findall('"([^"]*)"', text)
    for item in dq:
        if '.mp4' in item:
            return item


def particular_type_urls_finder(text, ft):
    print('Function particular_type_urls_finder:', text, ft)
    urls = []
    dq = re.findall('"([^"]*)"', text)
    for item in dq:
        if ft in item:
            urls.append(item)
    return urls


def mixed_url(text):
    print('Function mixed_url:', text)
    urls = []
    dq = re.findall('"([^"]*)"', text)
    for item in dq:
        if 'http' in item:
            urls.append(item)
    return urls


def m3u8f(text, filt):
    print('Function m3u8f:', text, filt)
    ul = []
    lines = str(text).split('\n')
    for i in lines:
        if filt in i:
            ul.append(i)
    return ul


def getSturl(vid, itag):
    print('Function getSturl:', vid, itag)
    info = scrap_data(vid)
    fmts = info['streamingData']['formats']
    if len(fmts) == 1:
        return fmts[0]['url']
    if itag == 140:
        adf = info['streamingData']['adaptiveFormats']
        for f in adf:
            if f['itag'] == 140:
                return f['url']
    for i in fmts:
        if i['itag'] == itag:
            return i['url']


def video_id(url: str) ->str:
    print('Function video_id:', url)
    if regex_search('(?:v=|\\/)([0-9A-Za-z_-]{11}).*', url, group=1):
        return regex_search('(?:v=|\\/)([0-9A-Za-z_-]{11}).*', url, group=1)
    else:
        print('invalid url')
