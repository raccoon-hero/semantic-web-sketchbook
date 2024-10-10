from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF, RDF, XSD

graph = Graph()

EX = Namespace("http://example.org/")
SCHEMA = Namespace("https://schema.org/")
DBPEDIA = Namespace("http://dbpedia.org/resource/")

graph.bind("ex", EX)
graph.bind("foaf", FOAF)
graph.bind("schema", SCHEMA)
graph.bind("dbpedia", DBPEDIA)

def add_fact(subject, predicate, value, lang="uk", graph = graph):
    if predicate == RDF.type:
        graph.add((subject, predicate, Literal(value)))
        return
    graph.add((subject, predicate, Literal(value, lang=lang)))

def add_fact_custom_literal(subject, predicate, literal, graph = graph):
    graph.add((subject, predicate, literal))

cade = URIRef(EX.Cade)
add_fact(cade, RDF.type, FOAF.Person)
add_fact(cade, FOAF.firstName, "Кейд")
add_fact(cade, SCHEMA.address, "1516 Henry Street, Берклі, Каліфорнія 94709, США")

cade_bachelors_degree = URIRef(EX.CadesBachelorsDegree)
add_fact(cade_bachelors_degree, RDF.type, SCHEMA.EducationalOccupationalCredential, lang="en")
add_fact(cade_bachelors_degree, SCHEMA.credentialCategory, "Бакалавр")
add_fact_custom_literal(cade_bachelors_degree,
                        SCHEMA.dateAwarded, 
                        Literal("2011", datatype=XSD.gYear))
add_fact(cade_bachelors_degree, SCHEMA.awardee, cade)
add_fact(cade_bachelors_degree, SCHEMA.educationalInstitution, "Каліфорнійський університет")

add_fact(cade, FOAF.interest, "Птахи")
add_fact(cade, FOAF.interest, "Екологія")
add_fact(cade, FOAF.interest, "Довкілля")
add_fact(cade, FOAF.interest, "Фотографія")
add_fact(cade, FOAF.interest, "Подорожі")
# [ПИТАННЯ]: DBPEDIA можна додавати лише англійською?
add_fact(cade, EX.visited, DBPEDIA.Canada, lang="en")
add_fact(cade, EX.visited, DBPEDIA.France, lang="en")

emma = URIRef(EX.Emma)
add_fact(emma, RDF.type, FOAF.Person)
add_fact(emma, FOAF.firstName, "Емма")
add_fact(emma, SCHEMA.address, "Carrer de la Guardia Civil 20, 46020 Valencia, Spain", lang="en")

emma_masters_degree = URIRef(EX.EmmasMastersDegree)
add_fact(emma_masters_degree, RDF.type, SCHEMA.EducationalOccupationalCredential, lang="en")
add_fact(emma_masters_degree, SCHEMA.credentialCategory, "Магістр")
add_fact_custom_literal(emma_masters_degree,
                        SCHEMA.dateAwarded, 
                        Literal("2015", datatype=XSD.gYear))
add_fact(emma_masters_degree, SCHEMA.awardee, emma)
add_fact(emma_masters_degree, SCHEMA.educationalInstitution, "Університет Валенсії")

add_fact(emma, EX.hasExpertiseIn, DBPEDIA.Waste_management, lang="en")
add_fact(emma, EX.hasExpertiseIn, DBPEDIA.Hazardous_waste, lang="en")
add_fact(emma, EX.hasExpertiseIn, DBPEDIA.Air_pollution, lang="en")

add_fact(emma, FOAF.interest, "Їзда на велосипеді")
add_fact(emma, FOAF.interest, "Музика")
add_fact(emma, FOAF.interest, "Подорожі")
add_fact(emma, EX.visited, DBPEDIA.Portugal, lang="en")
add_fact(emma, EX.visited, DBPEDIA.Italy, lang="en")
add_fact(emma, EX.visited, DBPEDIA.France, lang="en")
add_fact(emma, EX.visited, DBPEDIA.Germany, lang="en")
add_fact(emma, EX.visited, DBPEDIA.Denmark, lang="en")
add_fact(emma, EX.visited, DBPEDIA.Sweden, lang="en")

add_fact(cade, FOAF.knows, emma)

cade_emma_meeting = URIRef(EX.MeetingEmma)
add_fact(cade_emma_meeting, RDF.type, SCHEMA.Event)
add_fact(cade_emma_meeting, SCHEMA.location, DBPEDIA.Paris, lang="en")
add_fact_custom_literal(cade_emma_meeting, 
                        SCHEMA.startDate,
                        Literal("2014-08", datatype=XSD.gYearMonth))
add_fact(cade_emma_meeting, SCHEMA.attendee, cade)
add_fact(cade_emma_meeting, SCHEMA.attendee, emma)

# "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig", "nquads", "json-ld" and "hext"
graph.serialize(destination="results/cade_emma_graph.xml", format="xml")
graph.serialize(destination="results/cade_emma_graph.n3", format="n3")
graph.serialize(destination="results/cade_emma_graph.ttl", format="turtle")
graph.serialize(destination="results/cade_emma_graph.rdf", format="pretty-xml")
graph.serialize(destination="results/cade_emma_graph.nt", format="nt")
# graph.serialize(destination="results/cade_emma_graph.xml", format="trix")
graph.serialize(destination="results/cade_emma_graph.trig", format="trig")
# graph.serialize(destination="results/cade_emma_graph.nq", format="nquads")
graph.serialize(destination="results/cade_emma_graph.jsonld", format="json-ld")
graph.serialize(destination="results/cade_emma_graph.hext", format="hext")

print("\nУсі трійці у графі:")
for s, p, o in graph:
    print(f"{s} {p} {o}")

print("\nУсі трійці Емми:")
for s, p, o in graph.triples((emma, None, None)):
    print(f"{s} {p} {o}")

print("\nУсі трійці з іменами людей:")
for s, p, o in graph.triples((None, FOAF.firstName, None)):
    print(f"{s} {p} {o}")