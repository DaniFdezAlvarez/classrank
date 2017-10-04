__author__ = "Dani"
from networkx.algorithms import pagerank


def calculate_pagerank(graph, damping_factor=0.85):
    return pagerank(graph, alpha=damping_factor)
