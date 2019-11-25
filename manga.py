import requests
import re
import os
import urllib.request as urllib
from bs4 import BeautifulSoup as bs

main_url = "http://www.mangareader.net"
header = {"Accept-Encoding": "identity"}

#TODO: Implemt error handling!!!

"""
    getPage

Purpose: Parse the link to get it's html form and return a Beautiful Soup object 

Parameters:
    String url  The url link to the website

Return value:
    BeautifulSoup object to reference the page
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

Return value:
    List of chapters in url format. (eg. ['/naruto/1', '/naruto/2', ... etc])
"""
def getChapterUrl(manga):
    #Clean the manga name of symbols
    manga_name = re.findall("[A-Za-z0-9\s]", manga)
    manga_name = ''.join(manga_name)
    #Convert white spaces to -
    manga_name = re.sub("\s", "-", manga_name.lower())
    #Build the url to the manga
    url = '{0}/{1}'.format(main_url, manga_name)
    print("Url: " + url)
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

"""
    getPageNymber

Purpose: Get the page numbers of a chapter and return a list of the page numbers

Parameters:
    BeautifulSoup url_soup  BeautifulSoup object of the url

Return value:
    List of pages in url format with a specified chapter. (eg. ['/naruto/1/1', '/naruto/1/2', ... etc])
"""
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

"""
    getImages

Purpose: Stores the images in a list for every page of the chapter

Parameters:
    String chapter_url      The url of the chapter 
    int[] pages             List of pages of the chapter

Return value:
    List of url to the images
"""
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

"""
    downloadImages

Purpose: Create a directory for the manga and create a directory inside of the manga
         for the chapter if they do not exist. Downloads the images to the manga's
         chapter's directory. (eg. naruto/Chapter1)

Paramenters:
    String images       List of urls to the images
    String manga_name   Name of the manga
    Int chapter_number  The chapter number

Return value:
    None
"""
def downloadImages(images, manga_name, chapter_number):
    current_directory = os.getcwd()
    #Creating directory strings
    manga_directory = current_directory + "/" + manga_name
    chapter_directory = manga_directory + "/Chapter" + str(chapter_number)
    download_directory = manga_name + "/Chapter" + str(chapter_number)

    page_num = 1
    image_name = "page"
    #Creates a directory for the manga if it does not exist
    if not os.path.exists(manga_directory):
        os.makedirs(manga_directory)
    #Create a directory for that manga's chapter if it does not exist
    if not os.path.exists(chapter_directory):
        os.makedirs(chapter_directory)
    #Iterate through the list of images
    for image in images:
        #Send a request for the image url
        request = urllib.Request(image)
        request.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
        #Open the url
        response = urllib.urlopen(request)
        #Get the image
        response_image = response.read()
        #Create the path where the image is downloaded
        file_name = download_directory + "/" + image_name + str(page_num) + ".jpg"
        #Download the image 
        with open(file_name, 'wb') as outfile:
            outfile.write(response_image)
        page_num += 1

def main():
    #Name of the manga
    manga = input("Enter the name of the manga you would like to download: ")

    #Chapter the user wishes to download
    chapter_to_download = int(input("Enter the chapter you want to download: "))

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

    #Download the images
    downloadImages(images, manga, chapter_to_download)

    print("Download complete!")

main()