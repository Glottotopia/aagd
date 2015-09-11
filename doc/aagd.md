## install
 docker
 zip 

## use
### search
The basic use of the AAGD platform is to search for examples. The main search field allows you to search for English or vernacular words and glosses. In order to search for other fields, use a colon, e.g. "polarity:situation_negative".

Inline-style: 
![Domains](https://github.com/Glottotopia/aagd/blob/master/doc/img/domains.png "Domains")


On the right hand side, you see a number of sorted tags for the result of your search. The numbers after the tags indicate how many documents in the result set bear the particular tags. By clicking on these tags, you can further restrict your search, yielding a more constrained set. The currently active constraints are listed on the top right in red.


![Constraints](https://github.com/Glottotopia/aagd/blob/master/doc/img/constraints.png "Constraints")


By clicking on the red constraints, you can remove them. By adding and removing constraints, you can customize the result set according to your needs.

The examples matching your constraints are given in the middle. In the standard view, you see only the vernacular sentence and its translation.

![standard view](https://github.com/Glottotopia/aagd/blob/master/doc/img/standardview.png "Standard view")

By clicking on [expand], you can display the interlinear glosses and tags as well. By clicking again, you can hide those elements.


![expanded view](https://github.com/Glottotopia/aagd/blob/master/doc/img/constraints.png "Expanded view")


### annotate
 In order to add or remove tags, you have to be logged in as an annotator. Tags are grouped according to domains, or instance, `polarity:negative` and `polarity:positive`. The standard interface for adding tags presents a list of these domains. In order to open this list, click on [add tags]. The list will appear on the right. Select a tag from a domain to add it. The tag list below your example will be updated. 
 
 
![add tags](https://github.com/Glottotopia/aagd/blob/master/doc/img/addtags.png "Add tags")
 
 If you cannot remember the domain of a tag, you can also use the tab [free]. This will give you a box where you can search for (parts of) tag names. To add a tag from the query result to your example, click on it. 
 
 
![freetags](https://github.com/Glottotopia/aagd/blob/master/doc/img/freetags.png "Add tags via search box")

 To remove a tag from an example, select [delete] from the tag's dropdown list below the example.
 Using this dropdown list, you can also star tags, signalling that this exmaple is particularly valuable for didactic purposes relating to that tag. 
 
 
![remove tags](https://github.com/Glottotopia/aagd/blob/master/doc/img/removetags.png "Remove tags")
 
 Finally, there is a green flag towards the bottom of the example. You can turn it red by clicking on it. The semantics you want to associate with the flag are up to you. 
 
 
![flag](https://github.com/Glottotopia/aagd/blob/master/doc/img/flag.png "Flag")
 
### change translation
  As a first step towards changing the content online, you can correct typos in examples. Doubleclick on an example to make it editable. Change as desired and click [Save].
  
  
![change translation](https://github.com/Glottotopia/aagd/blob/master/doc/img/changetranslation.png "Change translation")

  
## read additional information 
 the database focuses on example sentences and their properties. More extensive information can be found in the wiki. You can find links to the wiki on the navibar at the top, e.g. the link [languages].
 
 You can edit the content in the wiki if your administrator gives you the necessary privileges. For information about how to edit the wiki, see the wiki's help pages. One particular aspect is not covered there: how to pull an example from the database to the wiki: use <<Anchor(ExampleID)>>, and the example will be fetched at the very place. Javascript has to be enabled in your browser for this to work. 

