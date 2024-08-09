import re
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def remove_unwanted_text(content):
        content = re.sub('@[^\s]+', '', content)  # Remove Twitter handles
        content = re.sub('http[^\s]+', '', content)  # Remove URLs
        content = re.sub('www[^\s]+', '', content)  # Remove URLs
        content = re.sub('#[^\s]+', '', content)  # Remove hashtags
        content = re.sub('&[^\s]+', '', content)  # Remove HTML entities
        content = re.sub('rt', '', content)  # Remove HTML entities
        return content

def remove_punctuations(text):
    return re.sub('[^A-Za-z ]+', '', text)

def remove_stop_words(text):
    sw = stopwords.words("english")  # English Stop Words
    # Remove punctuation from stopwords to ensure uniform comparison
    sw = [remove_punctuations(s) for s in sw]
    word_list = text.split()
    return ' '.join([word for word in word_list if word.lower() not in sw])

def stem_words(text):
    stemmer = PorterStemmer()
    word_list = text.split()
    return ' '.join([stemmer.stem(word) for word in word_list])

def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    word_list = text.split()
    return ' '.join([lemmatizer.lemmatize(word) for word in word_list])

def clean_data(content):
    content = content.lower()  # Convert to lower case
    content = remove_unwanted_text(content)  # Remove unwanted text like URLs, handles, etc.
    content = remove_punctuations(content)  # Remove punctuation
    content = remove_stop_words(content)  # Remove stopwords
    content = lemmatize_words(content)  # Lemmatize the words
    return content
    
