from urllib.parse import urlparse
import sys 
import os
import subprocess
import requests
import random
import time
import pathlib
import json 
from hashlib import sha1

# formats a byte array into hexadecimal encoded by chars
HEX_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
def getFormattedText(bArr: bytes): 
    length = len(bArr)
    sb2 = ''
    for i10 in range(length):
        cArr = HEX_DIGITS
        sb2 += cArr[(bArr[i10] >> 4) & 15]
        sb2 += cArr[bArr[i10] & 15]
    return sb2

# hash app specific secret with random string and timestamp
SECRET = "tingshu3dbeb952d32d8a7f30f5dd88"
def getCheckSum(randomStr, curTime):
    digest = sha1((SECRET + randomStr + curTime).encode('utf-8')).digest()
    return getFormattedText(digest)

def current_milli_time():
    return round(time.time() * 1000)

chars = list("abcdefghijklmnopqrstuvwxyz0123456789")
def getRandomStr():
    random.shuffle(chars)
    return ''.join(chars[:8])

def getNewHeaders():
    curTime = str(current_milli_time())
    randomStr = getRandomStr()
    checkSum = getCheckSum(randomStr, curTime)
    # backend uses packageName (which it knows SECRET for), nonce and curtime to validate checksum
    checkSumDTO = {
        "appid": "20210621161",
        "nonce": randomStr,
        "curtime": curTime,
        "checksum": checkSum,
        "packageName": "com.listenbook.god",
        "version": "1.3.0"
    }
    return {
        "checkSumDTO": json.dumps(checkSumDTO),
        "packageId": "com.listenbook.god",
        "version": "1.3.0",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; PCT-AL10 Build/N6F26Q)"
     }

def respData(url, body):
    return requests.post(url, headers=getNewHeaders(), json=body).json()

def dumpTo(data, path):
    pathlib.Path(path).write_text(json.dumps(data))

def searchBooksFor(term, page=1):
    url = "https://listenbookslst.com/api/book/bookSearch"
    return respData(url, {"pageNum": str(page), "searchTerms": term, "pageSize": "20"})['data']['bookList']

def getChapterUrl(chapterId) -> str:
    url = "https://listenbookslst.com/api/book/getUrlByChapterId"
    return respData(url, {"chapterId": chapterId})["data"]["chapterUrl"]

def getChapterList(bookId):
    url = "https://listenbookslst.com/api/book/getNewBookChapterList"
    chapterList: list =  respData(url, {"bookId": str(bookId)})["data"]["chapterList"]
    chapterList.sort(key=lambda chap: chap["chapterIndex"]) # sort just in case
    return chapterList

def getAllChannelAndBook():
    url = "https://listenbookslst.com/api/book/getAllChannelAndBook"
    return requests.post(url, headers=getNewHeaders()).json()


def getMediaDuration(path):
    return int((subprocess.run(f"ffprobe -v quiet -of csv=p=0 -show_entries format=duration {path}", 
                               shell=True, capture_output=True).stdout.decode().strip().replace(".", "")))

# metafile in format ffmpeg wants
def makeMetaFile(bookName, authorName, chapterList: list, fileType):
    with open(f"{bookName}/metadata", "w") as m:
        m.write(f";FFMETADATA1\ntitle={bookName}\nartist={authorName}\n")
        pos = 0
        for chap in chapterList:
            microsecs = getMediaDuration(f"{bookName}/{chap['chapterIndex']}.{fileType}")
            chapStr = f"""[CHAPTER]
TIMEBASE=1/1000000
START={pos}
END={pos + microsecs}
title={chap['chapterName']}
"""
            m.write(chapStr)
            pos += microsecs + 1

# alternative ffmpeg commands i experimented with:
# os.system(f"cd {bookName} && ffmpeg -hide_banner -y -f concat -i files -i metadata -map_metadata 1 -c:a:0 {fileType} {bookName}.{fileType}")
# ffmpeg -y -i bookname.m4a -i cover.png -map 0:a -map 1:0 -c:1 copy -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" test.mp3
# "ffmpeg -hide_banner -y -f concat -i files -i metadata -map_metadata 1 -c:a aac -strict experimental out.m4b"
def combineFiles(bookName, fileType):
    err = os.system(f"cd {bookName} && ffmpeg -hide_banner -y -f concat -i files -i metadata -map_metadata 1 -map 0:a -c:a aac -strict experimental -vn {bookName}.m4b")
    if err:
        print("unsuccessful converting files")

# dowloads all chapters by default
def downloadNChapters(bookData, n = None):
    fileType = None
    bookName, authorName = bookData['bookName'], bookData['authorName']
    chapterList = getChapterList(bookData['bookId'])
    if n != None:
        chapterList = chapterList[:n]
    if not os.path.isdir(bookName):
        os.mkdir(bookName)
        for chap in chapterList:
            chapterUrl = getChapterUrl(chap["chapterId"])
            if fileType == None:
                fileType = urlparse(chapterUrl).path.split('.')[-1]
                if not fileType:
                    fileType = 'out'
            print(f"downloading chapter {chap['chapterIndex']}")
            os.system(f"curl '{chapterUrl}' --output-dir {bookName} -o {chap['chapterIndex']}.{fileType}")
            time.sleep(random.randint(1, 3))
    pathlib.Path(f"{bookName}/files").write_text(
            '\n'.join(map(lambda chap: f"file {chap['chapterIndex']}.{fileType}", chapterList)))

    makeMetaFile(bookName, authorName, chapterList, fileType)
    combineFiles(bookName, fileType)

def saveCoverImage(bookData):
    bookName = bookData['bookName']
    fileEnding = str(bookData['coverImageUrl']).split('.')[-1]
    os.system(f"curl '{bookData['coverImageUrl']}' -o {bookName}/{bookName}.{fileEnding}")


if __name__ == "__main__":
    action = sys.argv[1]
    term = sys.argv[2]
    if action != "search":
        print(f"unknown command '{action}'")
        exit(1)
    results = searchBooksFor(term)
    if len(results) == 0:
        print("No results")
        exit()
    for i, r in enumerate(results):
        bookName, author, bookId, intro, imageUrl = r['bookName'], r['authorName'], r['bookId'], r['introduction'], r['coverImageUrl']
        print(f"Book {i + 1}: {bookName} by {author}, id {bookId}\ncover: {imageUrl}\n{intro[:60]}...\n")

    sel = int(input("Select 1, 2, ...: "))
    bookData = results[sel - 1]
    downloadNChapters(bookData)
    saveCoverImage(bookData)
    # os.popen(f"cd {bookData['bookName']} && rm ./*.out ./files ./metadata && cd ..")
