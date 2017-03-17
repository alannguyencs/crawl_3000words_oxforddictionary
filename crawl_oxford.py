"""
Crawl dictionary from oxfordlearnersdictionaries.com
"""
import urllib2
import string
import time

printable = string.printable
exclude = set(string.punctuation)
digit = "0123456789"
for d in digit:
    exclude.add(d)
exclude.remove('-')
dictionary = open("3000words.txt", "w")

def clean(s):
    return ''.join(ch for ch in s.lower() if ch not in exclude)
def Crawl_page(url_page):
    try:
        response = urllib2.urlopen(url_page)
        word = clean(url_page.split("/")[-1])
        word = word.replace("-", " ")
        print word
        dictionary.write("word: " + word + "\n\n")
        web_data = response.read().decode('utf-8')
        web_data = ''.join(filter(lambda x: x in printable, web_data))  # delete strange character
        # print web_data
        content = web_data.split("jump to other results")[1].split("</div>\n")[0]
        # print content
        definition = content.split("class=\"def\"")
        for sub_def in definition[1:]:
            sub_def = sub_def.replace("class=\"cf\"", "class=\"x\"")
            sub_def = sub_def.split("class=\"x\"")
            # print sub_def[0].split("<")[0].split(">")[-1]
            def_word = sub_def[0].split("<")[0].split(">")[-1]
            if len(def_word) < 3:
                break
            dictionary.write("def: " + def_word+ "\n")
            for ss in sub_def[1:]:
                line = ""
                for block in ss.split("<")[:-1]:
                    line += block.split(">")[-1]
                if ". " or ".\n" in line:
                    line = line.split('.')[0]
                # print line
                dictionary.write("ex: " + line+ "\n")
            # print
            dictionary.write("\n")

        dictionary.write("-" * 5 + "\n\n")
    except Exception as e:
        print url_page

def Crawl_sub_Oxford3000(url_title, num):
    url = "http://www.oxfordlearnersdictionaries.com/wordlist/american_english/oxford3000/Oxford3000_" + url_title + "/?page=" + str(num)
    try:
        response = urllib2.urlopen(url)
        web_data = response.read().decode('utf-8')
        web_data = ''.join(filter(lambda x: x in printable, web_data))  # delete strange character
        url_set = web_data.split("href=\"")[1:]
        for link in url_set:
            link = link.split("\n")[0]
            if "title=" in link:
                word_link = link.split("\"")[0]
                if "oxford" in word_link:
                    Crawl_page(word_link)

    except Exception as e:
        print str(e)


def Crawl_Oxford3000():
    letter = ["A-B", "C-D", "E-G", "H-K", "L-N", "O-P", "Q-R", "S", "T", "U-Z"]
    for url_title in letter:
        for num in range(1,10):
            print url_title, num
            Crawl_sub_Oxford3000(url_title, num)


# Crawl_page("http://www.oxfordlearnersdictionaries.com/definition/english/abuse_1")
# Crawl_page("http://www.oxfordlearnersdictionaries.com/definition/american_english/ability_1")
# Crawl_page("http://www.oxfordlearnersdictionaries.com/definition/american_english/acceptable")
# Crawl_page("http://www.oxfordlearnersdictionaries.com/definition/american_english/active_1")

Crawl_Oxford3000()

dictionary.close()

