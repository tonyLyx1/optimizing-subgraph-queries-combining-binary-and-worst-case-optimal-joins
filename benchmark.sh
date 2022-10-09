#!/bin/bash

LDBC_SCALE=1
LDBC_DATA_PATH=/Users/guanchao/Desktop/Graphs/Graphs/benchmark/Graphflow/LDBC/scale-${LDBC_SCALE}/variant-1/Graphflow
AMAZON_DATA_PATH=/Users/guanchao/Desktop/Graphs/Graphs/benchmark/Graphflow/Amazon0601
ABSOLUTE_DATA_PATH=${LDBC_DATA_PATH}
EDGES_FILE_NAME=edges
VERTICES_FILE_NAME=vertices
DATA_NAME=data

EDGES_FILE_PATH=${ABSOLUTE_DATA_PATH}/${EDGES_FILE_NAME}.csv
VERTICES_FILE_PATH=${ABSOLUTE_DATA_PATH}/${VERTICES_FILE_NAME}.csv
DATA_PATH=${ABSOLUTE_DATA_PATH}/${DATA_NAME}

#PERSON_KNOWS_TRIANGLE="(a)-[KNOWS]->(b),(b)-[KNOWS]->(c),(a)-[KNOWS]->(c)"
##PERSON_KNOWS_TRIANGLE="(a:PERSON)-[KNOWS]->(b:PERSON),(b:PERSON)-[KNOWS]->(c:PERSON),(a:PERSON)-[KNOWS]->(c:PERSON)"
#PERSON_KNOWS_TRIANGLE_WITHOUT_LABEL="(a)->(b),(b)->(c),(a)->(c)"
#BI_QUERY_11="
#  (a)-[KNOWS]->(b),
#  (b)-[KNOWS]->(a),
#  (b)-[KNOWS]->(c),
#  (c)-[KNOWS]->(b),
#  (a)-[KNOWS]->(c),
#  (c)-[KNOWS]->(a),
#  (a)-[ISLOCATEDIN]->(d),
#  (b)-[ISLOCATEDIN]->(e),
#  (c)-[ISLOCATEDIN]->(f),
#  (d)-[ISPARTOF]->(g),
#  (e)-[ISPARTOF]->(g),
#  (f)-[ISPARTOF]->(g)
#"
#BI_QUERY_3="
#  (a)-[HASMODERATOR]->(b),
#  (b)-[ISLOCATEDIN]->(c),
#  (c)-[ISPARTOF]->(d),
#  (a)-[CONTAINEROF]->(e),
#  (f)-[REPLYOF]->(e),
#  (f)-[HASTAG]->(g),
#  (g)-[HASTYPE]->(h)
#"

PERSON_KNOWS_TRIANGLE="(a)-[knows]->(b),(b)-[knows]->(c),(a)-[knows]->(c)"
#PERSON_KNOWS_TRIANGLE="(a:PERSON)-[KNOWS]->(b:PERSON),(b:PERSON)-[KNOWS]->(c:PERSON),(a:PERSON)-[KNOWS]->(c:PERSON)"
PERSON_KNOWS_TRIANGLE_WITHOUT_LABEL="(a)->(b),(b)->(c),(a)->(c)"
BI_QUERY_11="
  (a)-[knows]->(b),
  (b)-[knows]->(a),
  (b)-[knows]->(c),
  (c)-[knows]->(b),
  (a)-[knows]->(c),
  (c)-[knows]->(a),
  (a)-[isLocatedIn]->(d),
  (b)-[isLocatedIn]->(e),
  (c)-[isLocatedIn]->(f),
  (d)-[isPartOf]->(g),
  (e)-[isPartOf]->(g),
  (f)-[isPartOf]->(g)
"
BI_QUERY_3="
  (a)-[hasModerator]->(b),
  (b)-[isLocatedIn]->(c),
  (c)-[isPartOf]->(d),
  (a)-[containerOf]->(e),
  (f)-[replyOf]->(e),
  (f)-[hasTag]->(g),
  (g)-[hasType]->(h)
"

## ## Load Dataset
# Use both edges and vertices data
# JAVA_OPTS='-Xmx500G' python3 ./scripts/serialize_dataset.py ${EDGES_FILE_PATH} ${DATA_PATH} -v ${VERTICES_FILE_PATH} -e ',' -s ','
# Use edges data only
# JAVA_OPTS='-Xmx500G' python3 ./scripts/serialize_dataset.py ${EDGES_FILE_PATH} ${DATA_PATH} -e ','

## Build Catalogue
# JAVA_OPTS='-Xmx500G' python3 ./scripts/serialize_catalog.py ${DATA_PATH} -t 4

## Query Execution
# BI 11
JAVA_OPTS='-Xmx500G' python3 ./scripts/execute_query.py "${BI_QUERY_11}" ${DATA_PATH} -t 1
# BI 3
JAVA_OPTS='-Xmx500G' python3 ./scripts/execute_query.py "${BI_QUERY_3}" ${DATA_PATH} -t 1
# Person Knows Person Triangle
JAVA_OPTS='-Xmx500G' python3 ./scripts/execute_query.py "${PERSON_KNOWS_TRIANGLE}" ${DATA_PATH} -t 1
