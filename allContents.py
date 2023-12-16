#produce code below to get api call method using end point "https://tm.tapi.videoready.tv/homescreen/pub/api/v4/rail/seeAll?limit=1000&id=4203"
import requests
import json as json


content_list = []

def getUserDetails():
    with open("userDetails.json", "r") as userDetailFile:
        userDetails = json.load(userDetailFile)
    return userDetails

def getContentInfo(contentId):
    url = "https://tm.tapi.videoready.tv/content-detail/pub/api/v1/catchupEpg/{}".format(contentId)
    x = requests.get(url)
    if (x.json()['code']==8):
      url = "https://tm.tapi.videoready.tv/content-detail/pub/api/v1/vod/{}".format(contentId)
      x = requests.get(url)
      content_meta = x.json()['data']['meta']
      content_genre_alt = x.json()['data']['meta']['genre']
      content_detail_dict = x.json()['data']['detail']
      content_genre = content_meta.get('masterGenre[0]','')
      content_logo = content_meta.get('previewImage','')
      content_name = content_meta.get('title', ''),
    else:
        content_meta = x.json()['data']['meta']
        content_genre_alt = x.json()['data']['meta'][0]['genre']
        content_detail_dict = x.json()['data']['detail']
        content_genre = content_meta[0].get('primaryGenre','')
        content_logo = content_meta[0].get('transparentImageUrl','')
        content_name= content_meta[0].get('title', ''),
    #covert content_genre list to string with comma
    if content_genre_alt is None:
           content_genre = content_genre
    else:
           content_genre = content_genre_alt[0]

    onecontent = {
        "content_id": str(contentId),
        "content_name": str(content_name).replace("('",'').replace("',)",''),
        "content_license_url": content_detail_dict.get('dashWidewineLicenseUrl', ''),
        "content_url": content_detail_dict.get('dashWidewinePlayUrl', ''),
        "content_entitlements": content_detail_dict.get('entitlements', ''),
        "content_logo": content_logo,
        "content_genre": content_genre
    }
    content_list.append(onecontent)

def savecontentsToFile():
    print(len(content_list))
    with open("allcontents.json", "w") as content_list_file:
        json.dump(content_list, content_list_file)
        content_list_file.close()


def processChunks(content_lists):
    for content in content_lists:
        print("Getting contentId:{}".format(content.get('id', '')))
        content_id = str(content.get('id', ''))
        getContentInfo(content_id)

def getHeaders():
    userDetails = getUserDetails()
    accessToken = userDetails['accessToken']
    profileId = userDetails['profileId']
    headers = {
    'authorization': 'bearer ' + accessToken,
    'platform': 'web',
    'profileid': str(profileId)
    }
    return headers

def getAllContents():
    ids=[2703,4088,70768,704,12,760,6987,1552]
    for id in ids:
        url = "https://tm.tapi.videoready.tv/homescreen/pub/api/v3/rail/{}".format(id)
        x = requests.get(url)
        content_list = x.json()['data']['contentList']
        print("Total contents fetched:", len(content_list))
        print("Fetching content info..........")
        processChunks(content_list)
        print("Saving all to a file.... " + str(len(content_list)))
        savecontentsToFile()
    POST_URL="https://tm.tapi.videoready.tv/ta-recommendation/api/v1/recommend/UC_LAST_7DAY_EPISODES?max=20&layout=LANDSCAPE"
    x = requests.request("POST",POST_URL,headers=getHeaders(), data={})
    content_list = x.json()['data']['contentList']
    print("Total contents fetched:", len(content_list))
    print("Fetching content info..........")
    processChunks(content_list)
    print("Saving all to a file.... " + str(len(content_list)))
    savecontentsToFile()



if __name__ == '__main__':
    getAllContents()

