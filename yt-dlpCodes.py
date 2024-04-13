from yt_dlp import YoutubeDL
#_get_requested_clients
ydl_opts = {'cache_age':0}
with YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info("https://youtu.be/XbRrIYyQiGw?si=xbjBsAfORoanjKyC",
                                 download=False)
    print(info_dict)
    # videos = info_dict["formats"]
    # title = info_dict["title"]
    # print("formatsss")
    # # [youtube] NZSmagbz9wA: Downloading tv embedded player API JSON
    # for item in videos:
    #     print(item)
    #     print("end part of format")
# import TOOLBOX
# # dict_keys(['responseContext', 'playabilityStatus', 'streamingData', 'playbackTracking', 'captions', 'videoDetails', 'playerConfig', 'storyboards', 'trackingParams', 'attestation', 'endscreen', 'onResponseReceivedEndpoints', 'overlay', 'adBreakHeartbeatParams', 'frameworkUpdates'])
# infoJson=TOOLBOX.scrap_data("wBiNif9pqpk")
# # dict_keys(['expiresInSeconds', 'adaptiveFormats', 'hlsManifestUrl', 'aspectRatio', 'serverAbrStreamingUrl'])
# adaptiveFmts=infoJson["streamingData"]["adaptiveFormats"]
# hlsManifestUrl=infoJson["streamingData"]["hlsManifestUrl"]
# for i in adaptiveFmts:
#     print(i)
# print(hlsManifestUrl)