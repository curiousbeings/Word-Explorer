import cv2
import pytesseract
import PyDictionary
import re
from PyDictionary import PyDictionary as pd
import streamlit as st
import numpy as np
import urllib.request
from bs4 import BeautifulSoup

pytesseract.pytesseract.tesseract_cmd = r'' #r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 

#@st.cache(suppress_st_warning=True)
def word_tiles(word):
    dictionary = pd()
    with st.container():
        if st.button(word) or "button_{}".format(word) in st.session_state:
            st.session_state["button_{}".format(word)]=True
            if word not in st.session_state:
               #print(word)
               st.session_state[word]=str(dictionary.meaning(word))
               #print(st.session_state[word])
            st.text(st.session_state[word])
        if st.checkbox("",key="check_{}".format(word)):
            if "check_list" not in st.session_state:
                st.session_state["check_list"]={}
            st.session_state["check_list"][word]=True
        else:
            if "check_list" not in st.session_state:
                st.session_state["check_list"]={}
            st.session_state["check_list"][word]=False
            
                    
def create_playlist(playlist_name):
    if playlist_name not in st.session_state:
        st.session_state[playlist_name] = playlist_name
        return True
    else:
        return False

def save_words(playlist_name,playlist_comment):
    i=0
    with open(r''.format(playlist_name),"a+") as fo:    #Update the upload location where the words are to be saved
        check_list = st.session_state["check_list"]
        fo.seek(0,0)
        if fo.read()=="":
            print("Empty")
            fo.write("000000")
            fo.seek(0,0)
        else:
            fo.seek(0)
            playlist_text=fo.read()
            print("this"+playlist_text[-6:])
            i = int(playlist_text[-6:])

        fo.seek(0,0)
        current_state = fo.read()
        new_state = current_state[0:len(current_state)-6]
        fo.seek(0)
        fo.truncate(0)
        
        new_state += ("\n" + "-"*25 + playlist_comment + "-"*25 + "\n")
        for word in check_list:
            if check_list[word]:
                new_state += (str(i+1)+ ".> " + word+": " + st.session_state[word] + "\n")
                i+=1
            
        new_state += ("-"*(50+len(playlist_comment)) + "\n")
        fo.write(new_state)
        fo.write(f'{i:06}')
        fo.close()
            
@st.cache
def extract_text(uploaded_file):
    ##If file uploaded process it
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()),dtype=np.uint8)
        img = cv2.imdecode(file_bytes,1)
        text = pytesseract.image_to_string(img)
        return text
    return ""
        
def main():
    st.title('OpenCv2 usage')                                                       #Title Name
    uploaded_file = st.file_uploader("Choose an image",["jpg","jpeg","png"])        #upload widget

    converted_text = "Nothing to convert..."

    text = extract_text(uploaded_file)

#Playlist creation/deletion form
    playlist_form = st.form("Playlist")
    playlist_name = playlist_form.text_input("Playlist Name")
    playlist_comment = playlist_form.text_input("Playlist Comment")
    if playlist_form.form_submit_button("Save"):
        #if create_playlist(playlist_name):
        save_words(playlist_name,playlist_comment)
        playlist_form.text("{} saved!!!".format(playlist_name))
        st.text(st.session_state["check_list"])
        #else:
            #playlist_form.text("{} already exists....".format(playlist_name))
    
    #img = cv2.imread('C://Users/Rishav Punia/Desktop/circe2.jpg')

    word_list = []
    #print("--------------------------")
    #print(repr(text))
    text = text.replace("-\n","")
    #print("--------------------------")
    #print(repr(text))
    text_words = re.split('\n| ',text)
    for word in text_words:
        new_word = re.sub('[^A-Za-z|*-*]+', '', word)
        
        if len(new_word)>=4:
            word_list.append(new_word)
            #print(new_word+": "+str(dict.meaning(new_word.lower()))+"\n")

    #print(dict.getMeanings())

    #word = input('Enter the word to find the meaning : ')

    fo = open(r'',"r")         #Frequent words list to filter out some easy words
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

if __name__=="__main__":
    main()
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
