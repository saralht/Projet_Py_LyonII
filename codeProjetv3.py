# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:16:56 2020

@author: HP LEHTIHET
"""

from nltk.corpus import stopwords
import datetime as dt
from gensim.summarization.summarizer import summarize
import pickle
import re
import praw
import urllib.request
import xmltodict
import networkx as nx
import numpy as np
import pandas as pd
from pyvis.network import Network
from itertools import combinations



 
try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    stopwords = set(stopwords.words('english'))
    

    
########################## CREATION du singleton ##################################

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
    
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
  
    #--------------------------------------- here ---------------------
     
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
        
    
    #chercher un mot dans un doc et afficher tout les autres mots      
    def seach_word(self,word):
        doc = self.word_occurence()
        if word in doc:
            print("Le mot %s a ete trouve dans le document %s " % (word, self.get_title()))
            #return doc
        else:
            print("Attention: le mot %s n existe pas dans le document: %s"% (word,self.get_title()))
        #print(resultat) 
        
    #fonction qui decoupe le text du doc en phrase
    #la phrase contient 6 mots
    #il prend les mots restants < 6 sont integrer dans une phrase
    def doc_to_sentence(self,liste):
        taille=len(liste)
        nbMot6=taille//6
        nbRestMot=taille%6
    
        j=0
        newListe=[]
        listeInter=[]
        for i in range(0, nbMot6):
            listeInter.clear()
            
            for k in range(0, 6):
                listeInter.append(liste[j])
                j=j+1
            newListe.append(listeInter.copy())
        listeInter=[]
        for i in range(j,j+nbRestMot):
            listeInter.append(liste[j])
            j=j+1
        newListe.append(listeInter)
        return newListe
        
    # declaration de la variables global 
    global G 
    
     # matrice de co occurence
    def cooccurence_matrix(self):
        cleanDoc = self.clean_text() # renvois la liste 
        #document contenant les mots sans doublant
        wordWithoutRep = []
        wordWithoutRep = list(set(cleanDoc))
        #print("-----------names----------\n",wordWithoutRep)
        
        #decouper le doc en phrase
        doc2sentence = self.doc_to_sentence(cleanDoc)
    
        #print("----------------------sentence------------\n",doc2sentence)
        G = nx.MultiGraph()
        G = nx.from_edgelist((c for n_nodes in doc2sentence for c in combinations(n_nodes, r=2)),create_using=nx.MultiGraph)
        res = nx.to_pandas_adjacency(G, nodelist=wordWithoutRep, dtype='int')
        #print("---------------co occurrence matrix --------------\n")
        #print(res)
        #convert list into matrix in ordor to use it in drawing the graph
        res = np.array(res)
        return res


    def centralite(self):
        cleanDoc = self.clean_text() 
        doc2sentence = self.doc_to_sentence(cleanDoc)
        G = nx.MultiGraph()
        G = nx.from_edgelist((c for n_nodes in doc2sentence for c in combinations(n_nodes, r=2)),create_using=nx.MultiGraph)
        degree = G.degree()
        
        """
        pas besoin
        degre_max = max(np.array(G.degree())[:,1]) # [:,1] prendre que les values
        print("\n\n")
        print(np.array(G.degree()))
        # convertir la valeur degre_max qui est un str en int
        degre_max = int(degre_max)"""
      
        #centralité de degré
        # liste des noeuds ayant un degre max
        nodes_max =[]
        dictDegree = dict(degree)
        print(dictDegree)

        #rechercher le sommet de degres max
        degre_max = max(dictDegree.values()); {value for key, value in dictDegree.items() if value == degre_max}
    
        for k in dictDegree:
            if (dictDegree[k]==degre_max):
                nodes_max.append(k)
        print("node maxxxxxxxx",nodes_max)
       
        """
        # indicateur de centralité  de degrée
        # donne le meme resultat de la premiere
        sommets_centralite_max = []
        centralite = nx.degree_centrality(G)
        centralite_ind = list(centralite.keys()) #covid
        centralite_val = list(centralite.values()) #8
        print("vaaaaaaaaaaaaaaaaaaaaaaaaaal",centralite_val)
        maximum = max(centralite_val)
        maximum = float(maximum)
        print(maximum)
        for i in range(len(G.nodes)):
            if centralite_val[i]==maximum:
                sommets_centralite_max.append(centralite_ind[i])
        print("teeeeeeeeeeeeeesetttttttttteee",sommets_centralite_max) """
        
        #indicateur centralité de proximité 
        sommets_centralite_max = []
        centralite = nx.closeness_centrality(G)
        centralite_ind = list(centralite.keys())
        centralite_val = list(centralite.values())
       
        maximum = max(centralite_val)
        maximum = float(maximum)
        print(maximum)
        for i in range(len(G.nodes)):
            if centralite_val[i]==maximum:
                sommets_centralite_max.append(centralite_ind[i])
        #print("teeeeeeeeeeeeeesetttttttttteee",sommets_centralite_max) 
    
        #concatenation des deux resultats de centralite en une seule liste
        final_centralilte = []
        final_centralilte.extend(nodes_max)
        final_centralilte.extend(sommets_centralite_max)
        #s'assurer de suprimmer les doublons
        final_centralilte = list(set(final_centralilte))
        #print('fffffffinal',final_centralilte)
        return final_centralilte 
           
    def draw_graph(self):
        cleanDoc = self.clean_text() # renvois la liste 
        wordWithoutRep = []
        wordWithoutRep = list(set(cleanDoc))
        #recup la matrice
        matrix = self.cooccurence_matrix()
        sources_nodes = []
        targets_nodes = []
        weights = []
        for i in range(len(wordWithoutRep)): # a changer 
            for j in range(len(wordWithoutRep)):
                if ((i != j) & (matrix[i,j]>0)):
                    sources_nodes = sources_nodes + [wordWithoutRep[i]]
                    #sources_nodes = list(set(sources_nodes))
                    targets_nodes = targets_nodes + [wordWithoutRep[j]]
                    #targets_nodes = list(set(targets_nodes))
                    weights = weights + [float(matrix[i, j])]
        #print("-------sources---\t\n",sources_nodes)
        #print("--------aretes------\t\n", weights)
        
        #on crée des séries de données au format "pandas"
        sources = pd.Series(sources_nodes)
        targets = pd.Series(targets_nodes)
        weights = pd.Series(weights)
        net = Network(height="400px", width="100%", bgcolor="#222222", font_color="white", notebook=True)

        # set the physics layout of the network
        net.barnes_hut()
        edge_data = zip(sources, targets, weights)

        for e in edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]
            net.add_node(src, src, title=src)
            net.add_node(dst, dst, title=dst)
            net.add_edge(src, dst, value=w)
        
      
        neighbor_map = net.get_adj_list()
        #bet=nx.betweenness_centrality(G)
        #add neighbor data to node hover data
        #neighbor : liste des voisins du sommet i
        for node in net.nodes:
            #node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
            node["value"] = len(neighbor_map[node["id"]])

        """#change color of central node
        centralNode = self.centralite()
        
        G.nodes[1]['title'] = 'Number 1'
        G.nodes[1]['group'] = 1
        
        G.nodes[3]['title'] = 'I belong to a different group!'
        G.nodes[3]['group'] = 10
        
        G.add_node(20, size=20, title='couple', group=2)
        G.add_node(21, size=15, title='couple', group=2)
       
       
        net = Network("500px", "500px")
        # populates the nodes and edges data structures
        net.from_nx(G)
        net.show("nx.html")"""
        
      
        """ a faire : coloration des noeuds 
        matrix = nx.from_numpy_matrix(matrix, create_using=nx.MultiDiGraph())
        centralNode = nx.MultiDiGraph()  # changed the graph type to MultiDiGraph
        for n in net.nodes:
            if n in centralNode:  # if the node is part of the sub-graph
                color="red"
       
            net.add_node(n, label=n, color=color)"""
        
        #net.show_buttons(filter_=['physics'])  
        net.show("graph.html")
        
        
    
        
                
# classe fille permettant de modéliser un Document Reddit

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
            
            
    ###############################################################################
    #                 chercher dans le corpus les doc qui contiennent word
    ###############################################################################
    # focntion qui liste les documents ou le mot a été trouvé
    def docsIncludingW(self,word):
        corp = self.get_coll()
        
        titlesOfdocs = dict()
        
        # appeler le document pretraiter
        for key, val in corp.items():
            doc = corpus.get_doc(key)
            doc = doc.clean_text()
            if word in doc:     
                #titlesOfdocs.append(corp[key].get_title())
                titlesOfdocs[key] = corp[key].get_title()
        return titlesOfdocs
                
        
        
            
    
#doc = corpus.get_coll() 
#doc[0]
#doc[o].getText        
      
################################## Création du Corpus ##################################
# classe mere : corpus
#classe fille : creation_corpus
class Creation_corpus(Corpus,metaclass=Singleton): 
     
    def __init__(self):
        super()
    
    def create(self):
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
    
        return corpus
    
    
c = Creation_corpus()
corpus = c.create()        

if __name__ == "__main__":
    
    print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))

    doc1 = corpus.get_doc(199)
    print(doc1.get_text())

    print("\n------------- Document apres pretraitement------------- \n")
    clean= doc1.clean_text()
    print(clean)


    """print('\n------- occurence des mots dans le documents -----------\n')
    occurence = doc1.word_occurence()
    print(occurence)"""


    print(doc1.cooccurence_matrix())

    searchw = doc1.seach_word("covid")
    print(searchw)

    print("---------soucrces---------\n",doc1.draw_graph())
    #print("------------centralite\n",doc1.centralite())

    print("Enregistrement du corpus sur le disque...")
    corpus.save("Corona.crp")

    print(corpus.docsIncludingW("ratio"))
