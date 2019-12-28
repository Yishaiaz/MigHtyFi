# Load library
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from profanity_check import predict, predict_prob
from spellchecker import SpellChecker


#
# my_sent = "Fuck\nI ain't got no motherfuckin' friends\nThat's why I fucked yo' bitch, you fat motherfucker\n(Take money) West side!\nBad Boy killers\n(Take money) You know the realest is niggaz\n(Take money) We bring it to you\n(Take money)\n\nTupac:\nFirst off, fuck your bitch and the clique you claim\nWest side when we ride come equipped with game\nYou claim to be a player but I fucked your wife\nWe bust on Bad Boy niggaz fuck for life\nPlus Puffy tryin' ta see me weak, hearts I rip\nBiggie Smallz and Junior M.A.F.I.A. some mark ass bitches\nWe keep on comin' while we runnin' for ya jewels\nSteady gunnin', keep on bustin' at the fools, you know the rules\nLittle Ceaser, go ask ya homie how I leave ya\nCut your young ass up, leave you in pieces, now be deceased\nLil Kim, don't fuck around with real G's\nQuick to snatch yo' ugly ass off tha street, so fuck peace\nI let them niggas know it's on for life\nSo let the West side ride tonight hahahah\nBad Boy murdered on wax, and killed\nFuck wit' me and get yo caps peeled, you know... see...\n\nGrab ya Glocks, when you see Tupac\nCall the cops, when you see Tupac, uh\nWho shot me, but ya punks didn't finish\nNow ya bout to feel the wrath of a menace\nNIGGA, I hit em' up...\n\nTupac:\nCheck this out, you muthafuckas know what time it is\nI don't even know why I'm on this track\nY'all niggaz ain't even on my level\nI'ma let my little homies ride on you\nBitch made-ass bad boy bitches, feel it!\n\nFatal:\nGet out the way yo, get out the way yo\nBiggie Smallz just got dropped\nLittle Moo, pass the Mac, and let me hit him in his back\nFrank White need to get spanked right, for settin' traps\nLittle accident murderer, and I ain't never heard-a ya\nPoisonous gats attack when I'm servin' ya\nSpank ya shank ya whole style when I gank\nGuard your rank, 'cause I'ma slam you ass in the paint\nPuffy weaker than the fuckin' block I run on you nigga\nAnd I'll smoke ya junior mafia in front of you nigga\nWith the ready power tuckin' my Guess under my Eddie Bauer\nYa clout, pretty sour I get packages every hour\nAnd hit 'em up\n\nGrab ya Glocks, when you see Tupac\nCall the cops, when you see Tupac, uh\nWho shot me, but ya punks didn't finish\nNow ya bout to feel the wrath of a menace\nNigga, we hit em' up...\n\nTupac:\nPeep how we do it, keep it real, it's penitentiary steel\nThis ain't no freestyle battle, all you niggaz gettin'\nKilled with ya mouths open\nTryin' to come up offa me, you in the clouds hoping\nSmokin' dope it's like a sherm high\nNiggaz think they learned to fly\nBut they burn muthafucka, you deserve to die\nTalkin' 'bout you gettin' money, but its funny to me\nAll you niggaz living bummy, why you're fuckin' with me\nI'm a self made millionaire\nThug Livin' out a prison, pistols in the air, hahaha\nBiggie, remember when I used to let you sleep on tha couch\nAnd beg the bitch to let you sleep in the house, ah\nNow it's all about Versace, you copied my style\nFive shots couldn't drop me, I took it, and smiled\nNow I'm bout to set the record straight, with my AK\nI'm still the thug that you love to hate\nMotherfucker, I hit 'em up\n\nKadafi:\nI'm from N-E-W Jerz, where plenty murders occur\nNo point to comment, we bringin' drama to all you herbs\nKnuckle check the scenario, Little Cease\nI bring you fake G's to your knees\nCoppin pleas in de janeiro\nLil Kim, is you coked up, or doped up?\nGet ya lil Junior whopper clique smoked up, what the fuck\nIs you stupid?! I take money, crash and mash through Brooklyn\nWith my clique lootin', shootin' and pollutin' ya block\nWith 15 shots cocked Glock to your knot\nOutlaw mafia clique movin' up another notch\nAnd you bast stops squaws get mopped and dropped\nAll your fake-ass east coast props brainstormed and locked\n\nIdi Amin:\nYou is a, b writer, a Pac style taker\nI'll tell you to ya face you ain't shit but a faker\nSofter than Alizee with a chaser\nBout to get murdered for the paper\nIdi Amin approach the scene of the caper\nLike a loc, with little ceaser in a choke hold\nTotin smoke, we ain't no muthafuckin joke\nThug Life, niggaz betta be known, we approachin'\nIn the wide open, guns smokin'\nNo need for hopin' it's a battle lost, I got 'em crossed\nSoon as the funk is poppin' off\nNigga I hit 'em up\n\nTupac:\nNow you tell me who won\nI see them, they run\nThey don't wanna see us\nWhole Junior M.A.F.I.A. click dressin' up tryin' ta be us\nHow the fuck they gonna be the mob when we always on our job\nWe millionaires, killin' ain't fair but somebody gotta do it\nOh yeah, Mobb Deep, you wanna fuck with us?\nYou little young ass motherfuckers\nDon't one of you niggaz got sickle cell or somethin'?\nYou fuckin' with me nigga you fuck around\nAnd have a seizure or a heart-attack\nYou better back the fuck up, before you get smacked the fuck up\nThat's how we do it on our side\nAny of you niggaz from New York that wanna bring it, bring it\nBut we ain't singin', we bringin' drama\nFuck you and your motherfuckin' mama\nWe gonna kill all you motherfuckers\nNow when I came out I told you it was just about Biggie\nThen everybody had to open their mouth with a motherfuckin' opinion\nWell this how we gonna do this\nFuck Mobb Deep\nFuck Biggie\nFuck Bad Boy as a staff record label\nAnd as a motherfuckin' crew\nAnd if you wanna be down with Bad Boy\nThen fuck you too\nChino XL, fuck you too\nAll you motherfuckers, fuck you too\n\n(Take money)\n(Take money)\nAlla y'all motherfuckers, fuck you die slow motherfucker\nMy fo'-fo' make sure all y'all kids don't grow\nYou motherfuckers can't be us or see us\nWe the motherfuckin' Thug Life riders West side till we die!\nOut here in California nigga we warn ya we'll bomb on you motherfuckers\nWe do our job\nYou think you mob, nigga we the motherfuckin mob\nAin't nuttin' but killers and fa'real niggaz\nAll you motherfuckers feel us\nOur shit's going triple and four-quadruple\n(Take money)\nYou niggaz laugh 'cause our staff got guns in they\nMotherfuckers belt, you know how it is\nWhen we drop records they felt\nYou niggaz can't feel it\nWe the realest, fuck em, we Bad Boy killaz"
# my_sent = "Hey girl, you know what you've been missing?\nMe, me, yeah\nHey girl, whoever you've been kissing\nIt ain't me, me\nI got that love medicinal\nI'll make you feel invincible\nI'm more than recreational\nI'm what you need\n\nI'll be your smooth ride, that late night, your Walter White high\nI'll be your first time, that's so right\nGet you falling in love at the end of the night\nWith that good-ish, that long trip, that sugar on your lips\nThat favorite habit, gotta have it, you can't quit\nI got your fix\n\nI'll be the high that never lets you down (I got your fix)\nThe one you crave when no one is around (I got your fix)\nI'll pick you up and never let you go (I got your fix)\nNever let you go, hey hey\n\nHey girl, he don't get you there never\nSo leave, oh just leave\nListen, baby baby baby baby girl\nLet me make it feel better\nPlease, please, please, please\nI'm what you need\n\nI'll be your smooth ride, that late night, your Walter White high\nI'll be your first time, that's so right\nGet you falling in love at the end of the night\nWith that good-ish, that long trip, that sugar on your lips\nThat favorite habit, gotta have it, you can't quit\nI got your fix\n\nI'll be the high that never lets you down (that never lets you down)\nThe one you crave when no one is around (when no one is around)\nI'll pick you up and never let you go (I got your fix)\nNever let you go\n\nYeah, come on baby, yeah, oh oh oh\nI'll be the high that never lets you down\nThe one you crave when no one is around\n\nI'll be your smooth ride, that late night, your Walter White high\nI'll be your first time, that's so right\nGet you falling in love at the end of the night\nWith that good-ish, that long trip, that sugar on your lips\nThat favorite habit, gotta have it, you can't quit\nI got your fix\n\nI'll be the high that never lets you down (that never lets you down)\nThe one you crave when no one is around (when no one is around)\nI'll pick you up and never let you go (I got your fix)\nNever let you go"
# my_sent = "When I find myself in times of trouble\nMother Mary comes to me\nSpeaking words of wisdom\nLet it be\n\nAnd in my hour of darkness\nShe is standing right in front of me\nSpeaking words of wisdom\nLet it be\n\n(Ooh) Let it be, let it be\nA-let it be, let it be\nWhisper words of wisdom\nLet it be\n\nAnd when the broken-hearted people\nLiving in the world agree\nThere will be an answer\nLet it be\n\nFor though they may be parted\nThere is still a chance that they will see\nThere will be an answer\nLet it be\n\nLet it be, let it be\nLet it be, let it be\nYeah, there will be an answer\nLet it be\n\nLet it be, let it be\nA-let it be, let it be\nWhisper words of wisdom\nLet it be\n\nLet it be, let it be\nA-let it be, yeah, let it be\nWhisper words of wisdom\nLet it be\n\nAnd when the night is cloudy\nThere is still a light that shines on me\nShine until tomorrow\nLet it be\n\nI wake up to the sound of music\nMother Mary comes to me\nSpeaking words of wisdom\nLet it be\n\nYeah, let it be, let it be\nLet it be, yeah, let it be\nOh, there will be an answer\nLet it be\n\nLet it be, let it be\nLet it be, yeah, let it be\nOh, there will be an answer\nLet it be\n\nLet it be, let it be\nLet it be, yeah, let it be \nWhisper words of wisdom \nLet it be"
class TextFeatureExtractor:


    def not_number(self,word):
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
        dic = dict()
        for token in tokens:
            if token not in dic:
                dic[token] = 1
            else:
                dic[token] =  dic[token] + 1

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
        total_size = len(tokens)
        unique_size = len(set(tokens))
        return unique_size/total_size





    def correctSpellCheck(self,sentences,lyrics):

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

        sentences = lyrics.split('\n')
        sentences = list(filter(lambda x: x is not None and x!= '' and len(x) >= 1, sentences))
        sentence_count = len(sentences)
        # sentences = self.correctSpellCheck(sentences, lyrics)
        offensive_count = 0

        for sentence in sentences:
            prob = predict_prob([sentence])
            if prob >= 0.3:
                offensive_count += 1

        return offensive_count/sentence_count

    def feature_slang(self,lyrics,tokens):
        spell = SpellChecker()
        word_tokenize(lyrics)
        misspelled = spell.unknown(tokens)
        return 1 - len(set(misspelled))/len(set(tokens))



    def start(self,lyrics):
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
