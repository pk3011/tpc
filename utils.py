# Generates Kodi playlist by default, If you want OTT Navigator Supported Playlist, pass '--ott-navigator' as argument.
import jwtoken as jwt
import json as json



m3ustr = ''
kodiPropLicenseType = "#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha"


def processTokenChunks(contentList):
    global m3ustr
    kodiPropLicenseUrl = ""
    result=dict()
    for onecontent in contentList:
      result[onecontent["content_id"]] = onecontent
    if not contentList:
        print("content List is empty ..Exiting")
        exit(1)
    for content in contentList:
     if content['content_url'] != "dummy":
        ls_session_key = jwt.generateJWT(content['content_id'], result, iterative=False)
        if ls_session_key != "":
            licenseUrl = content['content_license_url'] + "&ls_session=" + ls_session_key
            kodiPropLicenseUrl = "#KODIPROP:inputstream.adaptive.license_key=" + licenseUrl + "|Content-Type=application/octet-stream|R{SSM}|"
        else:
            print("Didn't get license for content: Id: {0} Name:{1}".format(content['content_id'],
                                                                            content['content_name']))
            print('Continuing...Please get license manually for content :', content['content_name'])
        m3ustr += kodiPropLicenseType + "\n" + kodiPropLicenseUrl + "\n" + "#EXTINF:-1 "
        m3ustr += "group-title=" + "\"" + content['content_genre'] + "\" " + "tvg-logo=\"" + content['content_logo'] + "\" ," + content['content_name'] + "\n" + content['content_url'] + "\n\n"



def m3ugen():
    global m3ustr
    contentList = jwt.getContentList()
    processTokenChunks(contentList)

    print("================================================================")
    print("Found total {0} contents subscribed by user \nSaving them to m3u file".format(len(contentList)))
    print("================================================================")
    saveM3ustringtofile(m3ustr)


def saveM3ustringtofile(m3ustr):
    with open("allCatcupDetails.m3u", "w") as allcontentPlaylistFile:
        allcontentPlaylistFile.write(m3ustr)
        allcontentPlaylistFile.close()
def getPrintNote():
    s = " *****************************************************\n" + "Welcome To TataSky Channel Generation Script\n" + \
        "**********************************************************\n" + \
        "- Using this script you can generate playable links based on the channels you have subscribed to \n" + \
        "- You can always read the README.md file if you don't know how to use the generated file \n" + \
        "- You can login using your password or generate an OTP. You need to enter both the Registered Mobile Number \n" + \
        "\n Caution: This doesn't promote any kind of hacking or compromising anyone's details"

    return s

if __name__ == '__main__':
    m3ugen()
