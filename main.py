from bs4 import BeautifulSoup
import webbrowser
import requests
import csv


def open_url(url):
    '''Open websites with new informations'''
    try: 
        webbrowser.open_new(url)
        print('Opening URL...')  
    except: 
        print('Failed to open URL.')

def load_archive(file_name):
    ''''load old articles'''
    # titles of old news
    old_titles = []
    # adresses of old news 
    old_links = []

    # read csv archive
    try:
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            archive_reader = csv.reader(csvfile, delimiter=';', quotechar='|')

            # save read information to variables
            for row in archive_reader:
                old_titles.append(row[0])
                old_links.append(row[1])
    except:
        print("Couldn't read file")

    return old_titles, old_links

def scrap_page(archived_titles):
    '''Scrap news from page'''

    # link to page to scrap
    scrapped_page = 'http://www.wieik.pk.edu.pl'
    source = requests.get(scrapped_page).text
    soup = BeautifulSoup(source, 'lxml')

    # find all containers of class news
    news = soup.find_all('div', class_='news')
    links = []
    titles = []

    # for all found divs of class news
    for info in news:

        # store title 
        title = info.h2.a.text
        # store link
        link = scrapped_page+info.h2.a['href']

        if title in archived_titles:
            # if all new articles are found, stop searching 
            break

        titles.append(title)
        links.append(link)

    return titles, links


def save_archive(file_name, titles, links):
    '''Save uptaded archive to a file'''

    try:
        # open file and save all collected informations 
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            archive_writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for title, link in zip(titles, links):
                archive_writer.writerow([title,link])
    except:
        print("Couldn't save file")

if __name__ == '__main__':

    archive_name = 'archiv1e.csv'

    # load old and new articles
    old_titles, old_links = load_archive(archive_name)
    titles, links = scrap_page(old_titles)

    # if nothing new found exit 
    if len(titles) == 0:
        print("No new news found. Exiting...")
        exit(0)

    # open pages with news
    for title,link in zip(titles, links):
        open_url(link)


    # extend titles and links to save by archived news
    titles.extend(old_titles[:20-len(titles)])
    links.extend(old_links[:20-len(links)])

    save_archive(archive_name, titles, links)

