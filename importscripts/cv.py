from athautils import EAF, Language

eaf = EAF("UT/ANLC0878a_mt_puberty-draft131004.eaf-elan-utterance.xml", language=Language("Upper Tanana", "tau", "63.1377,-142.5244"))
eaf.parse() 
eaf.eaf2solr()