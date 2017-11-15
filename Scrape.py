# Author - Shivam Kapoor

# Importing libraries
from bs4 import BeautifulSoup
import urllib.request
import os,tldextract

# Creating Output folder
if (os.path.exists("Output")):
    delete = str('rm -r Output')
    os.system(delete)
    os.makedirs("Output")
    os.makedirs("Output/Positive")
    os.makedirs("Output/Negative")
else:
    os.makedirs("Output")

#################### Scraping Logic Below ###########################

# Collecting html content.
url = "https://gallery.123telugu.com/content/reviews/main/more_reviews_Telugu.html"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'),"html5lib")

# Finding Specific "a" tag data
links = []
aTag = soup.find_all("a", {"class": "NormalText"})

# Collecting all the links from given webpage
for tag in aTag:
    links.append(tag.get('href'))

# Saving links in a file
linkfile = open('links.txt', 'w')
for link in links:
    linkfile.write("%s\n" %link)

print (">>>>>> Links Scraping Finished <<<<<<")
print (">>>>>>>>> No of links - %s <<<<<<<<<" %(len(links)))
print (">>>Links can be found at links.txt<<<")

#################### Now links list contains all the links to scrape ###########################

for link in links:
    # Just for printing purposes
    i = 1
    print("\n>>> %s. Scraping data from %s <<<" %(i,link))
    i = i+1

    # Opening and scraping the data from every page.
    request = urllib.request.Request(link)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'),"html5lib")

    # Deciding File Name
    parts = link.split("/")
    name = parts[len(parts)-1].split(".")
    filename1 = str(os.path.abspath("") + '/Output/Positive-'+ name[0] + ".txt")
    filename2 = str(os.path.abspath("") + '/Output/Negative-'+ name[0] + ".txt")

    # Opening Files
    positivefile = open(filename1,"a")
    negativefile = open(filename2,"a")

    # Finding Specific DIV tag data
    divTag = soup.find("div", {"class": "post-content"})
    data = divTag.find_all("p")

    # Very complicated logic because encoding isn't supported.(Desi solution)
    # Here we are finding one anchor string which is not changing due to encoding
    # From there we are manually picking up data
    # Very complicated logic = NOT A GOOD CODE
    for i in range(0:len(data)):
        if "<p><strong>కథ :</strong></p>" in str(data[i]):
            savepoint1 = i
            break

    for i in range(savepoint1+1,len(data)):
        if "<p><strong>" in str(data[i]):
            savepoint2 = i
            break

    for i in range(savepoint2+1,len(data)):
        if "<p><strong>" in str(data[i]):
            savepoint3 = i
            break

    for i in range(savepoint3+1,len(data)):
        if "<p><strong>" in str(data[i]):
            savepoint4 = i
            break

    # Saving positive points in respective file
    for i in range(savepoint2+1,savepoint3):
        temp = str(data[i]).replace('<p>','').replace('/<p>','')
        postivefile.write(temp)

    # Saving negative points in respective file
    for i in range(savepoint3+1,savepoint4):
        temp = str(data[i]).replace('<p>','').replace('/<p>','')
        negativefile.write(temp)

        positivefile.close()
        negativefile.close()
