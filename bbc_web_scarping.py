from bs4 import BeautifulSoup
from collections import Counter
import requests
import pandas as pd
from tkinter import *
import threading





def web_scrape():

    global categories, headlines, headlineSet, links, linkSet, allArticleText, allArticleTextSet, categoryNames, storyLengths, categories2

    categories = ['https://www.bbc.com/urdu/topics/cjgn7n9zzq7t', 'https://www.bbc.com/urdu/topics/cw57v2pmll9t',
                  'https://www.bbc.com/urdu/topics/c340q0p2585t', 'https://www.bbc.com/urdu/topics/ckdxnx900n5t',
                  'https://www.bbc.com/urdu/topics/c40379e2ymxt']

    headlines = []  # column2
    headlineSet = set()
    links = []
    linkSet = set()
    allArticleText = []  # column3
    allArticleTextSet = set()
    categoryNames = []  # column1
    storyLengths = []

    categories2 = ['https://www.bbc.com/urdu/topics/c340q0p2585t']

    catNum = 1;
    # iterate through categories
    for category in categories:
        # iterate through 10 pages for each category

        for i in range(1, 12):
            page = requests.get(category + "/page/" + str(i)).text
            # print(page)
            soup = BeautifulSoup(page, 'lxml')

            articles = soup.find_all('article', class_='qa-post gs-u-pb-alt+ lx-stream-post gs-u-pt-alt+ gs-u-align-left')

            num = 1

            # iterate through 10 articles for each page

            for article in articles:
                if not article.find('figure') and not article.find('span', class_='lx-stream-asset__gallery-cta-icon gel-icon') and (
                        'live' not in article.find('a', class_='qa-story-cta-link')['href']):
                    headline = article.find('span', class_='lx-stream-post__header-text gs-u-align-middle')
                    headlines.append(headline.getText())
                    headlineSet.add(headline.getText())
                    read_more = article.find('a', class_='qa-story-cta-link')
                    read_more_link = read_more['href']
                    links.append(read_more_link)
                    linkSet.add(read_more_link)
                    headlines = list(dict.fromkeys(headlines))
                    links = list(dict.fromkeys(links))

                content = requests.get('https://www.bbc.com/' + read_more_link).text
                soup_2 = BeautifulSoup(content, 'lxml')
                paragraphs = soup_2.find_all('p', class_='bbc-1sy09mr e1cc2ql70')

                articleText = []
                articleTextSet = set()



                # iterate through paragraphs in each article
                for paragraph in paragraphs:
                    articleText.append(paragraph.getText())
                    #root.update()

                articleContent = ' '.join(articleText)
                allArticleText.append(articleContent)

                print('')
                print('category:', catNum, 'page:', i, 'article:', num)
                progress.config(text='FETCHING DATA...  Category: ' + str(catNum) + '  Page: ' + str(i) + '  Article: ' + str(num))
                num += 1
                print(read_more_link)
                print(articleText)
                print(articleContent)

        catNum += 1

    for k in links:
        myCategory = k.split('-')[0].split('/')[-1]
        categoryNames.append(myCategory)

    allArticleText = list(dict.fromkeys(allArticleText))


    # writing to csv
    csv_dict = {
        'label': categoryNames,
        'headline': headlines,
        'story': allArticleText
    }

    csv_file = pd.DataFrame(csv_dict)
    csv_file.to_csv('bbc_data.csv', encoding='utf-8-sig')

    progress.config(text="Scraping Finished. " + str(len(links)) + " Stories Retrieved")

    unique_words_button.config(state=NORMAL)
    stories_retrieved_button.config(state=NORMAL)
    shortest_story_button.config(state=NORMAL)
    longest_story_button.config(state=NORMAL)
    repeated_words_button.config(state=NORMAL)









# METHODS
# 1. Unique Words
def unique_words():
    dataset = ' '.join(categoryNames) + ' ' + ' '.join(headlines) + ' ' + ' '.join(allArticleText)
    datasetWordList = dataset.split()
    uniqueWords = set(datasetWordList)
    uniqueWordCount = len(uniqueWords)
    print("UNIQUE WORDS")
    print(uniqueWordCount)
    output.config(text='UNIQUE WORDS: ' + str(uniqueWordCount))
    output2.config(text='')
    output3.config(text='')

# 2. Number of stories retrieved for each category
def stories_retrieved():
    worldNum = categoryNames.count('world')
    pakistanNum = categoryNames.count('pakistan')
    sportNum = categoryNames.count('sport')
    entertainmentNum = categoryNames.count('entertainment')
    scienceNum = categoryNames.count('science')
    regionalNum = categoryNames.count('regional')

    print('STORIES RETRIEVED FOR EACH CATEGORY')
    print('world:', worldNum, 'science:', scienceNum, 'pakistan:', pakistanNum, 'sport:', sportNum,
          'entertainment:', entertainmentNum, 'regional:', regionalNum)
    output.config(text='STORIES RETRIEVED FOR EACH CATEGORY:')
    output2.config(text='World: ' + str(worldNum) + ',  Science: ' + str(scienceNum) + ',  Pakistan: ' + str(pakistanNum) + ',  Sports: ' + str(sportNum) +
          ',  Entertainment: ' +  str(entertainmentNum) + ',  Regional: ' + str(regionalNum))
    output3.config(text='')

# 3. Min and max length story
def min_story():
    for text in allArticleText:
        splitWords = text.split()
        storyLengths.append(len(splitWords))

    minLength = min(storyLengths)
    minIndex = storyLengths.index(minLength)
    minStory = [minLength, headlines[minIndex], allArticleText[minIndex]]
    print('MIN LENGTH STORY')
    print(minLength)
    print(links[minIndex])
    print(headlines[minIndex])
    print(allArticleText[minIndex])

    output.config(text='SHORTEST STORY: ' + str(minLength) + " Words")
    output2.config(text=('www.bbc.com' + links[minIndex]))
    output3.config(text=('Headline: ' + headlines[minIndex]))

def max_story():
    for text in allArticleText:
        splitWords = text.split()
        storyLengths.append(len(splitWords))

    maxLength = max(storyLengths)
    maxIndex = storyLengths.index(maxLength)
    maxStory = [maxLength, headlines[maxIndex], allArticleText[maxIndex]]
    print("MAX LENGTH STORY")
    print(maxLength)
    print(links[maxIndex])
    print(headlines[maxIndex])
    print(allArticleText[maxIndex])

    output.config(text='LONGEST STORY: ' + str(maxLength) + " Words")
    output2.config(text=('www.bbc.com' + links[maxIndex]))
    output3.config(text=('Headline: ' + headlines[maxIndex]))

# 4. Top 10 repeated words:
def most_repeated_words():
    stopwords = []
    dataset2 = ' '.join(categoryNames) + ' ' + ' '.join(headlines) + ' ' + ' '.join(allArticleText)
    dataset2_words = dataset2.split()

    with open('urdu_stopwords.txt', encoding='utf-8-sig') as f:
        for line in f:
            strip_lines = line.rstrip()
            stopwords.append(strip_lines)

    for i in range(len(stopwords)):
        if stopwords[i] in dataset2_words:
            dataset2_words = list(filter((stopwords[i]).__ne__, dataset2_words))

    dataset2 = ' '.join(dataset2_words)

    term_frequencies = Counter(dataset2.split())
    print(term_frequencies)

    mrw = ''
    print("MOST REPEATED WORDS")
    for i in range(10):
        max_key = max(term_frequencies, key=term_frequencies.get)
        print(max_key + ":", term_frequencies[max_key])
        mrw += max_key + ": " + str(term_frequencies[max_key]) + ",  "
        del term_frequencies[max_key]

    output.config(text='MOST REPEATED WORDS')
    output2.config(text=mrw)
    output3.config(text='')



# User Interface using tkinter:

root = Tk()
root.title("BBC URDU Web Scraper     Zain-Yawar-Aazain")

progress = Label(root, text='Click the button to fetch data')
progress.pack()

scrape_data = Button(root, text='Scrape Data', command=lambda: threading.Thread(target=web_scrape).start(), width=20, bg='green')
scrape_data.pack(pady = 10)

unique_words_button = Button(root, text='Unique Words', command=unique_words, state=DISABLED)
unique_words_button.pack(pady = 10)

stories_retrieved_button = Button(root, text='Stories Retrieved', command=stories_retrieved, state=DISABLED)
stories_retrieved_button.pack(pady = 10)

shortest_story_button = Button(root, text='Shortest Story', command=min_story, state=DISABLED)
shortest_story_button.pack(pady = 10)

longest_story_button = Button(root, text='Longest Story', command=max_story, state=DISABLED)
longest_story_button.pack(pady = 10)

repeated_words_button = Button(root, text='Most Repeated Words', command=most_repeated_words, state=DISABLED)
repeated_words_button.pack(pady = 10)

output = Label(root, text='')
output.pack(pady = 10)
output2 = Label(root, text='')
output2.pack(pady = 5)
output3 = Label(root, text='')
output3.pack(pady = 5)


root.geometry('650x425')

root.mainloop()

