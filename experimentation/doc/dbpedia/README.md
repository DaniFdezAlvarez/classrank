# Experimenting with DBpedia
We have applied ClassRank over the English chapter of DBpedia and compared the results with many other centrality metrics. The dump files used can be dowloaded in the following links:

* [Mapping based objects](http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2)
* [Infobox properties](http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_en.ttl.bz2)
* [Instance types](http://downloads.dbpedia.org/2016-10/core-i18n/en/instance_types_en.ttl.bz2)
* [Infobox properties mapped](http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_mapped_en.ttl.bz2)
* [Persondata](http://downloads.dbpedia.org/2016-10/core-i18n/en/persondata_en.ttl.bz2)
* [Specific mapping base properties](http://downloads.dbpedia.org/2016-10/core-i18n/en/specific_mappingbased_properties_en.ttl.bz2)
* [Topical concepts](http://downloads.dbpedia.org/2016-10/core-i18n/en/topical_concepts_en.ttl.bz2)

## Mining logs

We have mined log files of the official DBpedia SPARQL endpoint for detecting class mentions in SPARQL queries consider that a class is mentioned when:

* The URI of the class is mentioned.
* The URI of an instance of the class is mentioned.
* The URI of an element _e_ used in a triple with a property whose domain/range forces _e_ to be an instance of a class is mentioned. 

We generated two different files with mining results. These files are tsv where the different type of class mentions are annotated:
* [Total results](total_result.tsv): Class mentions in all entries in the logs.
* [Human results](human_result.tsv): Class mentions of those entries in the logs associated to IPS whose petition rate has been associated to human agents. 

### Logs
The logs minned can be dowloaded at the following link:
* [DBpedia log files](http://156.35.94.8/classrank/logs/dbpedia-2017-10-logs.zip), provided by OpenLink. These files are provided under a CC-BY-SA license (credits to OpenLink). The license is available in the download link.

Please, contact the authors if you experiment any issue when dowloading the logs. 

The logs contain 14 files of queries thrown against the SPARQL endponit of DBpedia run by Openlink. Each file contain the acceses to the endpoint during a whole day in a random date of 2017. Each file is named after its date with the following pattern: access.log-YYYYmmdd.zip, where YYYY means year, mm month, and dd day.
   
## Result files:

We applied different techniques to rank the importance of the classes in the [DBpedia ontology](dbo.ttl). 

* [ClassRank](classrank_dbpedia_rdftype.json). Json file with a root list which contains elements sorted by its ClassRank score in decreasing order (most important ones at the top). Each class is an object in the list. The classrank score of each class appers associated to the key "CR_score". ClassRank settings: 
  * Damping factor: 0.85.
  * Secutiry thresghold: 0.
  * Class-pointer: rdf:type.

The following JSON files share a common structure. They all contain a list of lists. Each second-level list contains the information associated to a given class with three elements that appear in thie order: class uri, score (the natura of thsi score depends on the technique used) and position in the ranking. Some lists include also an internal ID in the fourth position, which is usually the class URI again. The lists are sorted in decreasing order with regard to its rank position (most impostant ones at the top).

* [ClassRank](cr_dbpedia_labelled_comparable.json).
* [Adapted ClassRank](cr_adapted_dbpedia_labelled_comparable.json).
* [PageRank AAT](pagerank_ranking_dbpedia.json). Damping factor: 0.85.
* [PageRank OTT](pagerank_ott_dbpedia_labelled_comparable.json). Damping factor: 0.85.
* [Adapted PageRank AAT](pagerank_adapted_classes_dbpedia_labelled_comparable.json). Damping factor: 0.85.
* [Adapted PageRank OTT](pagerank_ott_adapted_dbpedia_labelled_comparable.json). Damping factor: 0.85.
* [HITS AAT](hits_classes_dbpedia_labelled_comparable.json).
* [HITS OTT](hits_ott_dbpedia_labelled_comparable.json).
* [Adapted HITS AAT](hits_adapted_classes_dbpedia_labelled_comparable.json).
* [Adapted HITS OTT](hits_ott_adapted_dbpedia_labelled_comparable.json).
* [Instance counting](instance_counting_dbpedia.json)
* [Degree](deg_dbo_onto.json)
* [Betweeness](betw_dbo_onto.json).
* [Closseness](clos_dbo_onto.json)
* [Harmonic centrality](harm_dbo_onto.json)
* [Radiality](rad_dbo_onto.json)
* [Bridging centraltity](bridging_dbo_onto.json)
* [Adapted degree](adapted_deg_dbo_onto.json)
* [Adapted betweeness](adapted_betw_dbo_onto.json).
* [Adapted harmonic centrality](adapted_harm_dbo_onto.json)
* [Adapted radiality](adapted_rad_dbo_onto.json)
* [Adapted bridging centraltity](adapted_bridging_dbo_onto.json)

## Comparison
We have compared each technique with the mining files (totals and just human log entries) using Ranking Biased Overlap giving different importance to different prefix length of each ranking. The results of this comparison are avaiable to dowload in [a csv file](comparison_all.csv). The file contains different structures of CSV values (tip: do not parse, explore first with any spreadsheet software to keep one of the csv structures).


