__author__ = "Dani"
from networkx.algorithms import pagerank


def calculate_pagerank(graph, damping_factor=0.85, max_iter=100):
    return pagerank(graph, alpha=damping_factor, max_iter=max_iter)
