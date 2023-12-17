from pyswip import *


prolog_file = Prolog()
prolog_file.consult('family.pl')


########################################################################################################################
#Code to Validate EXISTING RELATIONSHIPS
########################################################################################################################

def find_relationships(list_of_names, return_query, new_child_name, query):
    descendant_list = get_descendants(list_of_names, return_query, new_child_name)
    uncle_and_aunts_list = get_uncle_aunt(list_of_names, return_query, new_child_name)

    if any(word in query for word in ["sibling", "brother", "sister"]):
        parents_list = get_parents_of_siblings(list_of_names, new_child_name)
        child_list = []
    else:
        parents_list = []
        child_list = get_children_of_parents(list_of_names, new_child_name)

    relationship_list = return_query + child_list + parents_list + descendant_list + uncle_and_aunts_list

    relationship_list = list({tuple(pair): pair for pair in relationship_list}.values())

    return relationship_list


def names_filter(list_of_names):
    response = True

    if len(list_of_names) < 3:
        if existing_relationship_checker(list_of_names) == False:
            response = "I already know that!"
        elif repeat_names_checker(list_of_names) == False:
            response = "That's Impossible!"
    else:
        if repeat_names_checker(list_of_names) == False:
            response = "That's Impossible!"

    return response

def repeat_names_checker(list_of_names):
    
    seen_names = set()

    for name in list_of_names:
        if name in seen_names:
            return False
        seen_names.add(name)

    return True


def existing_relationship_checker(list_of_names):
    relationships = ['parent', 'father', 'mother', 'sibling', 'sister', 'brother', 
                     'grandchild', 'grandmother', 'grandfather', 'child', 'daughter', 
                     'aunt', 'uncle']  # Add other relationships as needed
    
    relationship_validity = True

    for name1 in list_of_names:
        for name2 in list_of_names:
            if name1 == name2:
                continue
            else:
                for relationship in relationships:
                    query = f"{relationship}({name1}, {name2})."
                    result = list(prolog_file.query(query))
                    if result:
                        relationship_validity = False
    
    return relationship_validity

def existing_relationship_cleaner(list_of_names, relationship_facts):
    relationships = ['parent', 'father', 'mother', 'sibling', 'sister', 'brother', 
                     'grandchild', 'grandmother', 'grandfather', 'child', 'daughter', 
                     'aunt', 'uncle']  # Add other relationships as needed
    

    list_of_names_with_relationship = []

    for name1 in list_of_names:
        for name2 in list_of_names:
            if name1 == name2:
                continue
            else:
                for relationship in relationships:
                    query1 = f"{relationship}({name1}, {name2})."
                    result1 = list(prolog_file.query(query1))
                    if result1:
                        list_of_names_with_relationship.append([name1, name2])

                        


    list_of_names_with_relationship = list({tuple(pair): pair for pair in list_of_names_with_relationship}.values())



    updated_relationship_facts = []

    if len(list_of_names_with_relationship) < 1:
        updated_relationship_facts = relationship_facts
    else:
        for pair in list_of_names_with_relationship:
            for facts in relationship_facts:
                if pair[0] and pair[1] not in facts:
                    continue
                else:
                    updated_relationship_facts.append(facts)



    return updated_relationship_facts



########################################################################################################################
#This section detects User Input and Converts it to Prolog Facts#
########################################################################################################################



def statement_to_prolog(query):
    query = query.lower().replace('.', '')

    #X is a male.
    if "is a male" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "male"]]
        return_query = [f'male({list_of_names[0]})']
        if list(prolog_file.query(return_query[0])):
            return "I already know that!"
        elif list(prolog_file.query(f'female({list_of_names[0]})')):
            return "That's Impossible!"
        else:
            return return_query
        
    #X is a female.
    if "is a female" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "female"]]
        return_query = [f'female({list_of_names[0]})']
        if list(prolog_file.query(return_query[0])):
            return "I already know that!"
        elif list(prolog_file.query(f'male({list_of_names[0]})')):
            return "That's Impossible!"
        else:
            return return_query

    #X and Y are the parents of Z.
    if "are the parents of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["and", "are", "the", "parents", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[2]]
        return_query = [f'parent({list_of_names[0]}, {list_of_names[2]})', 
                        f'parent({list_of_names[1]}, {list_of_names[2]})']
        relationship_facts = find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts

    #X is the father of Y.
    elif "is the father of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "father", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[1]]
        return_query = [f'father({list_of_names[0]}, {new_child_name[0]})', 
                        f'parent({list_of_names[0]}, {new_child_name[0]})',
                        f'child({new_child_name[0]}, {list_of_names[0]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts      

    #X is the Mother of Y.
    elif "is the mother of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "the", "mother", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[1]]
        return_query = [f'mother({list_of_names[0]}, {new_child_name[0]})', 
                        f'parent({list_of_names[0]}, {new_child_name[0]})',
                        f'child({new_child_name[0]}, {list_of_names[0]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X is a child of Y.
    elif "is a child of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "child", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0]]
        return_query = [f'child({list_of_names[0]}, {list_of_names[1]})', 
                        f'parent({list_of_names[1]}, {list_of_names[0]})']
        relationship_facts = find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X and Y are siblings.
    elif "are siblings" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["and", "are", "siblings"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0], list_of_names[1]]
        return_query = [f'sibling({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X is a sister of Y.
    elif "is a sister of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "sister", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0], list_of_names[1]]
        return_query = [f'sister({list_of_names[0]}, {list_of_names[1]})', 
                        f'sibling({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X is a brother of Y.
    elif "is a brother of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "brother", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0], list_of_names[1]]
        return_query = [f'brother({list_of_names[0]}, {list_of_names[1]})', 
                        f'sibling({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts

    #X is a grandmother of Y.
    elif "is a grandmother of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandmother", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[1]]
        return_query = [f'grandmother({list_of_names[0]}, {list_of_names[1]})', 
                        f'grandchild({list_of_names[1]}, {list_of_names[0]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts 

    #X is a grandfather of Y.
    elif "is a grandfather of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "grandfather", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[1]]
        return_query = [f'grandfather({list_of_names[0]}, {list_of_names[1]})', 
                        f'grandchild({list_of_names[1]}, {list_of_names[0]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts  

    #X is a daughter of Y.
    elif "is a daughter of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "daughter", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0]]
        return_query = [f'child({list_of_names[0]}, {list_of_names[1]})', 
                        f'parent({list_of_names[1]}, {list_of_names[0]})', 
                        f'daughter({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts  
    
    #X is a son of Y.
    elif "is a son of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "a", "son", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0]]
        return_query = [f'child({list_of_names[0]}, {list_of_names[1]})', 
                        f'parent({list_of_names[1]}, {list_of_names[0]})', 
                        f'son({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts  
    
    #X is an uncle of Y.
    elif "is an uncle of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "uncle", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0]]
        return_query = [f'uncle({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X is an aunt of Y.
    elif "is an aunt of" in query:
        query = query.split()
        list_of_names = [word for word in query if word not in ["is", "an", "aunt", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0]]
        return_query = [f'aunt({list_of_names[0]}, {list_of_names[1]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts
    
    #X, Y, and Z are children of W.
    elif "are children of" in query:
        query = query.replace(",","")
        query = query.split()
        list_of_names = [word for word in query if word not in ["and", "are", "children", "of"]]
        if names_filter(list_of_names) is not True:
            return names_filter(list_of_names)
        new_child_name = [list_of_names[0], list_of_names[1], list_of_names[2]]
        return_query = [f'parent({list_of_names[3]}, {list_of_names[0]})', 
                        f'parent({list_of_names[3]}, {list_of_names[1]})', 
                        f'parent({list_of_names[3]}, {list_of_names[2]})',
                        f'child({list_of_names[0]}, {list_of_names[3]})', 
                        f'child({list_of_names[1]}, {list_of_names[3]})', 
                        f'child({list_of_names[2]}, {list_of_names[3]})',
                        f'sibling({list_of_names[0]}, {list_of_names[1]})', 
                        f'sibling({list_of_names[0]}, {list_of_names[2]})', 
                        f'sibling({list_of_names[1]}, {list_of_names[2]})']
        relationship_facts= find_relationships(list_of_names, return_query, new_child_name, query)
        relationship_facts = existing_relationship_cleaner(list_of_names, relationship_facts)
        return relationship_facts 

    else:
        return "Kindly fix the sentence format."
    


########################################################################################################################
#This section provides logic to find the relationship between siblings and parents#
########################################################################################################################




###########################  CODE TO FIND CHILDREN ###################################

def get_children_of_parents(list_of_names, child_name):
    children_list = find_children(list_of_names)
    children_list = children_list + child_name

    parents_list = find_parents(children_list)

    updated_parents = process_children(parents_list, children_list)


    
    list_of_parent_child_pairs = get_parent_child_pairs(parents_list, children_list)

    sibling_list = []

    for child in children_list:
        for name in children_list:
            if child == name:
                continue
            else:
                pair_detection  = []
                for pair in list_of_parent_child_pairs:
                    if child in pair and name in pair:
                        pair_detection.append(True)
                    else:
                        pair_detection.append(False)
                if True in pair_detection:
                    continue
                else:
                    sibling_list.append(f"sibling({child}, {name})")

    return updated_parents + sibling_list


def find_children(list_of_names):
    # List to store query results
    children_list =  []

    # Query for each name
    for name in list_of_names:
        parent_query = list(prolog_file.query(f"parent({name}, Y)"))
        father_query = list(prolog_file.query(f"father({name}, Y)"))
        mother_query = list(prolog_file.query(f"mother({name}, Y)"))

        for parent in parent_query:
            children_list.append(parent['Y']) 
        
        for father in father_query:
            children_list.append(father['Y'])
        
        for mother in mother_query:
            children_list.append(mother['Y'])

    children_list = list(set(children_list))

    return children_list

def get_parent_child_pairs(parents_list, children_list):

    list_of_parent_child_pairs = []

    for i in range(len(parents_list)):
        for name in children_list:
            for name2 in children_list:
                if name == name2:
                    continue
                elif name and name2 not in parents_list[i]:
                    continue
                elif name and name2 and "parent" in parents_list[i]:
                    fact = parents_list[i].replace('parent(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    list_of_parent_child_pairs.append(parent_child)
                elif name and name2 and "child" in parents_list[i]:
                    fact = parents_list[i].replace('child(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    list_of_parent_child_pairs.append(parent_child)
                elif name and name2 and "father" in parents_list[i]:
                    fact = parents_list[i].replace('father(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    list_of_parent_child_pairs.append(parent_child)
                elif name and name2 and "mother" in parents_list[i]:
                    fact = parents_list[i].replace('mother(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    list_of_parent_child_pairs.append(parent_child)

    return list_of_parent_child_pairs


def process_children(parents_list, children_list):

    list_of_parent_child_pairs = get_parent_child_pairs(parents_list, children_list)

    updated_parents_list = []

    for child in children_list:
        for parent in parents_list:
            if child in parent:
                for name in children_list:
                    if name in parent:
                        continue
                    else:
                        pair_detection  = []
                        for pair in list_of_parent_child_pairs:
                            if child in pair and name in pair:
                                pair_detection.append(True)
                            else:
                                pair_detection.append(False)

                        if True in pair_detection:
                            continue
                        else:
                            updated_parents_list.append(parent.replace(child, name))
            else:
                continue
    
    updated_parents_list = list(set(updated_parents_list) - set(parents_list))
    
    return updated_parents_list
    

###########################  CODE TO FIND CHILDREN ###################################

###########################  CODE TO FIND PARENTS ###################################

def get_parents_of_siblings(list_of_names, new_child_name):
    parents_list = find_parents(list_of_names)
    final_parents = process_parents(parents_list, list_of_names, new_child_name)



    return final_parents

def find_parents(list_of_names):
    # List to store query results
    parents_list = []

    # Query for each name
    for name in list_of_names:
        parent_query = list(prolog_file.query(f"parent(X, {name})"))
        father_query = list(prolog_file.query(f"father(X, {name})"))
        mother_query = list(prolog_file.query(f"mother(X, {name})"))

        # Add results to the list
        parents_list.extend([
            f"parent({parent['X']}, {name})" for parent in parent_query
        ])
        parents_list.extend([
            f"father({father_query[0]['X']}, {name})" if father_query else None,
            f"mother({mother_query[0]['X']}, {name})" if mother_query else None
        ])
        parents_list.extend([
            f"child({name}, {parent['X']})" for parent in parent_query
        ])
        parents_list.extend([
            f"child({name}, {father_query[0]['X']})" if father_query else None,
            f"child({name}, {mother_query[0]['X']})" if mother_query else None,
        ])

    # Remove None values and empty strings from the list
    parents_list = [result for result in parents_list if result is not None and result != '']
       
    return parents_list

def process_parents(parents_list, list_of_names, new_child_name):

    children_list = find_children(list_of_names) + new_child_name

    new_name = []
    for name in list_of_names:
        found = any(name in item for item in parents_list)
        if found:
            old_name = name
        else:
            new_name.append(name)

    facts_list = []

    remove_parents_list = []


    for parent in list_of_names:
        for child in children_list:
            for fact in parents_list:
                if parent and child in fact:
                    remove_parents_list.append(fact)
                else:
                    continue

    intersection_set = set(parents_list) & set(remove_parents_list)
    parents_list = [parent for parent in parents_list if parent not in intersection_set]

    for name in new_name:
        facts_list.append([fact.replace(old_name, name) for fact in parents_list])

    facts_list = [item for sublist in facts_list for item in sublist]
    facts_list = [f'{fact}' for fact in facts_list]

    return facts_list

###########################  CODE TO FIND PARENTS ###################################

###########################  CODE TO FIND GRANDPARENTS ###################################

def get_descendants(list_of_names, return_query, child_name):

    children_list = find_children(list_of_names)
    children_list = children_list + child_name
    parents_list = find_parents(children_list)
    parents_list = parents_list + return_query

    parent_child_pair = []

    for i in range(len(parents_list)):
        for name in children_list:
            for name2 in children_list:
                if name == name2:
                    continue
                elif name and name2 not in parents_list[i]:
                    continue
                elif name and name2 and "parent" in parents_list[i]:
                    fact = parents_list[i].replace('parent(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)
                elif name and name2 and "father" in parents_list[i]:
                    fact = parents_list[i].replace('father(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)
                elif name and name2 and "mother" in parents_list[i]:
                    fact = parents_list[i].replace('mother(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)

    parent_child_pair = list({tuple(pair): pair for pair in parent_child_pair}.values())


    list_of_grandparent_grandchild = []

    for pair in parent_child_pair:
        parent = pair[0]
        child  = pair [1]

        for pair2 in parent_child_pair:
            if pair == pair2:
                continue
            elif child == pair2[0]:
                list_of_grandparent_grandchild.append([parent, pair2[1]])

    
    grandparent_facts = []

    for pair in list_of_grandparent_grandchild:
        for relationship in parents_list: 
            if f"father({pair[0]}" in relationship:
                grandparent_facts.append(f'grandfather({pair[0]}, {pair[1]})')
            elif f"mother({pair[0]}" in relationship:
                grandparent_facts.append(f'grandmother({pair[0]}, {pair[1]})')
            else:
                continue
    
    grandparent_facts = list({tuple(pair): pair for pair in grandparent_facts}.values())



    return grandparent_facts


###########################  CODE TO FIND GRANDPARENTS ###################################

###########################  CODE TO FIND UNCLES AND AUNTS ###################################

def get_uncle_aunt(list_of_names, return_query, child_name):

    children_list = find_children(list_of_names)
    children_list = children_list + child_name + list_of_names
    parents_list = find_parents(children_list)
    parents_list = parents_list + return_query



    parent_child_pair = []

    for i in range(len(parents_list)):
        for name in children_list:
            for name2 in children_list:
                if name == name2:
                    continue
                elif name and name2 not in parents_list[i]:
                    continue
                elif name and name2 and "parent" in parents_list[i]:
                    fact = parents_list[i].replace('parent(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)
                elif name and name2 and "father" in parents_list[i]:
                    fact = parents_list[i].replace('father(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)
                elif name and name2 and "mother" in parents_list[i]:
                    fact = parents_list[i].replace('mother(', '').replace(')', '').replace(' ', '')
                    parent_child = fact.split(",")
                    parent_child_pair.append(parent_child)

    parent_child_pair = list({tuple(pair): pair for pair in parent_child_pair}.values())

    parents_of_new_child = []

    for pair in parent_child_pair:
        if child_name[0] in pair:
            parents_of_new_child.append(pair[0])
        else:
            continue

    
    parent_of_parents = find_parents(parents_of_new_child)

    grandparents = []

    for relationship in parent_of_parents:
        for name in parents_of_new_child:
            if name + ")" in relationship:
                if "parent" in relationship:
                    grandparent = relationship.replace('parent(', '').replace(f'{name})', '').replace(' ', '').replace(',', '')
                    grandparents.append(grandparent)
                elif "father" in relationship:
                    grandparent = relationship.replace('father(', '').replace(f'{name})', '').replace(' ', '').replace(',', '')
                    grandparents.append(grandparent)
                elif "mother" in relationship:
                    grandparent = relationship.replace('mother(', '').replace(f'{name})', '').replace(' ', '').replace(',', '')
                    grandparents.append(grandparent)
            else:
                continue


    sibling_list = []


    for name in list_of_names:
        for name2 in list_of_names:
            if name == name2:
                continue
            elif f"brother({name}, {name2})" or f"brother({name2}, {name})" in return_query:
                    sibling_list.append(name)
                    sibling_list.append(name2)
            elif f"sister({name}, {name2})" or f"sister({name2}, {name})" in return_query:
                    sibling_list.append(name)
                    sibling_list.append(name2)
            elif f"sibling({name}, {name2})" or f"sibling({name2}, {name})" in return_query:
                    sibling_list.append(name)
                    sibling_list.append(name2)
            else:
                continue
    

    sibling_list = sibling_list + find_siblings(parents_of_new_child) + find_children(grandparents) + find_siblings(list_of_names)
    sibling_list = list(set(sibling_list) - set(parents_of_new_child))

    uncle_aunt_facts = []

    for sibling in sibling_list:
        for child in child_name:
            try:
                if list(prolog_file.query(f"male({sibling})")):
                    uncle_aunt_facts.append(f"uncle({sibling}, {child})")
                elif list(prolog_file.query(f"female({sibling})")):
                    uncle_aunt_facts.append(f"aunt({sibling}, {child})")
            except Exception:
                continue
            
    
    for sibling in sibling_list:
        for parent in parents_of_new_child:
            for child in child_name:
                if sibling == parent:
                    continue
                else:
                    try:
                        if list(prolog_file.query(f"brother({parent}, {sibling})")) or list(prolog_file.query(f"brother({sibling}, {parent})")):
                            uncle_aunt_facts.append(f"uncle({sibling}, {child})")
                        elif list(prolog_file.query(f"sister({parent}, {sibling})")) or list(prolog_file.query(f"sister({sibling}, {parent})")):
                            uncle_aunt_facts.append(f"aunt({sibling}, {child})")
                    except Exception:
                        continue





    uncle_aunt_facts = list({tuple(pair): pair for pair in uncle_aunt_facts}.values())



    return uncle_aunt_facts


def find_siblings(list_of_names):
    relationships = ['sibling', 'sister', 'brother']
    
    list_of_siblings = []

    for name in list_of_names:
        for relationship  in relationships:      
                    query = f"{relationship}({name}, Y)."
                    result = list(prolog_file.query(query))
                    for sibling in result:
                        list_of_siblings.append(sibling['Y'])
                    query2 = f"{relationship}(X, {name})."
                    result2 = list(prolog_file.query(query2))
                    for sibling in result2:
                        list_of_siblings.append(sibling['X'])


    list_of_siblings = list({tuple(pair): pair for pair in list_of_siblings}.values())

    return list_of_siblings