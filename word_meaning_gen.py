import cv2
import pytesseract
import PyDictionary
import re
from PyDictionary import PyDictionary as pd
import streamlit as st
import numpy as np

import urllib.request
from bs4 import BeautifulSoup

pytesseract.pytesseract.tesseract_cmd = r'' #generally C:\\Program Files\\Tesseract-OCR\\tesseract.exe or your tesseract installation location

#@st.cache(suppress_st_warning=True)
def word_tiles(word):
    with st.container():
        if st.button(word):
            if word not in st.session_state:
               #print(word)
               st.session_state[word]=str(dictionary.meaning(word))
               #print(st.session_state[word])
            st.write(st.session_state[word])
                    
st.title('OpenCv2 usage')
uploaded_file = st.file_uploader("Choose an image",["jpg","jpeg","png"])

converted_text = "Nothing to convert..."

text = ""

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()),dtype=np.uint8)
    img = cv2.imdecode(file_bytes,1)
    text = pytesseract.image_to_string(img)

#img = cv2.imread('C://Users/Rishav Punia/Desktop/circe2.jpg')

word_list = []
#print("--------------------------")
#print(repr(text))
text = text.replace("-\n","")
#print("--------------------------")
#print(repr(text))
text_words = re.split('\n| ',text)
for word in text_words:
    new_word = re.sub('[^A-Za-z]+', '', word)
    
    if len(new_word)>=4:
        word_list.append(new_word)
        #print(new_word+": "+str(dict.meaning(new_word.lower()))+"\n")
        


dictionary = pd()

#print(dict.getMeanings())

#word = input('Enter the word to find the meaning : ')

fo = open(r'',"r")    #Location of word filter file
freq_words_list=fo.read().split('\n')

word_reduced_list = []
#print(len(word_list))
for word in word_list:
    if word.lower() not in freq_words_list:
        word_reduced_list.append(word.lower())        

word_reduced_list = list(dict.fromkeys(word_reduced_list).keys())
#print(len(word_reduced_list))
for word in word_reduced_list:
    word_tiles(word)


##
##
##for word in word_reduced_list:
##    if st.button(word):
##        with st.expander("meaning"):
##            st.text(dict.meaning(word))




##for word in word_list:
##    url = "https://www.vocabulary.com/dictionary/" + word + ""
##    htmlfile = urllib.request.urlopen(url)
##    soup = BeautifulSoup(htmlfile, 'lxml')
##
##    soup1 = soup.find(class_="short")
##
##    try:
##        soup1 = soup1.get_text()
##    except AttributeError:
##        print(word+': Cannot find such word! Check spelling.')
##        
##    # Print short meaning
##    if soup1!=None:
##        print ('-' * 25 + '->',word,"<-" + "-" * 25)
##        print ("SHORT MEANING: \n\n",soup1)
##        print ('-' * 65)
##
##    # Print long meaning
##    #else:
##     #   soup2 = soup.find(class_="long")
##      #  soup2 = soup2.get_text()
##       # print ("LONG MEANING: \n\n",soup2)
##
##    #print ('-' * 65)
##
##    # Print instances like Synonyms, Antonyms, etc.
##    #soup3 = soup.find(class_="instances") 
##    #txt = soup3.get_text()
##    #txt1 = txt.rstrip()
##
##    #print (' '.join(txt1.split()))
