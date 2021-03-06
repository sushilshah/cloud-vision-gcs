# @author Sushil Shah

import json
import knowledge_graph_api as kgraph

input_json = {}

def start_chirping(data, get_kg=False):
    chirping_response = {}
    if 'responses' in data:

        _results = data["responses"][0]
        for attribute in _results:
            if attribute == 'safeSearchAnnotation':
                safe_search_result  = validate_safe_search_annotation(_results[attribute])
                if not safe_search_result:
                	raise ValueError("Image Failed Safe Search Result")
            if attribute == 'labelAnnotations': 
                validate_label_result = validate_label_annotations(_results[attribute])
                if validate_label_result:
                    #bird found. chirping....
                    ##Search birdName and 
                    search_bird_results = search_bird(_results[attribute])
                    
                    if search_bird_results:
                        chirping_bird = search_bird_results[0] #pick at index 0
                        if not 'birdInfo' in chirping_response:
                        	chirping_response['birdInfo'] = []
                        chirping_response['birdInfo'].append(chirping_bird)
                        chirping_response['knowledgeGraphUri'] = chirping_bird['mid']
                        #knowledge graph search 
                        if get_kg:
                        	kg_response = kgraph.get_from_freebase_knowledge_graph(chirping_bird['mid'])
                            ##Add to response bird info
                        	chirping_response['knowledgeGraphResponse'] = kg_response
                    else:
                        chirping_response = {"message": "Bird Name not recognised"}
                        print "#### ELse block in bird chirping"
                else:
                    chirping_response = {"message": "No bird recognised"}
                    
    return chirping_response


#expects input format as [{u'score': u'0.98018545', u'mid': u'/m/0h29c', u'description': u'peafowl'}, {u'score': u'0.94620532', u'mid': u'/m/015p6', u'description': u'bird'}]
bird_name_list = ['hummingbird', 'owl', 'penguin', 'kingfisher', 'peafowl', 'parrot', "house sparrow", 'tinamou','ostrich','rhea','cassowarie','emu','kiwi','waterfowl','screamer','megapode','guineafowl','loon','penguin','albatrosse','grebe','flamingo','tropicbird','stork','heron','Hamerkop','Shoebill','Pelican','frigatebird','darter','secretarybird','osprey','bustard','mesite','seriema','kagu','sunbittern','flufftail','finfoot','trumpeter','crane','limpkin','buttonquail','sheathbill','oystercatcher','ibisbill','jacana','seedsnipe','sandpiper','skua','auk','sandgrouse','hoatzin','turaco','owl','frogmouth','oilbird','potoo','nightjar','treeswift','swift','hummingbird','mousebird','trogon','roller','kingfisher','todie','motmot','jacamar','puffbird','toucan','honeyguide']
def search_bird(input):
    response = []
    i = 0
    for label_annotations in input:
        if label_annotations['description'].lower() in bird_name_list:
            response.append(label_annotations)
            i=+1
    return response



ADULT_PASS_CRITERIA = ['VERY_UNLIKELY', 'UNLIKELY']
VIOLENCE_PASS_CRITERIA = ['VERY_UNLIKELY', 'UNLIKELY']
#expects input format as {"spoof": "VERY_UNLIKELY", "adult": "VERY_UNLIKELY"}
def validate_safe_search_annotation(input):
    pass_flag = False

    for attribute in input:
        if attribute == 'adult':
            if input[attribute] in ADULT_PASS_CRITERIA:
                pass_flag = True 
                #false
            if input[attribute] in VIOLENCE_PASS_CRITERIA and pass_flag:
                pass_flag = True
            else:
                pass_flag = False
    return pass_flag




#expects input format as [{u'score': u'0.98018545', u'mid': u'/m/0h29c', u'description': u'peafowl'}, {u'score': u'0.94620532', u'mid': u'/m/015p6', u'description': u'bird'}]
def validate_label_annotations(input):
    for label_annotation in input:
        if label_annotation['description'] == 'bird':
            print "HAPPINESS: Yay! Bird found."
            return True
    return False
