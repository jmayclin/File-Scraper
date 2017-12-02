import requests
import os

def inputs():
    url = input("Enter the url of the webpage that contains the links to download:")
    
    print("Enter desired download path.")
    path = input("\"./subdirectory\" or press enter for current:")
    if path == '':
        path = '.'
    
    print("Would you like to restrict the downloaded link to a certain word? e.g. pdf")
    query_word = input("Something must be inputted:")
    
    print("Would you like to check before you download each file?")
    check = input("(Y)es or (N)o:")
    check = False if check.lower() == 'n' else True
    
    return url, path, query_word, check
    
def create_subdirectory(path):
    if path == '.': return
    if not os.path.exists(path):
        os.makedirs(path)

def find_hrefs(request):
    string = request.text
    begin = 0
    markers = []
    while string.find('a href=', begin) != -1:
        start = string.find('a href', begin) + len('a href=')
        end = string.find('>', start)
        markers.append((start, end))
        begin = end
    contained = [string[index[0]:index[1]] for index in markers]
    return contained
    
def constrain_hrefs(contained, query_word):
    print(query_word)
    formats = [s for s in contained if (s.lower().find(query_word.lower()) != -1)]
    print("Found the following:")
    for link in formats:
        print(link)
    return formats
    
def download(links, path, url, check):
    url = url[:url.rfind('/')]
    for link in links:
        if check:
            continueResponse = input("Download " +  link + "? (Y) or (N):")
            if continueResponse.lower() == 'n': break
        print('Requesting ', link)
        full_url = url + '/' + link
        r = requests.get(full_url)
        print('Downloading ', link)
        full_path = path + '/' + link
        with open(full_path, 'wb')as f:
            f.write(r.content)

#url = 'https://stats200.stanford.edu/lectures.html'
#query_word = 'lecture'
url, path, query_word, check = inputs()
#print(query_word.strip() == 'Lecture')

#url, query_word, path, check = 'https://stats200.stanford.edu/lectures.html', 'lecture', './tmp2', True
r = requests.get(url)
all_links = find_hrefs(r)
to_download = constrain_hrefs(all_links, query_word)

create_subdirectory(path)
download(to_download, path, url, check)


    