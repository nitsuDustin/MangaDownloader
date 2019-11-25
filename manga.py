import requests
import re
import os
from bs4 import BeautifulSoup as bs

main_url = "http://www.mangareader.net"
header = {"Accept-Encoding": "identity"}
#sample = open('sample.txt', 'w')

"""
    getPage

Purpose: Parse the link to get it's html form and return a Beautiful Soup object 

Parameters:
    String url  The url link to the website
"""
def getPageSoup(url):
    #Send a request to access the page
    page = requests.get(url, headers=header)
    #Parse the page to get it's html 
    soup_page = bs(page.text, "html.parser")
    return soup_page


"""
    getChapterUrl

Purpose: Search through the html and find the link to all chapters

Parameters:
    String manga   The name of the manga 
"""
def getChapterUrl(manga):
    #Clean the manga name of symbols
    manga_name = re.findall("[A-Za-z0-9\s]", manga)
    manga_name = ''.join(manga_name)
    #Convert white spaces to -
    manga_name = re.sub("\s", "-", manga_name.lower())
    #Build the url to the manga
    url = '{0}/{1}'.format(main_url, manga_name)
    print("Url:" + url)
    page = getPageSoup(url)
    chapter = []
    #Find the html element that contains the chapters
    chapter_list = page.find(id="listing")
    #Find all of the chapters in the html element above
    links = chapter_list.findAll('a')
    for link in links:
        if(manga_name in link['href']):
            chapter.append(link['href'])   
    return chapter

def getPageNumbers(url_soup):
    pages = []
    #Find the select element in the html
    page_select = url_soup.findAll('select')[1]
    #Get all the page numbers
    page_option = page_select.findAll('option')
    #Iterate through all the page numbers
    for page in page_option:
        #Append the page number to a list of pages
        pages.append(page['value'])
    return pages

def getImages(chapter_url, pages):
    images = []
    #Iterate through all the pages in the chapter
    for page in pages:
        #Create a new Beautiful Soup object for every page
        page_soup = getPageSoup(main_url + page)
        #Find the image on the page
        chapter_image = page_soup.find(id="img")
        #Get the source of the image
        img_src = chapter_image['src']
        #Append the source to a list of images
        images.append(img_src)
    return images

def downloadImages(images, manga_name, chapter_number):
    current_directory = os.getcwd()
    manga_directory = current_directory + "/" + manga_name
    #print(chapter_number)
    #if not os.path.exists(manga_directory):
    #    os.makedirs(manga_directory)
    
    print(manga_directory)
    print(chapter_number)

def main():
    #Name of the manga
    manga = raw_input("Enter the name of the manga you would like to download: ")

    #Chapter the user wishes to download
    chapter_to_download = int(raw_input("Enter the chapter you want to download: "))

    #Convert chapter to index for the list
    chapter = chapter_to_download-1

    #Get the list of chapters
    chapters = getChapterUrl(manga)

    #URL of the chapter
    chapter_url = main_url + chapters[chapter]

    #List of pages for the specified chapter
    pages = getPageNumbers(getPageSoup(chapter_url))

    #List of images of the chapter
    images = getImages(chapter_url, pages)

    downloadImages(images, manga, chapter_to_download)

    #print(pages)



#getChapterUrl("Naruto!")
#getPageNumbers(getPage("https://www.mangareader.net/naruto/1"))
main()