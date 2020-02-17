# Experimenting with DBpedia
We have applied ClassRank over the English chapter of DBpedia and compare the results with many other centrality metrics. All the obtained results are available in this repository. The dump files sused can be dowloaded in the following links:

* [Mapping based objects](http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2)
* [Infobox properties](http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_en.ttl.bz2)
* [Instance types](http://downloads.dbpedia.org/2016-10/core-i18n/en/instance_types_en.ttl.bz2)
* [Infobox properties mapped](http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_mapped_en.ttl.bz2)
* [Persondata](http://downloads.dbpedia.org/2016-10/core-i18n/en/persondata_en.ttl.bz2)
* [Specific mapping base properties](http://downloads.dbpedia.org/2016-10/core-i18n/en/specific_mappingbased_properties_en.ttl.bz2)
* [Topical concepts](http://downloads.dbpedia.org/2016-10/core-i18n/en/topical_concepts_en.ttl.bz2)

## Result files:

We applied different techniques to rank the importance of the classes in the [DBpedia ontology](). 

* [ClassRank](). Json file with a root list which contains elements sorted by its ClassRank score in decreasing order (most important ones at the top). Each class is an object in the list. The classrank score of each class appers associated to the key "CR_score". ClassRank settings: 
  * Damping factor: 0.85.
  * Secutiry thresghold: 0.
  * Class-pointer: rdf:type.
* [PageRank](): Json file. Keys are key URIs pointing to theis PageRank score. The elements are not sorted. PageRank settings:
  * Damping factor: 0.85.

The following JSON files share a common structure. They all contain a list of lists. Each second-level list contains the information associated to a given class with three elements that appear in thie order: class uri, score (the natura of thsi score depends on the technique used) and position in the ranking. The lists are sorted in decreasing order with regard to its rank position (most impostant ones at the top).

* [Instance counting]()
* [Degree]()
* [Betweeness]()
* [Closseness]()
* [Harmonic centrality]()
* [Radiality]()
* [Bridging centraltity]()


