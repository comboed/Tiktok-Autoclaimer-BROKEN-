This is being released becuase thee endpoints are all patched.

A Tiktok Autoclaimer and Turbo. Automanically checks and claims usernames over a period time using Tiktok's Mobile 

**Install**
* Download Python (Version 3.8) and check 'Enviroment Variable' during setup
* Run the follow command in CMD - **python -m pip install colorama discord_webhook pycurl**
* Run the script and it will generate all the required data needed for usage

**Usage**
* The Autoclaimer uses Mobile Tiktok Session ID's to check and claim. This can be grabbed using an rooted/jailbroken device with SSL Unpinning.
* Account Session's go in 'sessions.txt' in the following format: *email:password:session*
* Target's go in the 'usernames.txt' in the following format: *username:uid*. In the case where there is no UID provided, it will get the one associated with the username
    * If the username is banned, the autoclaimer will generate a .txt doccument of the username with the old UID  
    * If the username is swapped, the autoclaimer will send a webhook if provided with the old UID and the new one

**Know Issues**
* Error installing Pycurl:
    * Pycurl is a linux based package. If the user is on a window's device, it will be required to build the package from scratch.
