import login
import utils
import jwtoken as jwt


try:
        userDetails = jwt.getUserDetails()
except FileNotFoundError:
        logged_in = "false"
else:
        logged_in = userDetails["loggedIn"]

s = utils.getPrintNote()
print(s if logged_in != "true" else "")
print("====================================")
print(" Login Status: " + logged_in)
print("====================================")
if logged_in == "true":
            print("***********************")
            print("Please wait till the playlist is generated...")
            print("You may see a lot of lines being printed, you may ignore it")
            print("The generated m3u will be saved as allMoviesPlaylist.m3u under the code_samples directory")
            print("************************************")
            utils.m3ugen()
else:
            print("Please login with options 1 or 2 before generating playlist")