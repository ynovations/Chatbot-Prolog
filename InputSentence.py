import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

stop_words = set(stopwords.words('english'))


class InputSentence:
    def __init__(self, input_sentence):
        self.question_words = ["who", "are", "is", "are", "whom", "whose"]
        self.relationships = ["father", "mother", "son", "daughter", "sibling", "parents", "children"]
        self.word_tokens = word_tokenize(input_sentence)
        # word_tokens = [w for w in word_tokens if not w in stop_words]
        # self.tagged_tokens = nltk.pos_tag(word_tokens)

    def is_question(self):
        return True if any(x in self.word_tokens[0].lower() for x in self.question_words) else False
        # return self.is_question

    def get_tokens(self):
        tokens = [w for w in self.word_tokens if not w.lower() in stop_words]
        tokens = [w.lower() for w in tokens if w.isalpha()]
        return nltk.pos_tag(tokens)
        # return self.tagged_tokens

    def get_word_chunks(self):
        ner = []
        for chunk in nltk.ne_chunk(nltk.pos_tag(self.word_tokens)):
            if hasattr(chunk, 'label'):
                entity_pair = chunk.label(), ' '.join(c[0] for c in chunk)
                ner.append(entity_pair)
                print(entity_pair)

        return ner

    def get_ner_position(self):
        tokens = [w for w in self.get_tokens()]
        ner_position = []
        position = 0
        for token in tokens:
            pair = position, token[0]
            ner_position.append(pair)
            position += 1

        return ner_position

    def get_relationships(self):
        return [w for w in self.word_tokens if w in self.relationships][0]
