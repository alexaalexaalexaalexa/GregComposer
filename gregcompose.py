#get words
#make graph using words
#get next word for x number of words, as defined by user
#show the user

import requests
from bs4 import BeautifulSoup
import random
import string
from greggraph import Graph, Vertex

def get_gregwords():
    
    url = 'https://over-the-garden-wall.fandom.com/wiki/Transcript'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    greglines = []
    for i, tag in enumerate(soup.select('p'), start=1):
        line = tag.get_text(strip=True)
        if line.startswith("Greg"):
            greglines.append(line)
    with open ("greg_lines.txt", "w", encoding="utf-8") as f:
        for line in greglines:
            f.write(line + "\n")
    with open("greg_lines.txt", "r") as f:
        gregtext = f.read()
        gregtext = ' '.join(gregtext.split())
        gregtext = gregtext.lower()
        gregtext = gregtext.translate(str.maketrans('','',string.punctuation))
    gregwords = gregtext.split()
    return gregwords

def make_greg_graph(gregwords):
    g = Graph()
    prev_word = None
    for word in gregwords:
        word_vertex = g.get_vertex(word)
        if prev_word:
            prev_word.increment_edge(word_vertex)
        prev_word = word_vertex
    g.generate_probability_mappings()
    return g
        
def compose(g, gregwords, length=50):
    composition = []
    gregword = g.get_vertex(random.choice(gregwords))

    for _ in range(length):
        composition.append(gregword.value)  

        next_vertex = g.get_next_word(gregword) 
        if next_vertex is None:
            gregword = g.get_vertex(random.choice(gregwords)) 
        else:
            gregword = next_vertex

    return composition


def main():
    gregwords = get_gregwords()
    g=make_greg_graph(gregwords)
    composition = compose (g, gregwords, 100)
    return ' '.join(composition)

if __name__== '__main__':
    print(main())

