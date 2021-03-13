from  typing import List
import nltk
from nltk.stem.snowball import SnowballStemmer
import nltk.tokenize
from nltk.corpus import stopwords
import pycountry


nltk.download("stopwords")
nltk.download('crubadan')

lang_guesser = nltk.classify.textcat.TextCat()

lang_map = {
"EN":"english",
"EN-GB":"english",
"EN-US":"english",
"None":"russian",
"RU":"russian",
"Ru":"russian",
"Russian":"russian",
"ba":"russian",
"be":"russian",
"bel":"russian",
"bg":"russian",
"br":"russian",
"cu":"russian",
"de":"german",
"el":"greek",
"en":"english",
"en-US":"english",
"es":"spanish",
"eu":"russian",
"fr":"french",
"frm":"french",
"ja":"japan",
"kk":"kazakh",
"ko":"korean",
"la":"latin",
"lv":"latvian",
"nl":"dutch",
"pl":"polish",
"pl-PL":"polish",
"pt":"portuguese",
"ro":"romanian",
"ru":"russian",
"ru-RU":"russian",
"rus":"russian",
"sp":"spanish",
"sv":"swedish",
"ua":"russian",
"uk":"russian",
"ukr":"russian",
"русский":"russian"
}

stop_words={
"arabic":set(stopwords.words("arabic")),
"azerbaijani":set(stopwords.words("azerbaijani")),
"danish":set(stopwords.words("danish")),
"dutch":set(stopwords.words("dutch")),
"english":set(stopwords.words("english")),
"finnish":set(stopwords.words("finnish")),
"french":set(stopwords.words("french")),
"german":set(stopwords.words("german")),
"greek":set(stopwords.words("greek")),
"hungarian":set(stopwords.words("hungarian")),
"indonesian":set(stopwords.words("indonesian")),
"italian":set(stopwords.words("italian")),
"kazakh":set(stopwords.words("kazakh")),
"nepali":set(stopwords.words("nepali")),
"norwegian":set(stopwords.words("norwegian")),
"portuguese":set(stopwords.words("portuguese")),
"romanian":set(stopwords.words("romanian")),
"russian":set(stopwords.words("russian")),
"slovene":set(stopwords.words("slovene")),
"spanish":set(stopwords.words("spanish")),
"swedish":set(stopwords.words("swedish")),
"tajik":set(stopwords.words("tajik")),
"turkish":set(stopwords.words("turkish"))
}


tokenizers = set(["czech",
"danish",
"dutch",
"english",
"estonian",
"finnish",
"french",
"german",
"greek",
"italian",
"norwegian",
"polish",
"portuguese",
"russian",
"slovene",
"spanish",
"swedish",
"turkish"])

stemmers ={
    "russian":SnowballStemmer(language="russian"),
    "english":SnowballStemmer(language="english"),
    "ukrainian":SnowballStemmer(language="russian"),
    "bulgarian":SnowballStemmer(language="russian"),
    "french":SnowballStemmer(language="french"),
    "spanish":SnowballStemmer(language="spanish"),
    "german":SnowballStemmer(language="german"),
    "belarussian":SnowballStemmer(language="russian"),
    "italian":SnowballStemmer(language="italian")
}

def remove_punctuation_and_stopwords(words:List,language:str):
    ret = set()
    for i in words:
        if i.isalnum() and i not in stop_words.get(language,"russian"):
            ret.add(i.lower())
    return ret
            

def word_tokenize(text:str, language:str):
    lang = language if language in tokenizers else "english"
    words = nltk.tokenize.word_tokenize(text,language=lang)
    words = remove_punctuation_and_stopwords(words,language)
    stemmer = stemmers.get(lang, stemmers["english"])
    words = set(map(lambda x: stemmer.stem(x),words))
    return words

def guess_language(text):
    lang_guess = lang_guesser.guess_language(text).strip()
    return pycountry.languages.get(alpha_3=lang_guess).name.lower()



