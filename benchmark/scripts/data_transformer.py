import pandas as pd
import numpy as np
import sys
import os
import glob

SOURCE_FOLDER = "/Users/guanchao/Desktop/Graphs/Graphs/benchmark/Graphflow/LDBC/scale-1/variant-0/csv"
SRC_VERTICES_FOLDER = SOURCE_FOLDER + "/Vertices"
SRC_EDGES_FOLDER = SOURCE_FOLDER + "/Edges"
OUTPUT_FOLDER = "/Users/guanchao/Desktop/Graphs/Graphs/benchmark/Graphflow/LDBC/scale-1/variant-0/Graphflow"
OUTPUT_EDGES_PATH = OUTPUT_FOLDER + "/edges.csv"
OUTPUT_VERTICES_PATH = OUTPUT_FOLDER + "/vertices.csv"

vertex_label_map = {
    'PLACE': 0,
    'PERSON': 1,
    'COMMENT': 2,
    'POST': 3,
    'FORUM': 4,
    'ORGANISATION': 5,
    'TAGCLASS': 6,
    'TAG': 7,
    'COUNTRY': 8,
    'CITY': 9,
    'CONTINENT': 10,
    'COMPANY': 11,
    'UNIVERSITY': 12,
}
edge_label_map = {
    'HASCREATOR': 0,
    'HASTAG': 1,
    'REPLYOF': 3,
    'CONTAINEROF': 5,
    'HASMEMBER': 6,
    'HASMODERATOR': 7,
    'HASINTEREST': 10,
    'ISLOCATEDIN': 11,
    'KNOWS': 12,
    'LIKES': 13,
    'STUDYAT': 15,
    'WORKAT': 16,
    'ISPARTOF': 17,
    'HASTYPE': 21,
    'ISSUBCLASSOF': 22,
}

edges_list = [
    ('COMMENT_HASCREATOR_PERSON'),
    ('POST_HASCREATOR_PERSON'),
    ('COMMENT_HASTAG_TAG'),
    ('FORUM_HASTAG_TAG'),
    ('POST_HASTAG_TAG'),
    ('COMMENT_REPLYOF_COMMENT'),
    ('COMMENT_REPLYOF_POST'),
    ('FORUM_CONTAINEROF_POST'),
    ('FORUM_HASMEMBER_PERSON'),
    ('FORUM_HASMODERATOR_PERSON'),
    ('ORGANISATION_ISLOCATEDIN_PLACE'),
    ('POST_ISLOCATEDIN_PLACE'),
    ('PERSON_ISLOCATEDIN_PLACE'),
    ('COMMENT_ISLOCATEDIN_PLACE'),
    ('PERSON_KNOWS_PERSON'),
    ('PERSON_LIKES_COMMENT'),
    ('PERSON_LIKES_POST'),
    ('PERSON_STUDYAT_ORGANISATION'),
    ('PERSON_WORKAT_ORGANISATION'),
    ('PLACE_ISPARTOF_PLACE'),
    ('TAG_HASTYPE_TAGCLASS'),
    ('TAGCLASS_ISSUBCLASSOF_TAGCLASS'),
    ('PERSON_HASINTEREST_TAG'),
]

def gen_edges_csv():
    vertices_df = pd.DataFrame(columns=['id', 'label'])
    df = pd.DataFrame(columns=['from', 'to', 'label'])
    for edge_name in edges_list:
        from_vertex_label = edge_name.split("_")[0]
        edge_label_str = edge_name.split("_")[1]
        to_vertex_label = edge_name.split("_")[2]
        edge_label = edge_label_map.get(edge_label_str)
        print('Edge Dir: %s, Edge_Label: %s' % (edge_name, edge_label))
        csv_file_path = SRC_EDGES_FOLDER + "/" + edge_name + "_0_0.csv"
        if os.path.exists(csv_file_path):
            data = pd.read_csv(csv_file_path, sep='|', encoding='utf-8', usecols=[0, 1])
            data['label'] = edge_label_str
            # data['label'] = edge_label_map.get(edge_label_str)
            data.rename(columns={data.columns[0]:'from', data.columns[1]:'to', data.columns[2]:'label'}, inplace=True)
            data.info()
            data = data.astype({"from": np.int32, "to": np.int32, "label": str})
            df = pd.concat([df, data], axis=0)
            ## Append to vertices.csv
            from_vertices = pd.DataFrame(data, columns=['from'])
            from_vertices['label'] = from_vertex_label
            from_vertices.rename(columns={from_vertices.columns[0]:'id'}, inplace=True)
            from_vertices.drop_duplicates(inplace=True)
            vertices_df = pd.concat([vertices_df, from_vertices], axis=0)
            to_vertices = pd.DataFrame(data, columns=['to'])
            to_vertices['label'] = to_vertex_label
            to_vertices.rename(columns={to_vertices.columns[0]:'id'}, inplace=True)
            to_vertices.drop_duplicates(inplace=True)
            vertices_df = pd.concat([vertices_df, to_vertices], axis=0)
        else:
            print("CSV File %s not exists" % csv_file_path)
    # df = df.astype({"from": np.int32, "to": np.int32, "label": str})
    # df.drop_duplicates(inplace=True)
    # vertices_df = vertices_df.astype({"id": np.int32, "label": str})
    vertices_df.drop_duplicates(inplace=True)
    df.info()
    df.to_csv(OUTPUT_EDGES_PATH, index=False, sep=',', header=None)
    vertices_df.to_csv(OUTPUT_VERTICES_PATH, index=False, sep=',', header=None)

def gen_vertices_csv():
    df = pd.DataFrame(columns=['id', 'label'])
    csv_files = glob.glob(os.path.join(SRC_VERTICES_FOLDER, "*.csv"))
    for file_path in csv_files:
        vertex_name = file_path.split("/")[-1].split("_")[0]
        print(vertex_name)
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, sep='|', encoding='utf-8', usecols=[0])
            data['label'] = vertex_name
            data.rename(columns={data.columns[0]:'id', data.columns[1]:'label'}, inplace=True)
            data.info()
            df = pd.concat([df, data], axis=0)
        else:
            print("CSV File %s not exists" % file_path)
    df = df.astype({"id": np.int32, "label": str})
    df.info()
    df.to_csv(OUTPUT_VERTICES_PATH, index=False, sep=',', header=None)

gen_edges_csv()
# gen_vertices_csv()
