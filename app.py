import streamlit as st
from gensim.summarization import summarize

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
#spacy.load('en')
#spacy.load('en_core_web_sm')
# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

# Function for Sumy Summarization
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

    # Fetch Text From Url
#@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


#@st.cache(allow_output_mutation=True)
def analyze_text(text):
    return nlp(text)

def main():
    """Summaryzer Streamlit App""" 

    st.title("Natural Language Processing (NLP)") #main header that will appear every page
    activities = ["About","Summarize","NER Checker","NER For URL"]
    choice = st.sidebar.selectbox("Select Activity",activities)



    if choice == 'Summarize':
        st.subheader("Summarize Document")
        raw_text = st.text_area("Enter Text Here","Type Here")
        summarizer_type = st.selectbox("Summarizer Type",["Gensim","Sumy Lex Rank"])     
        if st.button("Summarize"):
            if summarizer_type == "Gensim":
                summary_result = summarize(raw_text)
            elif summarizer_type == "Sumy Lex Rank":
                summary_result = sumy_summarizer(raw_text)

            st.write(summary_result)

    

    if choice == 'NER Checker':
        st.subheader("Named-Entity Recognition Checker")
        raw_text = st.text_area("Enter Text Here","Type Here")
        if st.button("Analyze"):
            docx = analyze_text(raw_text)
            html = displacy.render(docx,style="ent")
            html = html.replace("\n\n","\n")
            st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)



    if choice == 'NER For URL':
        st.subheader("Summary & NER from URL")
        raw_url = st.text_input("Enter URL Here","Type here")
        text_preview_length = st.slider("Length to Preview",50,100)
        if st.button("Analyze"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result)/text_preview_length)
                st.success("Length of Full Text : {}".format(len_of_full_text))
                st.success("Length of Short Text : {}".format(len_of_short_text))
                st.info(result[:len_of_short_text])
                summarized_docx = sumy_summarizer(result)
                docx = analyze_text(summarized_docx)
                html = displacy.render(docx,style="ent")
                html = html.replace("\n\n","\n")
                st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


    if choice == 'About':
        st.text("This is a NLP web app to help you summarize your essays by text & identify NER by text and URL")
        st.info("For the summary feature there are two ***SUMMARIZER TYPES*** to choose from which is GENSIM and LEXRANK. ")
        st.info("Gensim : This is a module that can automatically summarizes the given text, by extracting one or more important sentences from the text. In a similar way, it can also extract keywords. Gensim’s summarization only works for English for now, because the text is pre-processed so that stopwords are removed and the words are stemmed, and these processes are language-dependent.")
        st.info("LexRank : Is an unsupervised graph based approach for automatic text summarization. The scoring of sentences is done using the graph method. LexRank is used for computing sentence importance based on the concept of eigenvector centrality in a graph representation of sentences")





    
                
if __name__ == '__main__':
    main()
