from nltk import word_tokenize, pos_tag
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()

def filter_candidates(pairs):
    """Filters words by parts of speech (nouns and adjectives)."""
    return [pair[0] for pair in pairs if pair[1] in ['NN', 'JJ']]

def extract_bigram(words):
    """Extracts bigrams with the highest PMI."""
    finder = BigramCollocationFinder.from_words(words)
    return finder.nbest(bigram_measures.pmi, 10)  

def extract_trigram(words):
    """Extracts trigrams with the highest PMI."""
    finder = TrigramCollocationFinder.from_words(words)
    return finder.nbest(trigram_measures.pmi, 10) 

def extract_keywords_tfidf(text, num_keywords=5):
    """Extracts top TF-IDF keywords."""
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = X.toarray()[0]
    keywords = sorted(zip(scores, feature_names), reverse=True)[:num_keywords]
    return [keyword[1] for keyword in keywords]

def extract_keywords(para: str, num_tfidf_keywords=5):
    """Combines TF-IDF keywords with related bigrams and trigrams from NLTK."""

    words = word_tokenize(para)
    tagged_words = pos_tag(words)
    filtered_words = filter_candidates(tagged_words)
    
    bigrams = extract_bigram(filtered_words)
    trigrams = extract_trigram(filtered_words)
    
    tfidf_keywords = extract_keywords_tfidf(para, num_keywords=num_tfidf_keywords)
    
    combined_keywords = set(tfidf_keywords)
    
    for bigram in bigrams:
        bigram_phrase = " ".join(bigram)
        for keyword in tfidf_keywords:
            if keyword in bigram_phrase:
                combined_keywords.add(bigram_phrase)
    
    for trigram in trigrams:
        trigram_phrase = " ".join(trigram)
        for keyword in tfidf_keywords:
            if keyword in trigram_phrase:
                combined_keywords.add(trigram_phrase)
    
    return list(combined_keywords)

if __name__ == "__main__":

    para1 = r"Happiness is a profound and universal emotion that stems from a sense of contentment, fulfillment, and joy. It often arises from meaningful connections with others, personal achievements, or moments of gratitude for life's simple pleasures. While fleeting bursts of happiness may be triggered by external events, lasting happiness often requires an intentional focus on positive habits, self-awareness, and resilience in the face of challenges. It is both an emotional state and a mindset, shaped by our choices, attitudes, and perspectives. Ultimately, happiness is not just a destination but a journey of appreciating the present while striving for a life of purpose and balance."
    para2 = r"Cloudburst tablecloth jumble fleeting cactus umbrella diagonal reverie octopus candlestick porous zephyr juxtapose yonder kaleidoscope indigo cryptic marmalade flotsam quasar accordion plumage labyrinthine sapphire dithering inconsequential vortex jubilant effervescent oscillate."
    para3 = r"Manmohan Singh, an economist and politician, served as the 13th Prime Minister of India from 2004 to 2014. Renowned for his role in the economic reforms of the 1990s, Singh was instrumental in steering the country toward liberalization, fostering economic growth, and enhancing India's global standing. His tenure as Finance Minister in 1991, during a time of economic crisis, marked a pivotal moment in India's transformation, with bold measures such as trade liberalization, reducing government control, and encouraging foreign investment. A man of humility and intellect, Singh's leadership was marked by pragmatism and caution. He is widely respected for his integrity and efforts to balance economic growth with social development. Despite his relatively low-key personality, Manmohan Singh’s impact on India’s economic landscape remains indelible, solidifying his legacy as a key architect of modern India’s economic foundation."
    print(ans := extract_keywords(para1))
    print(ans := extract_keywords(para2))
    print(ans := extract_keywords(para3))