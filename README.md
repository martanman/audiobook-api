This project repackages in the form of a python script 
the requests made by a [certain android application](https://apkpure.com/%E5%90%AC%E4%B9%A6%E7%A5%9E%E5%99%A8%EF%BC%9A%E7%9C%9F%E4%BA%BA%E6%9C%89%E5%A3%B0%E5%B0%8F%E8%AF%B4%E3%80%81%E4%B9%A6%E7%B1%8D%E3%80%81%E6%95%85%E4%BA%8B%E3%80%81%E7%9B%B8%E5%A3%B0%E3%80%81%E5%B0%8F%E5%93%81%E3%80%81%E6%AE%B5%E5%AD%90/com.listenbook.god) that allows a user to search for
and download audiobooks from a content server backend.
It was made by decompiling the mobile app's .apk package to get the its assets
and (partially decompiled) Java code. 
Main examples of the useful decompiled Java files
are in the `java_samples` directory. `source_api.json` is a smaller part of a backend sources
json file found in the app's assets which contains the api details that the program
understands (though not very human intelligible).

The script can be used with 
``` python3 rep.py search '<search term(s) go here>'
```

Note that most books hosted are Chinese titles. A user can then select a result 
which the program will proceed to download the files for 
(split into chapters). It will then attempt to combine the individual chapter audio files
and cover image into a single `.m4b` file using ffmpeg. If ffmpeg is not on the command line, 
this part fails. Due to different audio file types used for each book, 
this conversion step may take many minutes (when converting from certain 
audio codings) and doesn't always succeed.
