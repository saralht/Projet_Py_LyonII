# -*- coding: utf-8 -*-
"""
                        **** PROJET PYTHON M1 INFORMATIQUE ****
                                      (Sujet II)
                                   
                                      Etudiantes:
                                        
                          Fatim-Zahra El Gaouzi, Sara Lehtihet
                                     
"""

######################################################################
#     LIBRAIRIES
######################################################################
from gensim.summarization.summarizer import summarize
from itertools import combinations
from nltk.corpus import stopwords
from pyvis.network import Network
import networkx as nx
import datetime as dt
import urllib.request
import pickle
import re
import praw
import xmltodict
import numpy as np
import pandas as pd



######################################################################
#       Definition des Stop Words
# exemple de stop word: Then, On, With, For, To, you , .....
# https://www.tutorialspoint.com/python_text_processing/python_remove_stopwords.htm
######################################################################
try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    stopwords = set(stopwords.words('english'))
    
    

######################################################################
#     Class Singleton: pour instanciation de la class(creation_corpus)
######################################################################
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
    
######################################################################
#     Class Author (TD2)
######################################################################
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
    
    
######################################################################
#     Class Document (TD2)
######################################################################

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
  
    #--------------------------------------- Code rajouté  ---------------------
     
    """ fonction: prétraitement et nettoyage du texte du doc
            input: le texte du document
           output: liste des mots pertinent du document après traitement"""
    def clean_text(self):
        docText = self.get_text()
        #supprimer les commentaire: en utilisant les expressions régulieres
        p = re.compile(r'\([^)]*\)')
        cleanedText = re.sub(p, ' ', docText)
        
        #charger chaque phrase dans une liste: 
            #la phrase commence par une Maj et se termine par un .
        p = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
        cleanedText = p.findall(cleanedText)
        
        eap_clean = [] 
        for i in range(len(cleanedText)):
            # remplacer les - par des espaces pour ne pas suprimer par exemple covid-19 pour pouvoir supprimer le chiffre 19 sans supp covid
            cleanedText[i] = cleanedText[i].replace('-',' ') 
            # replacer . par un espace pour ne pas supprimer ( information.) lors de la suppression des signes de poncuations
            cleanedText[i] = cleanedText[i].replace('.',' ') 
            # mettre tout en miniscule
            cleanedText[i] = cleanedText[i].lower()
            # Split des mots sous forme de liste
            cleanedText[i] = cleanedText[i].split() 
            
            #suppression des stopwords et des signes de poncuation restantes
            #isalpha : pour suppimer les chiffres
            for w in cleanedText[i]:
                if w not in stopwords and w.isalpha() :
                    eap_clean.append(w)
        return eap_clean  #retourne une list des mots filtré pour le document
    
    
    
    


    """ fonction word_occurence: cree un dictionnaire des cooccurences pour chaque mots du doc
            input: le texte nettoyé du document
           output: dictionnaire mot:nbr_cooccurence """
    def word_occurence(self):
        words_dico=dict()
        documentText2 = self.clean_text()
        for word in documentText2: 
            if word not in words_dico:
                words_dico[word]=1
            else: # Pour chaque mot déjà listé : ajouter 1 si on le retrouve
                words_dico[word]=words_dico[word]+1
        return words_dico
        
    
    
    
    
    

    """ fonction seach_word: qui teste si le mot recherché donc le doc existe 
            input: le texte nettoyé du document & le mot a chercher 
           output: un message """     
    def seach_word(self,word):
        doc = self.word_occurence()
        if word in doc:
            print("Le mot %s a ete trouve dans le document %s "% (word, self.get_title()))
        else:
            print("Attention: le mot %s n existe pas dans le document: %s"% (word,self.get_title()))
     




    """ fonction doc_to_sentence: fonction qui decoupe le text du doc en phrase
            la phrase contient 6 mots
            si nbr de mots % 6 <> 0, il integre les mots restant dans une phrase(sous-liste)"""  
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
                j = j + 1
            newListe.append(listeInter.copy())
        listeInter=[]
        for i in range(j,j+nbRestMot):
            listeInter.append(liste[j])
            j = j + 1
        newListe.append(listeInter)
        print('----------------Document décomposé en Fenetre----------------\n',newListe)
        return newListe
        
    # declaration de la variables global 
    global G 
    
    
    
    
    """ fonction cooccurence_matrix: retourne la matrice de cooccurence
                input: list des mots du doc sans doublons & liste des fenetres(6 mots)
                output: Matrice de cooccurence""" 
    def cooccurence_matrix(self):
        cleanDoc = self.clean_text()  
        #document contenant les mots sans doublons (wordWithoutRep)
        wordWithoutRep = []
        wordWithoutRep = list(set(cleanDoc))
        #decouper le doc en fenetre de 6 mots
        doc2sentence = self.doc_to_sentence(cleanDoc)
        # creation de la matrice de cooccurence
        G = nx.MultiGraph()
        G = nx.from_edgelist((c for n_nodes in doc2sentence for c in combinations(n_nodes, r=2)),create_using=nx.MultiGraph)
        res = nx.to_pandas_adjacency(G, nodelist=wordWithoutRep, dtype='int')
        # renvertir la matrice en tableau
        res = np.array(res)
        return res





    """ fonction centrality: fonction qui calcule la centralité 
                input: list des mots du document
                output: lists des mots avec un degré de centalité important""" 
    def centrality(self):
        cleanDoc = self.clean_text() 
        doc2sentence = self.doc_to_sentence(cleanDoc)
        G = nx.MultiGraph()
        G = nx.from_edgelist((c for n_nodes in doc2sentence for c in combinations(n_nodes, r=2)),create_using=nx.MultiGraph)
        degree = G.degree()

        #--------------- calcule d'indicateur 1 de centralité de degré------------------
        # liste des noeuds ayant un degre max
        nodes_max =[]
        dictDegree = dict(degree)
        #rechercher le sommet de degres max
        degre_max = max(dictDegree.values()); {value for key, value in dictDegree.items() if value == degre_max}
    
        for k in dictDegree:
            if (dictDegree[k]==degre_max):
                nodes_max.append(k)
        #print("node maxxxxxxxx",nodes_max)
       
        #--------------indicateur 2: centralité de proximité ------------
        sommets_centralite_max = []
        centralite = nx.closeness_centrality(G)
        centralite_ind = list(centralite.keys())
        centralite_val = list(centralite.values())
       
        maximum = max(centralite_val)
        maximum = float(maximum)
     
        for i in range(len(G.nodes)):
            if centralite_val[i]==maximum:
                sommets_centralite_max.append(centralite_ind[i])
        #print("teeeeeeeeeeeeeesetttttttttteee",sommets_centralite_max) 
    
        #----------concatenation des deux resultats de centralite en une seule liste-------
        final_centralilte = []
        final_centralilte.extend(nodes_max)
        final_centralilte.extend(sommets_centralite_max)
        #s'assurer de suprimmer les doublons
        final_centralilte = list(set(final_centralilte))
        print('------Liste des mots avec des degré de centralité élevé---\n',final_centralilte)
        return final_centralilte 
           
    
    
    
    """ fonction draw_graph: fonction qui affiche le graph dans le browser
                input: matric de cooccurence
                output: fichier.html contenant le graphe
                Note: Nous nous sommes inspiré de la documentation Pyvis :
              https://buildmedia.readthedocs.org/media/pdf/pyvis/latest/pyvis.pdf""" 
    def draw_graph(self):
        cleanDoc = self.clean_text() # renvois la liste 
        wordWithoutRep = []
        wordWithoutRep = list(set(cleanDoc))
        #recup la matrice
        matrix = self.cooccurence_matrix()
        sources_nodes = []
        targets_nodes = []
        weights = []
        #recuperation des noeuds sources, destinations et des poids
        for i in range(len(wordWithoutRep)):  
            for j in range(len(wordWithoutRep)):
                if ((i != j) & (matrix[i,j]>0)):
                    sources_nodes = sources_nodes + [wordWithoutRep[i]]
                    targets_nodes = targets_nodes + [wordWithoutRep[j]]
                    weights = weights + [float(matrix[i, j])]
       
        
        #on crée des séries de données au format "pandas"
        sources = pd.Series(sources_nodes)
        targets = pd.Series(targets_nodes)
        weights = pd.Series(weights)
        
        net = Network(height="750px", width="100%", bgcolor="#bedbbb", font_color="#2c061f", notebook=True)
        # options pour changer la police du graphe
        options = {
            "nodes": {
                "size": 20
                },
         }
        # set the physics layout of the network
        net.barnes_hut()
        edge_data = zip(sources, targets, weights)
        # recuprer la liste des mots de degree centralité de degré important
        centralNode = self.centrality()
        for e in edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]
            #changer la couleur des noeuds inclus dans centralNode(orange)
            if src in centralNode:
                
                 net.add_node(src ,dst, title=src,  color='#f37121')
                 net.add_node(dst, dst, title=dst,  color='#f37121')
                 #label : pour ajouter les poids 
                 net.add_edge(src, dst, label=w, color='red' )
            else:
                net.add_node(src, src, title=src,  color='#30475e')
                net.add_node(dst, dst, title=dst,  color='#30475e')
                #label : pour ajouter les poids 
                net.add_edge(src, dst, label=w, color='#92817a' )
           
        #neighbor : liste des voisins du sommet i
        neighbor_map = net.get_adj_list()
 
        for node in net.nodes:
            node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
            node["value"] = len(neighbor_map[node["id"]])
    
        net.options = options
        net.show("graph.html")
        
        
    
        
                

######################################################################
#     classe fille permettant de modéliser un Document Reddit
######################################################################

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
        return Document.__str__(self) + " [" + str(self.num_comments) + " commentaires]"
    


######################################################################
# classe fille permettant de modéliser un Document Arxiv
#possede plusieures auteurs -> coauteurs
######################################################################

class ArxivDocument(Document):
    
    def __init__(self, date, title, author, text, url, coauteurs):
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
    

    

######################################################################
#     Class Corpus
######################################################################

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
            
            

    """ fonction docsIncludingW:   chercher dans le corpus les doc qui contiennent word
                input: collocation du corpus
                output: lists des titres des documents qui contiennet le mot cherché """
    # focntion qui liste les documents où le mot recherché a été trouvé (nous l'utilisons pour remplir le combobox de l'interface)
    def docsIncludingW(self,word):
        corp = self.get_coll()
        titlesOfdocs = dict()
        # appeler le document pretraité
        for key, val in corp.items():
            doc = corpus.get_doc(key)
            doc = doc.clean_text()
            if word in doc:     
                titlesOfdocs[key] = corp[key].get_title()
        return titlesOfdocs # renvoie une liste des titres des documents trouvés
                
        
        
            
   
      

######################################################################
#     Class Creation_corpus
#    Héritage:
#       class mere : corpus
#       class fille : creation_corpus
#      utilisation du singleton pour l'unicité de la class
######################################################################

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

#######################################################################
# Ici nous avons proceder a ces teste pour valider l'implementation avant de passer
# a l'interface 
# ce script ne devait pas etre executable ( enlever toute la partie main )
##########################################################################

if __name__ == "__main__":
    
    print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))

    doc1 = corpus.get_doc(0)
    print(doc1.get_text())

    print("\n------------- Document apres pretraitement------------- \n")
    clean= doc1.clean_text()
    print(clean)

    #print('\n------- occurence des mots dans le documents -----------\n')
    #occurence = doc1.word_occurence()
    #print(occurence)
    print("\n------------- Matrice de Cooccurence------------- \n")
    print(doc1.cooccurence_matrix())

    searchw = doc1.seach_word("covid")
    print(searchw)

    print("---------soucrces---------\n",doc1.draw_graph())

    print(corpus.docsIncludingW("ratio"))
    
    print("Enregistrement du corpus sur le disque...")
    corpus.save("Corona.crp")
