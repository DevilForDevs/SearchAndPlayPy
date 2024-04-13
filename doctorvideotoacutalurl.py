import os
import re

import requests

import TOOLBOX

urlb = "https://voe.sx/e/apfnxduaacco"
res = requests.get(urlb, stream=True)
pageSource = res.text
baseUrl = "https://delivery-node-8s8wso5f4w7ft6sg.voe-network.net/engine/hls2/01/00463/apfnxduaacco_,n,.urlset/"


def download_segments(base_url, relative_urls, output_directory):
    for relative_url in relative_urls:
        segment_url = base_url + relative_url
        filename = os.path.join(output_directory, os.path.basename(relative_url))
        response = requests.get(segment_url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(relative_urls.index(relative_url), "/", len(relative_urls))


# https://delivery-node-8s8wso5f4w7ft6sg.voe-network.net/engine/hls2/01/00463/apfnxduaacco_,n,.urlset/master.m3u8?t=ucF3rgcx0JB3kJXkJhW9KGZpfgf-vccOl5ooUoV9_xY&s=1710773550&e=14400&f=2319608&node=delivery-node-8s8wso5f4w7ft6sg.voe-network.net&i=157.35&sp=2500&asn=55836
# index-v1-a1.m3u8?t=ucF3rgcx0JB3kJXkJhW9KGZpfgf-vccOl5ooUoV9_xY&s=1710773550&e=14400&f=2319608&node=delivery-node-8s8wso5f4w7ft6sg.voe-network.net&i=157.35&sp=2500&asn=55836
# https://delivery-node-8s8wso5f4w7ft6sg.voe-network.net/engine/hls2/01/00463/apfnxduaacco_,n,.urlset/seg-2-v1-a1.ts?t=aYeAbVyP7DTyNmzvoVg1PFRJAXGR3PbktEV-fAOtY6o&s=1710773676&e=14400&f=2319608&node=delivery-node-8s8wso5f4w7ft6sg.voe-network.net&i=157.35&sp=2500&asn=55836
# https://delivery-node-8s8wso5f4w7ft6sg.voe-network.net/engine/hls2/01/00463/apfnxduaacco_,n,.urlset/iframes-v1-a1.m3u8?t=Beazrz6fef8HvnaTfq1rCIlk4lSttLV2YP_3_4yiRdE&s=1710843275&e=14400&f=2319608&node=delivery-node-8s8wso5f4w7ft6sg.voe-network.net&i=157.42&sp=2500&asn=55836
def download(url):
    request1 = requests.get(url, stream=True)
    url_pattern = re.compile(r'(?<=URI=")(.*?)(?=")')
    urls = url_pattern.findall(request1.text)
    request2 = requests.get(baseUrl + urls[0], stream=True)
    pattern = r'seg-\d+-v\d+-\w+\.\w+\?t=[\w-]+&s=[\d]+&e=[\d]+&f=[\d]+&node=[\w.-]+&i=[\d.]+&sp=[\d]+&asn=[\d]+'
    segment_urls = re.findall(pattern, request2.text)
    download_segments(baseUrl, segment_urls, "Doctor who season 1 episode 1.mp4")


urls = TOOLBOX.mixed_url(pageSource)
for url in urls:
    if ".m3u8" in url:
        print(url)
        download(url)
