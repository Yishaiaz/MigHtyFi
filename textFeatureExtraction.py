# Load library
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from profanity_check import predict, predict_prob
from spellchecker import SpellChecker

class TextFeatureExtractor:


    def not_number(self,word):
        '''
        checks if there is a number in the string
        :param word: a string
        :return: true if no number inside else false
        '''
        for i in range(1,10):
            if str(i) in word:
                return False
        return True


    def removeStopWords(self,tokens):
        '''
        removes stopWords, single leter words and numbers
        :param tokens: the tokens
        :return: a clean token list
        '''
        stop_words = stopwords.words('english')
        return [word for word in tokens if word not in stop_words and len(word) > 1 and self.not_number(word)]




    def getWordFreaquency(self,tokens):
        '''
        counts the accurances of words
        :param tokens: list of tokens
        :return: a dictianary: key = token, value=accurances
        '''
        dic = dict()
        for token in tokens:
            if token not in dic:
                dic[token] = 1
            else:
                dic[token] = dic[token] + 1

        return dic


    def feature_most_freaquent(self,dictianery,total_word_count):
        '''
        feature: the most frequen
        :param dictianery:
        :param total_word_count:
        :return:
        '''
        max_value = 0;
        max_key = ""
        for word in dictianery:
            if max_value < dictianery[word]:
                max_value = dictianery[word]
                max_key = word

        return max_value/total_word_count


    def feature_repettive(self,tokens):
        '''
        this feature checks ratio of the word usage within all the words in the song
        :param tokens: a list of tokens
        :return: the feature value
        '''
        total_size = len(tokens)
        unique_size = len(set(tokens))
        return unique_size/total_size





    def correctSpellCheck(self,sentences,lyrics):
        '''
        will spell check and corect the given lyrics
        :param sentences: a list of sentences
        :param lyrics: all of the text combined as a string
        :return: a list of corrected sentences
        '''
        spell = SpellChecker()
        spellchecker = dict()
        misspelled = list(set(spell.unknown(word_tokenize(lyrics))))
        for word in misspelled:
            spellchecker[word] = spell.correction(word)

        for j in range(len(sentences)):
            words = word_tokenize(sentences[j].lower())
            for i in range(len(words)):

                if words[i] in spellchecker:
                    words[i] = spellchecker[words[i]]

            fixed_sentence = ""
            for word in words:
                fixed_sentence +=  word + " "
            sentences[j] = fixed_sentence[:-1]
        return sentences;



    def feature_offensive(self,lyrics):
        '''
        the feature check how offensive the lyrics are ( (total number og ofensive sentences)/(total number of sentences) )
        :param lyrics: the lyrics string
        :return: the feature value
        '''
        sentences = lyrics.split('\n')
        sentences = list(filter(lambda x: x is not None and x!= '' and len(x) >= 1, sentences))
        sentence_count = len(sentences)
        sentences = self.correctSpellCheck(sentences, lyrics)
        offensive_count = 0

        for sentence in sentences:
            prob = predict_prob([sentence])
            if prob >= 0.3:
                offensive_count += 1

        return offensive_count/sentence_count

    def feature_slang(self,lyrics,tokens):
        '''
        this feature check the ration between the mispelled words in the song to all the words in the song
        :param lyrics: lyrics string
        :param tokens: list of tokens
        :return: the features value
        '''
        spell = SpellChecker()
        word_tokenize(lyrics)
        misspelled = spell.unknown(tokens)
        return 1 - len(set(misspelled))/len(set(tokens))



    def extract(self,lyrics):
        '''
        the Main inteface for this class:
        given lyrics, it will generate the 4 features:
        [most_frequent, repetetive, offensive, speelCheck]
        :param lyrics: string of the lyrics
        :return: a dictionary with all the featers
        '''
        if not lyrics:
            return {"most Freq": None, "repetitive": None, "offensive": None, "spellScheck": None}
        lyrics = lyrics.replace("\'s", '')
        lyrics = lyrics.replace("\'", '')

        tokens = word_tokenize(lyrics.lower())
        tokens = self.removeStopWords(tokens)
        total_word_count = len(tokens)

        dictionary = self.getWordFreaquency(tokens)

        feature1 = self.feature_most_freaquent(dictionary,total_word_count)
        feature2 = self.feature_repettive(tokens)
        feature3 = self.feature_offensive(lyrics)
        feature4 = self.feature_slang(lyrics,tokens)

        return {"most Freq" : feature1, "repetitive" : feature2, "offensive" : feature3, "spellScheck" : feature4}
