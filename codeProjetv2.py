# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:16:56 2020

@author: HP
"""

from nltk.corpus import stopwords

import datetime as dt
from gensim.summarization.summarizer import summarize
import pickle
import re
import praw
import urllib.request
import xmltodict


 
try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    stopwords = set(stopwords.words('english'))
    
    
################################## Class author ##################################
class Author():
    
    #constructeur
    def __init__(self,name):
        self.name = name
        self.production = {} 
        self.ndoc = 0
        
    def add(self, doc):     
        self.production[self.ndoc] = doc
        self.ndoc += 1

    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)
    def __repr__(self):
        return self.name
    
    
################################## Class document ##################################

class Document():
    
    # constructor
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    # getters
    
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
        
    def get_text(self):
        return self.text

    def __str__(self):
        return "Document  : " + self.title
    
    def __repr__(self):
        return self.title

    def sumup(self,ratio): #****
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
    
    def getType(self):
        pass
  
     
    def clean_text(self):
        docText = self.get_text()
        #supprimer les commentaire:
        p = re.compile(r'\([^)]*\)')
        cleanedText = re.sub(p, ' ', docText)

        #charger chaque phrase dans une list 
        p = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
        cleanedText = p.findall(cleanedText)
  
        eap_clean = [] 
        for i in range(len(cleanedText)):
            cleanedText[i] = cleanedText[i].replace('-',' ')
            cleanedText[i] = cleanedText[i].replace('.',' ') # pour ne pas supprimer information.
            cleanedText[i] = cleanedText[i].lower()
            cleanedText[i] = cleanedText[i].split() #liste de sous liste contenant les mots spliter
            for w in cleanedText[i]:
                if w not in stopwords and w.isalpha() :
                    eap_clean.append(w)
        return eap_clean  #retourne une list des mots filtré pour le document
    

    #fonction qui affiche les occurences d'un mot dans un document
    def word_occurence(self):
        
        words_dico=dict()
        #text = expr.split(text)
        documentText2 = self.clean_text()
        for word in documentText2: # Récupération de chaque nouveau mot
            if word not in words_dico:
                
                words_dico[word]=1
            else: # Pour chaque mot déjà listé : ajouter 1 si on le retrouve
                words_dico[word]=words_dico[word]+1
  
        return words_dico
    
        
                
        
    
# classe fille permettant de modéliser un Document Reddit
#

class RedditDocument(Document):
    
    def __init__(self, date, title, author, text, url, num_comments):        
        Document.__init__(self, date, title, author, text, url) #constructeur de la classe mere
        # ou : super(...)
        self.num_comments = num_comments
        self.source = "Reddit"  #variable atypique
        
    def get_num_comments(self):
        return self.num_comments

    def getType(self):
        return "reddit"
    
    def __str__(self):
        #return(super().__str__(self) + " [" + self.num_comments + " commentaires]")
        return Document.__str__(self) + " [" + str(self.num_comments) + " commentaires]"
    
#
# classe fille permettant de modéliser un Document Arxiv
#
#possede plusieures auteurs -> coauteurs
class ArxivDocument(Document):
    
    def __init__(self, date, title, author, text, url, coauteurs):
        #datet = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        Document.__init__(self, date, title, author, text, url)
        self.coauteurs = coauteurs
    
    def get_num_coauteurs(self):
        if self.coauteurs is None:
            return(0)
        return(len(self.coauteurs) - 1) #-1: exclure l'auteur lui meme

    def get_coauteurs(self):
        if self.coauteurs is None:
            return([])
        return(self.coauteurs) #retourne la liste des coauteurs
        
    def getType(self):
        return "arxiv"

    def __str__(self):
        s = Document.__str__(self)
        if self.get_num_coauteurs() > 0:
            return s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
        return s
    
################################## class  Corpus ##################################
class Corpus():
    
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
            
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
            
    
#doc = corpus.get_coll() 
#doc[0]
#doc[o].getText        
      
################################## Création du Corpus ##################################

corpus = Corpus("Corona")

reddit = praw.Reddit(client_id='0AlqCfHuOc5Hkg', client_secret='80PspjYMdTvF91ti9qZeWzAS2BU', user_agent='Reddit Irambique')
hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet, post.title,  post.author_fullname,  txt,  post.url)
    corpus.add_doc(doc)


url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet, i['title'], author, txt, i['id'] )
    corpus.add_doc(doc)

print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))

doc1 = corpus.get_doc(0)
print(doc1.get_text())

print("\n------------- Document apres pretraitement------------- \n")
clean= doc1.clean_text()
print(clean)


print('\n------- occurence des mots dans le documents -----------\n')
occurence = doc1.word_occurence()
print(occurence)


print("Enregistrement du corpus sur le disque...")
corpus.save("Corona.crp")

