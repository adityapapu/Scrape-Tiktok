import sys
import time
import csv
import undetected_chromedriver as uc
import emoji
import pyprind


options = uc.ChromeOptions()

# options.headless=True
# options.add_argument('--headless')
chrome = uc.Chrome(options=options)
chrome.implicitly_wait(10)

height=0
countVideos=-1

def clean(s):
    s=s.replace("\u30b7","")
    s=s.replace("\ufe0f","")
    s=s.replace("\ufffc","")
    s=s.replace("\ufe0f","")
    return emoji.get_emoji_regexp().sub("", s)


def writeCSV(userName, description, likeCounts, commentCounts, shareCounts):
    description=clean(description)
    # print(userName, description, likeCounts, commentCounts, shareCounts)
    with open(fileName+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([userName, description, likeCounts, commentCounts, shareCounts])
    global countVideos
    countVideos+=1
    bar.update()

def scroll():
    global height
    height += 500
    time.sleep(5)
    chrome.execute_script("window.scrollTo(0, " + str(height) + ");")
    new_height = chrome.execute_script("return document.body.scrollHeight")
    # print(new_height, height)
    if height - new_height > 4000:
        # print("End is reached")
        return False


def idIsMain(i):
        global height
        try:
            # print("main")
            scroll()
            userName = chrome.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/div[1]/span[" + str(i) + "]/div/div/div[1]/a[1]/h3").text
            description = chrome.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/div[1]/span[" + str(i) + "]/div/div/div[2]").text
            likeCounts = chrome.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div[1]/span[" + str(
                i) + "]/div/div/div[5]/div[2]/div[1]/strong").text
            commentCounts = chrome.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/div[1]/span[' + str(
                i) + ']/div/div/div[5]/div[2]/div[2]/strong').text
            shareCounts = chrome.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/div[1]/span[' + str(
                i) + ']/div/div/div[5]/div[2]/div[3]/strong').text
            writeCSV(userName, description, likeCounts, commentCounts, shareCounts)
        except Exception as e:
            # print(e)
            # print("Now run except")
            if scroll()==False:
                return -1

def idIsApp(i):
    global height
    try:
        # print("app")
        scroll()
        userName = chrome.find_element_by_xpath(
            "//*[@id='app']/div[2]/div[2]/div[1]/div/div[" + str(i) + "]/div/div[1]/div[1]/a[2]/h3").text
        description = chrome.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div[1]/div/div[' + str(i) + ']/div/div[1]/div[2]').text
        likeCounts = chrome.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div[1]/div/div[' + str(i) + ']/div/div[2]/div[2]/button[1]/strong').text
        commentCounts = chrome.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div[1]/div/div[' + str(i) + ']/div/div[2]/div[2]/button[2]/strong').text
        shareCounts = chrome.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div[1]/div/div[' + str(i) + ']/div/div[2]/div[2]/button[3]/strong').text
        writeCSV(userName, description, likeCounts, commentCounts, shareCounts)
    except:
        # print("App except")
        if scroll()==False:
            return -1

def checkTheID():
    try:
        chrome.find_element_by_xpath(
            "//*[@id='main']/div[2]/div[2]/div/div[1]/span[" + str(2) + "]/div/div/div[1]/a[1]/h3")
        return True
    except:
        return False

def getVideos():
    global height
    height=0
    i=1
    chrome.get('https://www.tiktok.com/foryou')
    time.sleep(10)
    temp = checkTheID()
    while True:
        if totalVideos<=countVideos:
            # print("reached the target")
            return
        if temp:
            i+=1
            if idIsMain(i)==-1:
                break
        else:
            i+=1
            if idIsApp(i)==-1:
                break


if __name__ == "__main__":
    users = dict()
    totalVideos=int(input("Enter the total numbers of videos you want to scrape: "))
    fileName=input("Enter the file name: ")
    bar = pyprind.ProgBar(totalVideos+1, stream=sys.stdout)
    writeCSV("UserName","Description","Total Like","Total Comments","Toatal Shares")
    while totalVideos>countVideos:
        try:
            getVideos()
        except Exception as e:
            print(e)

