#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install matplotlib
#!pip install .


# In[2]:
import json
import matplotlib.pyplot as plt

from anytree import PostOrderIter, RenderTree
from comorbid_graphs import ComorbidGraph, ComorbidGraphNode


# ### Creating graph 

# In[3]:


with open('tests/fixtures/symp_tree.json') as f:
    data = json.load(f)
cg = ComorbidGraph(data, ComorbidGraphNode, assign_ids=True)
node_content = [i for i in PostOrderIter(cg.tree) if hasattr(i, 'body')][0]

# In[4]:


# print(cg.pretty_print_tree()[:500])
# print('...')


# ## Searching
# Searching should be extensible to allow sql search for larger data than KGs.
# For this we have a many step search.
# - search for ancestors, parents first
#   - get the names of these, include-exclude
#   - merge all of the nodes, merging with include-exclude
# - for docs in the ending KnowledgeGraph
#   - filter by type
#   - filter by body length
# - search in the body

# ### 1. Filtering
# Filter based on node properties if included or not - `name`, `parent`, `type`, `body-length`, `content`.
# 

# In[5]:
def test_filtering():

    assert cg.tree._filter_name(['Source'], [])
    assert cg.tree.children[0]._filter_parent(['Source'],[])
    assert cg.tree._filter_type(['default'],[])

    # text-length checks
    # check first node that has no content
    assert not cg.tree._filter_text_length([0],[])

    # check a node with content
    assert node_content._filter_text_length([0],[])
    assert node_content._filter_content([node_content.body],[])


# ### 2. Content
# Filtering the body for keywords.
# But it shouldnt be like the previous case, because loading the body of many of these guys will tire the machine - so will have to allow a filtering done by an en engine (like `sqlite`-engine) which are optimized for these kinds of updates.

# In[6]:

def test_lbl_filter():
    assert node_content.apply_lbl_content_filter(
        {"content": {"inc":[node_content.body], "exc":[]}}
    )


# ### 3. Subgraph
# Filter the `ancestors`, and use `inc-exc` to zoom in.

# In[7]:

subgraph = cg.filter_subgraph(
    inc_list=['nervous system'], exc_list=['pain'], node_type=ComorbidGraphNode, base_name='subgraph results'
)
def test_subgraph():
    for pre, fill, node in RenderTree(subgraph):
        if hasattr(node, 'old_parent') and hasattr(node.old_parent, 'name'):
            print("%s%s - %s" % (pre, node.name, node.old_parent.name))
        else:
            print("%s%s" % (pre, node.name))


# In[8]:

def test_merge_into_tree():
    nodes_list = set([i for i in PostOrderIter(subgraph)])- set([subgraph])
    result_node = cg.merge_nodes_into_tree(nodes_list, node_type=ComorbidGraphNode)
    # print(result_node)
    for pre, fill, node in RenderTree(result_node):
        if hasattr(node, 'old_parent') and hasattr(node.old_parent, 'name'):
            print("%s%s - %s" % (pre, node.name, node.old_parent.name))
        else:
            print("%s%s" % (pre, node.name))


# ## Searchable
# Create the search language by allowing all entries.   
# Control for inputs irregularities and more.

# In[21]:

def test_advanced_search():
    query_str = """
    inc_name:symptom,ache
    inc_ancestor:symptom
    """
    print()
    print(cg.build_query(query_str))
    print()

    result_cg = cg.advanced_search(query_str, node_type=ComorbidGraphNode, with_children=True)
    print(result_cg.pretty_print_tree())
# test case - check if search is complementary
# disorder = 6
# disease = 18
# disorder-disease = 4
# disease-disorder = 16
# disorder+disease = 22
# passed? yes


# ## Ordering Results
# There should be two options - first the graph properties.  
# Second our simple algorithm based on combination of scores - as found in `comorbid-lab`.

# In[ ]:


