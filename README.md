# swiftprinterLOCALwebpage
faustrolands swift printer web page but local.
i did not code the swift printer web page.
most of the code that was changed in the files are from chatgpt (idk what the fuck im doing with shit like this)






# TUTORIAL (READ, READ, READ)

you first need WSL (windows subsystem for linux) if ur alr on linux idk if this will work then at all.
open a command prompt and paste wsl --install after it finishes, restart your computer.
after your computer restarts, open command prompt agan and paste wsl --install archlinux
wait for it to finish. after it is done, make sure you are in the archlinux WSL enviroment. if you aren't , go to your search bar and type in archlinux.
in the WSL environment paste pacman -Syu python3 once prompted press y
after python3 has installed, paste pacman -S python-pip
press y again.
after that, download the files in this github repo by pressing Code then download zip.
unzip the files in the Documents directory (NOT in Onedrive.)
in WSL run cd /mnt/c/Users/YOURWINDOWSUSRNAME/Documents    *replace YOURWINDOWSUSRNAME with the name of the folder that is not Default or Public in Users. you can find Users by going into your c drive then going to Users.
you should be in the Documents dir now. execute ls to see all files.
if you extracted the zip properly, there should be a folder called SwiftPrinterLOCAL.
type cd SwiftPrinterLOCAL (or whatever the folder's name is)
you are now in the main dir of the website.
now execute: pacman -S python-flask python-psutil imagemagick pngquant zip file
press y again.
now, you should be ready to run app.py.
execute python3 app.py
you should now see stuff like Running on ###  the one right before Press Ctrl+C to quit is the one you should use.
ctrl click the link.
now it should work!!!!!

everytime you need to use the local page, you need to run archlinux,and cd back to the documents folder and to the SwiftPrinterLOCAL folder. and obv run the app.py

# NO, this will not work without WSL. if you cant access it for whatever reason, idk man

# if you encounter any errors during this it may just be my horrible teaching. my discord is @cayrr.s if you have issues that u cant just chatgpt through.


this tut sucks lmao but wtv
