from collections import defaultdict
import csv
import os
import sys

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def load_data(data_folder):
    nodes_path = os.path.join(data_folder, "nodes_neo4j.csv")
    edges_path = os.path.join(data_folder, "edges_neo4j.csv")
    group_by_semmantic_dict = defaultdict(list)
    id_type_mapping = {}
    with open(nodes_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            group_by_semmantic_dict[_item[-2]].append(_item[-1])
            id_type_mapping[_item[-1]] = _item[-2]
    cc_related = {}
    parsed_type_list = ['disease_or_phenotypic_feature', 'gene',
                        'protein', 'chemical_substance', 'phenotypic_feature',
                        'anatomical_entity', 'biological_process_or_activity']
    with open(edges_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            if _item[4] in group_by_semmantic_dict['cell_component']:
                if _item[4] not in cc_related:
                    cc_related[_item[4]] = {'_id': _item[4][5:],
                                                  'umls': _item[4][5:]}
                pred = _item[0].lower()
                semantic_type = id_type_mapping[_item[5]]
                if semantic_type not in parsed_type_list:
                    if pred not in cc_related[_item[4]]:
                        cc_related[_item[4]][pred] = {}
                    if semantic_type not in cc_related[_item[4]][pred]:
                        cc_related[_item[4]][pred][semantic_type] = []
                    cc_related[_item[4]][pred][semantic_type].append({'pmid': _item[1].split(';'), 'umls': _item[5][5:]})
            elif _item[5] in group_by_semmantic_dict['cell_component']:
                if _item[5] not in cc_related:
                    cc_related[_item[5]] = {'_id': _item[5][5:],
                                                  'umls': _item[5][5:]}
                pred = _item[0].lower() + '_reverse'
                semantic_type = id_type_mapping[_item[4]]
                if semantic_type not in parsed_type_list:
                    if pred not in cc_related[_item[5]]:
                        cc_related[_item[5]][pred] = {}
                    if semantic_type not in cc_related[_item[5]][pred]:
                        cc_related[_item[5]][pred][semantic_type] = []
                    cc_related[_item[5]][pred][semantic_type].append({'pmid': _item[1].split(';'), 'umls': _item[4][5:]})
    for v in cc_related.values():
        yield v
