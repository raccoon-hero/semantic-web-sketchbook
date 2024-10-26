# ЗАВДАННЯ 2
# __________________
# Використовуючи бібліотеки RdfLib, SPARQLWrapper та відкритий endpoint 
# написати Python-скрипт, який буде повертати основні типи захворювань, 
# які відносяться до гастроенерології (Gastroenterology) і чим вони зазвичай викликані.

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?disease ?diseaseLabel (GROUP_CONCAT(DISTINCT ?causeLabel; separator=" | ") AS ?causes)
WHERE {
  ?disease a dbo:Disease .

  ?disease dct:subject ?category .
  ?category skos:broader* <http://dbpedia.org/resource/Category:Diseases_of_oesophagus,_stomach_and_duodenum> .

  ?disease rdfs:label ?diseaseLabel .
  FILTER (LANG(?diseaseLabel) = "uk")

  OPTIONAL {
    ?disease dbo:medicalCause ?cause .
    ?cause rdfs:label ?causeLabel .
    FILTER (LANG(?causeLabel) = "uk")
  }
}
GROUP BY ?disease ?diseaseLabel
"""

sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

print("Гастроенерологічні захворювання та можливі причини появи:\n")
for result in results["results"]["bindings"]:
    disease_name = result["diseaseLabel"]["value"]
    causes = result["causes"]["value"] if "causes" in result and result["causes"]["value"].strip() else "Не знайдено джерело"
    print(f"Захворювання: {disease_name}\nПричина появи: {causes}\n")