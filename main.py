__author__ = 'Mengyao Yang'

import json
from collections import deque

#Entity object
class Entity(object):
    def __init__(self, enti_id, name, des = None, out_list = None):
        self.id = enti_id
        self.name = name
        self.des = des
        self.goes_to = out_list
    #override 'toString' function
    def __str__(self):
        if self.goes_to:
            str_list = [str(self.id), " ".join(str(v.id) for v in self.goes_to)]
        else:
            str_list = [str(self.id)]
        return ','.join(str_list)

# link object
class Link(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __str__(self):
        return ','.join([str(self.start), str(self.end)])

# input: nested dictionary (hashtable) from json file
# output: dictionary (hashtable) {id : entity}, list [links]
def input_parser(data):
    # build entity list
    entity_input = data["entities"]
    link_input = data["links"]

    id_to_entity = dict()
    link_olist = []
    for entity in entity_input:
        descrip = None
        if "description" in entity:
            descrip = entity["description"]

        if "entity_id" not in entity or "name" not in entity:
            # invalid input file
            # usually throw managable exception and record this in log
            # like: raise ValueError('input file is broken!')
            continue
        new_entity = Entity(entity["entity_id"], entity["name"], descrip)
        id_to_entity[entity["entity_id"]] = new_entity

    for link in link_input:
        if "from" not in link or "to" not in link:
            # invalid input file
            # usually throw managable exception and record this in log
            # like: raise ValueError('input file is broken!')
            continue
        come = link["from"]
        leave = link["to"]
        link_olist.append(Link(come, leave))
        start = id_to_entity[come]
        end = id_to_entity[leave]
        if start.goes_to:
            start.goes_to.append(end)
        else:
            start.goes_to = [end]
    return id_to_entity, link_olist

# input: dictionary (hashtable) {id : entity}, list [links]
# output: cloned dictionary, cloned list
# using BFS to search the graph
def clone(id_to_entity, link_olist, entity_id):
    if entity_id not in id_to_entity:
        raise ValueError('the id to clone does not exist!')

    queue = deque([id_to_entity[entity_id]])
    visited = set()
    while queue:
        current_entity = queue.popleft()
        visited.add(current_entity)
        # create new entity
        new_id = current_entity.id + 10000
        new_entity = Entity(new_id, current_entity.name, current_entity.des)
        id_to_entity[new_id] = new_entity
        if current_entity.goes_to is None:
            continue
        for child in current_entity.goes_to:
            if child in visited:
                continue
            queue.append(child)
    # create new links
    visited_id = set([x.id for x in visited])
    for link in link_olist:
        if link.start in visited_id and link.end in visited_id:
            new_link = Link(link.start + 10000, link.end + 10000)
            link_olist.append(new_link)
        else:
            pass
        if link.end == entity_id:
            new_link = Link(link.start, link.end + 10000)
            link_olist.append(new_link)
        else:
            pass

    return id_to_entity, link_olist

# input: cloned dictionary, cloned list
# output: nested dictionary that meets the input format
def output_parser(id_to_entity, link_olist):
    data = {"entities" : [], "links" : []}
    for id in id_to_entity:
        entity_dic = dict()
        entity_dic["entity_id"] = id
        entity_dic["name"] = id_to_entity[id].name
        if id_to_entity[id].des:
            entity_dic["description"] = id_to_entity[id].des

        data["entities"].append(entity_dic)

    for link in link_olist:
        link_dic = dict()

        link_dic["to"] = link.end
        link_dic["from"] = link.start
        data["links"].append(link_dic)

    return data

# main steps to tackle the problem
def main_sequence():
    # 1. parser command
    new_line = raw_input('please type the command:')
    input_file, entity_id = new_line.split(',')
    input_file = input_file.strip()
    entity_id = int(entity_id.strip())

    # 2. read input file
    try:
        with open(input_file) as file:
            data = json.load(file)
    except IOError:
        raise TypeError('wrong name for the input file!')

    # 3. parse the file
    id_to_entity, link_olist = input_parser(data)

    if not entity_id in id_to_entity:
        # record in log
        raise ValueError('the id to clone does not exist!')

    # 4. clone graph
    id_to_entity_cloned, link_olist_cloned = clone(id_to_entity, link_olist, entity_id)

    # 5. build the output format(nested dictionary)
    data_cloned = output_parser(id_to_entity_cloned, link_olist_cloned)

    # 6. write to result file
    with open('result.json', 'w') as out_file:
        json.dump(data_cloned, out_file, indent = 4)


if __name__ == "__main__":
    main_sequence()