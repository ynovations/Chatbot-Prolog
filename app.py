from flask import Flask, request

from InputSentence import InputSentence

app = Flask(__name__)


@app.route('/sentence', methods=["POST"])
def detect_sentence():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.get_json()
        # create prolog query or statement, then return answer
        input_sentence = InputSentence(json['sentence'])
        # is_question = SentenceDetector.parse_sentence(json['sentence'])
        token_sequence = []
        if input_sentence.is_question():
            # query = Template('ffather(x, $x)')
            # print(input_sentence.get_word_chunks())
            for token in input_sentence.get_tokens():
                token_sequence.append(token[1])
                # if str(token[1]) == "NNP":
                #     query.substitute(x=token[0])

            # print("-".join(token_sequence))
            query = "f'{0}(X, {1})'".format(input_sentence.get_relationships(),
                                            input_sentence.get_word_chunks()[0][1].lower())
            # return query
            # return f'{input_sentence.get_relationships()}(X, {input_sentence.get_word_chunks()})'
            return {"response": "sentence is a question",
                    "relationship": input_sentence.get_relationships(),
                    "sentence_pattern": input_sentence.get_ner_position(),
                    "query": query}
        else:
            query = "f'{0}(X, {1})'".format(input_sentence.get_relationships(), input_sentence.get_word_chunks())
            # return query
            # return f'{input_sentence.get_relationships()}(X, {input_sentence.get_word_chunks()})'
            return {"response": "added to knowledge base",
                    "relationship": input_sentence.get_relationships(),
                    "sentence_pattern": input_sentence.get_ner_position(),
                    "query": query}
    else:
        return {"response": "Content-Type not supported!"}

    # with PrologMQI() as mqi:
    #     with mqi.create_thread() as prolog_thread:
    #         result = prolog_thread.query("atom(a)")
    #         return str(result)


if __name__ == '__main__':
    app.run()
