# Comorbid-Graphs
A tool for making it easier to compare information using KnowledgeGraphs in neuro-psychology.   
Based on `anytree` (for tree structures) and `networkx` (for graphs).  

Part of the Comorbid project.

<br>

### Table of Contents
* [Getting Started](#getting-started)
    - [ComorbidGraphs-101](#comorbidgraphs-101)
    - [Installation and Setup](#installation-and-setup)
* [Examples](#examples)
    - [Compare Wikipedia articles on DSM-V disorders?](./examples/Wikipedia.ipynb)
    - [Compare DSM-V disorders on symptoms found?](./examples/DSM-V-Symptom.ipynb)
* [Usage](#usage)
    - [Explore](#explore)
    - [Search](#search)
    - [Stats](#stats)
* [Advanced Usage](#advanced-usage)
    - [Advanced Search](#advanced-search)
    - [Stacking](#stacking)
* [Insights](#insights)
    - [Compare By](#compare-by)
    - [SOM](#som)
    - [Pivot Analysis](#pivot-analysis)
* [References](#references)
    - [Software](#software)
    - [Research](#research)
<br><br>

## Getting Started

### ComorbidGraphs 101

For this example you can use one of [data files](https://github.com/DorenCalliku/comorbid-graphs/examples/data) in the docs.

```python
# import libraries needed
import json
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode

with open('example.json') as f:
    data = json.load(f)

# load data - expects a hierarchical tree of the form
# {"name": "Default", "children":[{"name": "Default Child", "children":[]}]}
cg = ComorbidGraph(json_data=data, node_type=ComorbidGraphNode)
```

### Installation and Setup

```bash
pip install git+https://github.com/DorenCalliku/comorbid-graphs
```

## Usage

### Explore

```python
cg.pretty_print_tree()
```

### Search

```python
results = cg.search("depressive disorders")
results.pretty_print_tree()
```

### Stats

```python
cg.stats()
```


## Advanced Usage
Besides the basics, there are some more geeky usages possible for people not searching for only a general picture.
This is the Zoom-In feature which can bring specific results.

### Advanced Search
Making use of this kind of structure makes sense if we can make use of an advanced query for extracting specifically what we want.
This way we can have some actions on these results.

A search is based on `{DIRECTION}_{FILTER}` for making things easier for people to use.

| DIRECTION | Meaning               | Example                                    |
| --------- | --------------------- | ------------------------------------------ |
| inc       | include or filter-in  | `inc_parent:DSM-V`                         |
| exc       | exclude or filter-out | `exc_name: Disorder` exclude all disorders |
| include   | include or filter-in  | `include_parent:DSM-V`                     |
| exclude   | exclude or filter-out | `exclude_title:Disorder`                   |

> **Info: inc and exc**: If a graph is included and excluded, it will be excluded in the end.  

<br>

| FILTER      | Filter inc/                                  | Expects | Strict Match | Example                          | Sorting Order                         |
| ----------- | -------------------------------------------- | ------- | ------------ | -------------------------------- | ------------------------------------- |
| name        | if graph has name/title                      | string  | False        | `inc_name: Disorder`             | `+ 100` per subgraph containing       |
| phrase      | these words are in the body                  | string  | True         | `exc_phrase:developmental`       | `+ 10` per time found in any subgraph |
| type        | if node has type like this                   | string  | True         | `inc_type:section`               | `NaN`                                 |
| text_longer | filter the nodes with text longer than count | int     | True         | `inc_text_longer:300`            | `NaN`                                 |
| ancestor    | if one of ancestors has a name like this     | string  | False        | `inc_ancestor: Phobic`           | `NaN`                                 |
| parent      | if parent has name like this                 | string  | False        | `inc_parent: Neurodevelopmental` | `NaN`                                 |

> **Info: Strict match**: Means if we are checking with `==` or with `contains`.  

> **Warning: parent vs ancestor**: If you write `inc_parent`, this will override `inc_ancestor`

<br>


```python
# Search in 'DSM-V', but exclude all the stuff in 'NeuroDevelopmental Disorders' subgraph
# for documents containing phrases like 'anxiety', and 'Disorder' in titles
# also, the text should be better than 300 chars.
# Dont return stuff that match partially.

results = cg.advanced_search("""
anxiety

inc_parent:DSM-V
inc_title:Disorder
inc_text_longer:300

exc_ancestor:Neurodevelopmental Disorders
""", full_match=True)

results.pretty_print_tree()
```

#### Stacking

You can stack results together.

```python
# What is the extent of depression in DSM-V? Include all of the depressive disorders.

results = cg.advanced_search("""
depressive, depression, low mood
inc_type:document
inc_ancestor:DSM-V
exc_ancestor:Depressive Disorders

MERGE

inc_type:document
inc_ancestor:Depressive Disorders
""", full_match=True)

results.pretty_print_tree()
```

## Insights


### Compare by  
Usage of `groupby` to compare 1-1 sections or documents.   


### SOM
Self-Organizing-Maps for Comorbid Graphs
```python
cg.som()
```
[SOM](docs/imgs/som.png)

### Pivot Analysis



## References

### Software
- [Anytree](https://anytree.readthedocs.io/en/latest/index.html)
- [Networkx](https://networkx.org/)

### Research