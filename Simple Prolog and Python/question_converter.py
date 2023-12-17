# question_converter.py
from InputSentence import InputSentence
import string

def question_to_prolog(query):
    query = query.lower().replace('?', '').replace(',', '')

    # Are X and Y the parents of Z?
    if all(word in query for word in ["are", "and", "the", "parents", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "the", "parents", "of"]]
        return f'parent(X, {list_of_names[2]})'

    # Are X and Y siblings?
    elif all(word in query for word in ["are", "and", "siblings"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "siblings"]]
        return f'sibling(X, {list_of_names[1]})'

    # Are X and Y relatives?
    elif all(word in query for word in ["are", "and", "relatives"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "relatives"]]
        return f'relative(X, {list_of_names[1]})'

    # Are W, X and Y children of Z?
    elif all(word in query for word in ["are", "and", "children", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "children", "of"]]
        return f'child(X, {list_of_names[3]})'

    # Who are the parents of X?
    elif 'who are the parents of ' in query:
        name = query.replace("who are the parents of ", "")
        return f'parent(X, {name.lower()})'

    # Who is the father of X?
    elif 'who is the father of ' in query:
        name = query.replace("who is the father of ", "")
        return f'father(X, {name.lower()})'

    # Who is the mother of X?
    elif 'who is the mother of ' in query:
        name = query.replace("who is the mother of ", "")
        return f'mother(X, {name.lower()})'

    # Who is the mother of X?
    elif 'who is the mother of ' in query:
        name = query.replace("who is the mother of ", "")
        return f'mother(X, {name.lower()})'

    # Who are the children of X?
    elif 'who are the children of ' in query:
        name = query.replace("who are the children of ", "")
        return f'child(X, {name.lower()})'

    # Who are the siblings of X?
    elif 'who are the siblings of ' in query:
        name = query.replace("who are the siblings of ", "")
        return f'sibling(X, {name.lower()})'

    # Who are the sisters of X?
    elif 'who are the sisters of ' in query:
        name = query.replace("who are the sisters of ", "")
        return f'sister(X, {name.lower()})'

    # Who are the brothers of X?
    elif 'who are the brothers of ' in query:
        name = query.replace("who are the brothers of ", "")
        return f'brother(X, {name.lower()})'

    # Who are the daughters of X?
    elif 'who are the daughters of ' in query:
        name = query.replace("who are the daughters of ", "")
        return f'daughter(X, {name.lower()})'

    # Who are the sons of X?
    elif 'who are the sons of ' in query:
        name = query.replace("who are the sons of ", "")
        return f'son(X, {name.lower()})'

    # Is X a grandmother of Y?
    elif all(word in query for word in ["is", "a", "grandmother", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandmother", "of"]]
        return f'grandmother(X, {list_of_names[1]})'

    # Is X a grandfather of Y?
    elif all(word in query for word in ["is", "a", "grandfather", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandfather", "of"]]
        return f'grandfather(X, {list_of_names[1]})'

    # Is X a sister of Y?
    elif all(word in query for word in ["is", "a", "sister", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "sister", "of"]]
        return f'sister(X, {list_of_names[1]})'

    # Is X a brother of Y?
    elif all(word in query for word in ["is", "a", "brother", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "brother", "of"]]
        return f'brother(X, {list_of_names[1]})'

    # Is X the mother of Y?
    elif all(word in query for word in ["is", "the", "mother", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "mother", "of"]]
        return f'mother(X, {list_of_names[1]})'

    # Is X the father of Y?
    elif all(word in query for word in ["is", "the", "father", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "father", "of"]]
        return f'father(X, {list_of_names[1]})'

    # Is X a daughter of Y?
    elif all(word in query for word in ["is", "a", "daughter", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "daughter", "of"]]
        return f'daughter(X, {list_of_names[1]})'

    # Is X a son of Y?
    elif all(word in query for word in ["is", "a", "son", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "son", "of"]]
        return f'son(X, {list_of_names[1]})'

    # Is X a child of Y?
    elif all(word in query for word in ["is", "a", "child", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "child", "of"]]
        return f'child(X, {list_of_names[1]})'

    # Is X an uncle of Y?
    elif all(word in query for word in ["is", "an", "uncle", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "uncle", "of"]]
        return f'uncle(X, {list_of_names[1]})'

    # Is X an aunt of Y?
    elif all(word in query for word in ["is", "an", "aunt", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "aunt", "of"]]
        return f'aunt(X, {list_of_names[1]})'

    else:
        return False


def question_to_query(query_sentence):
    input_sentence = InputSentence(query_sentence)
    ner = input_sentence.get_word_chunks()[0][1]
    query = "f'{0}(X, {1})'".format(input_sentence.get_relationships(), ner.lower())
    return query


def question_answer_converter(question_result, query):
    query = query.lower().replace('?', '')

    # Who are the parents of X?
    if 'who are the parents of' in query:
        if len(question_result) == 1:
            return f"The Parent is {question_result[0]['X']}"
        elif len(question_result) == 2:
            return f"The Parents are {question_result[0]['X']} and {question_result[1]['X']}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who is the father of X?
    elif 'who is the father of ' in query:
        if len(question_result) == 1:
            return f"The father is {question_result[0]['X']}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who is the mother of X?
    elif 'who is the mother of ' in query:
        if len(question_result) == 1:
            return f"The mother is {question_result[0]['X']}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the children of X?
    elif 'who are the children of ' in query:
        if len(question_result) > 0:
            children_list = []
            print(question_result)
            counter = 0
            while counter < len(question_result):
                children_list.append(question_result[counter]['X'])
                counter += 1
            if len(children_list) > 1:
                children_string = ', '.join(children_list)
                return f"The children are {children_string}"
            else:
                return f"The child is {children_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the siblings of X?
    elif 'who are the siblings of ' in query:
        if len(question_result) > 0:
            sibling_list = []
            print(question_result)
            counter = 0
            while counter < len(question_result):
                sibling_list.append(question_result[counter]['X'])
                counter += 1
            if len(sibling_list) > 1:
                sibling_string = ', '.join(sibling_list)
                return f"The siblings are {sibling_string}"
            else:
                return f"The sibling is {sibling_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the sisters of X?
    elif 'who are the sisters of ' in query:
        if len(question_result) > 0:
            sister_list = []
            print(question_result)
            counter = 0
            while counter < len(question_result):
                sister_list.append(question_result[counter]['X'])
                counter += 1
            if len(sister_list) > 1:
                sister_string = ', '.join(sister_list)
                return f"The sisters are {sister_string}"
            else:
                return f"The sister is {sister_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the brothers of X?
    elif 'who are the brothers of ' in query:
        if len(question_result) > 0:
            brother_list = []
            print(question_result)
            counter = 0
            while counter < len(question_result):
                brother_list.append(question_result[counter]['X'])
                counter += 1
            if len(brother_list) > 1:
                brother_string = ', '.join(brother_list)
                return f"The brothers are {brother_string}"
            else:
                return f"The brother is {brother_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the daughters of X?
    elif 'who are the daughters of ' in query:
        if len(question_result) > 0:
            daughter_list = []
            print(question_result)
            counter = 0
            while counter < len(question_result):
                daughter_list.append(question_result[counter]['X'])
                counter += 1
            if len(daughter_list) > 1:
                daughter_string = ', '.join(daughter_list)
                return f"The daughters are {daughter_string}"
            else:
                return f"The daughter is {daughter_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Who are the sons of X?
    elif 'who are the sons of ' in query:
        if len(question_result) > 0:
            son_list = []
            #print(question_result)
            counter = 0
            while counter < len(question_result):
                son_list.append(question_result[counter]['X'])
                counter += 1
            if len(son_list) > 1:
                son_string = ', '.join(son_list)
                return f"The sons are {son_string}"
            else:
                return f"The son is {son_list[0]}"
        else:
            return "Name/s is not yet in the knowledge base"

    # Are X and Y the parents of Z?
    elif all(word in query for word in ["are", "and", "the", "parents", "of"]):
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "the", "parents", "of"]]
        list_of_parents = [result['X'] for result in question_result]
        if all(item in list_of_names for item in list_of_parents):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Are X and Y siblings?
    elif 'are' and 'and' and 'siblings' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "siblings"]]
        list_of_siblings = [question_result[0]['X']]
        if all(item in list_of_names for item in list_of_siblings):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Are X and Y relatives?
    elif 'are' and 'and' and 'relatives' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["are", "and", "relatives"]]
        list_of_relatives = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_relatives):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Are W, X and Y children of Z?
    elif all(word in query for word in ["are", "and", "children", "of"]):
        query = query.split()
        list_of_names = [word.lower().strip(string.punctuation) for word in query if word not in ["are", "and", "children", "of"]]
        list_of_children = [result['X'].lower().strip(string.punctuation) for result in question_result]

        if all(name in list_of_children for name in list_of_names[:3]):
            return "Answer: Yes"
        else:
            return "Answer: No"

    # Is X a grandfather of Y?
    elif 'is' and 'a grandfather of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandfather", "of"]]
        list_of_grandfathers = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_grandfathers):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a grandmother of Y?
    elif 'is' and 'a grandmother of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandmother", "of"]]
        list_of_grandmothers = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_grandmothers):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a sister of Y?
    elif 'is' and 'a sister of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "sister", "of"]]
        list_of_sisters = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_sisters):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a brother of Y?
    elif 'is' and 'a brother of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "brother", "of"]]
        list_of_brothers = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_brothers):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X the mother of Y?
    elif 'is' and 'the mother of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "mother", "of"]]
        list_of_mothers = [result['X'] for result in question_result]
        if all(item in list_of_names for item in list_of_mothers):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X the father of Y?
    elif 'is' and 'the father of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "father", "of"]]
        list_of_fathers = [result['X'] for result in question_result]
        if all(item in list_of_names for item in list_of_fathers):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a daughter of Y?
    elif 'is' and 'a daughter of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "daughter", "of"]]
        list_of_daughters = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_daughters):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a son of Y?
    elif 'is' and 'a son of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "son", "of"]]
        list_of_sons = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_sons):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X a child of Y?
    elif 'is' and 'a child of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "child", "of"]]
        list_of_children = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_children):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X an uncle of Y?
    elif 'is' and 'an uncle of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "uncle", "of"]]
        list_of_uncles = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_uncles):
            return f"Answer: Yes"
        else:
            return f"Answer: No"

    # Is X an aunt of Y?
    elif 'is' and 'an aunt of ' in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "aunt", "of"]]
        list_of_aunts = [result['X'] for result in question_result]
        if any(item in list_of_names for item in list_of_aunts):
            return f"Answer: Yes"
        else:
            return f"Answer: No"


