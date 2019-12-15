"""DataScience Assignment 4 - Fabrice Normandin, ID 20142128

Graph ML
"""
# This set of assingments will teach you the differences between various node representations in graphs.
# Note that all questions are programming assingments but you do not need to use loss function to optimize the claculation of thesee embeddings.


import numpy as np
import itertools
import random

from typing import *


"""
1- (5 points) Write a function randadjmat(n,p) in Python which
returns an adjacency matrix for a "random graph" on n vertices.
Here p is the probability of having an edge between any pair of vertices.
"""


def randadjmat(n: int, p: float) -> np.ndarray:
    return random_connected_adjacency_matrix(n, p)


def random_adjacancy_matrix(n: int, p: float) -> np.ndarray:
    """Returns an adjacency matrix for a "random graph" on n vertices.
    NOTE: the graph might contain some isolated nodes with no edges.

    Args:
        n (int): The number of vertices in the graph.
        p (float): The probability of having an edge between any pair of vertices.

    Returns:
        np.ndarray: The resulting adjacency matrix. (a bool ndarray of shape [n,n])
    """
    adjacency_matrix = np.zeros([n, n], dtype=bool)
    for (i, j) in itertools.permutations(range(n), 2):
        if random.random() < p:
            adjacency_matrix[i, j] = adjacency_matrix[j, i] = True
    return adjacency_matrix


def node_degrees(adjacency_matrix: np.ndarray) -> np.ndarray:
    return np.sum(adjacency_matrix, axis=1)

def random_connected_adjacency_matrix(n: int,
                                      p: float,
                                      max_attempts=1000) -> np.ndarray:
    """Attempts to return an adjacency matrix for a random graph of n vertices
    where all nodes have degree >= 1. If we are unable to produce such a graph
    after `max_attempts` iterations, a RuntimeError is raised.
    
    Args:
        n (int): The number of vertices in the graph.
        p (float): The probability of having an edge between any pair of vertices.

    Returns:
        np.ndarray: The resulting adjacency matrix. (an ndarray of shape [n,n]
         and dtype bool)
    """
    assert 0 < p < 1
    adjacency_matrix = random_adjacancy_matrix(n, p)
    for i in range(max_attempts):
        if np.all(node_degrees(adjacency_matrix) != 0):
            # print(f"succeded after {i} attempts")
            return adjacency_matrix
        adjacency_matrix = random_adjacancy_matrix(n, p)
    raise RuntimeError(
        f"Unable to create an adjacency matrix for n={n} and p={p} without any "
        f"disconnected nodes after {max_attempts} attempts."
    )


"""
2- (5 points) Write a function transionmat(A) which, given an adjacency matrix
 A, generate a transition matrix T where probability of each edge (u,v) is
 calculated as 1/degree(u).
"""

def transionmat(A: np.ndarray) -> np.ndarray:
    transition_matrix = np.copy(A).astype(float)
    assert np.array_equal(transition_matrix, transition_matrix.T)

    degrees = np.sum(transition_matrix, axis=1)
    assert np.all(degrees != 0), "adjacency matrix contains nodes of degree 0!"

    nonzero_indices = np.nonzero(adjacency_matrix)
    for (u, v) in zip(*nonzero_indices):
        transition_matrix[u, v] = 1 / degrees[u]

    assert np.all(np.isclose(np.sum(transition_matrix, axis=1), 1))
    return transition_matrix



"""
3- (5 points) Write a function hotembd(A) which, given an adjacency matrix A,
generate an embedding matrix H where each node is represetned with a 1-hot
 vector.
"""

def hotembd(A: np.ndarray) -> np.ndarray:
    """given an adjacency matrix A, generate an embedding matrix H where each node
     is represetned with a 1-hot vector.

    Args:
        A (np.ndarray): An adjacency matrix

    Returns:
        np.ndarray: An Embedding matrix
    """
    return one_hot_embedding_matrix(adjacency_matrix=A)


def one_hot_embedding_matrix(adjacency_matrix: np.ndarray) -> np.ndarray:
    # TODO: not sure about this one, each node becomes a one-hot vector?
    # How is that different than just the identity?
    return np.identity(adjacency_matrix.shape[0], dtype=int)

"""
4- (5 points) Write a function randwalkemb(A,k) which, given an adjacency 
matrix A, a transition matrix T, and one-hot encoding H, performs random 
walks on the graph from each node w times with lenght equal to l and generate 
an embedding matrix for each node based on the sum of 1-hot encodings of all 
nodes that are visited during the walks.
"""

def randwalkembd(A, T, H, w, l):
    return random_walk_embedding(
        adjacency_matrix=A,
        transition_matrix=T,
        embedding_matrix=H,
        num_walks=w,
        walk_length=l
    )


def random_walk_embedding(adjacency_matrix: np.ndarray,
                          transition_matrix: np.ndarray,
                          embedding_matrix: np.ndarray,
                          num_walks: int,
                          walk_length: int) -> np.ndarray:
    """given an adjacency matrix A, a transition matrix T, and one-hot 
    encoding H, performs random walks on the graph from each node w times with 
    length equal to l and generate an embedding matrix for each node based 
    on the sum of 1-hot encodings of all nodes that are visited during the 
    walks.

    Args:
        adjacency_matrix (np.ndarray): The adjacency matrix
        transition_matrix (np.ndarray): The transition matrix
        embedding_matrix (np.ndarray): The one-hot embedding matrix
        num_walks (int): The number of random_walks
        walk_length (int): The length of each of the random walks

    Returns:
        np.ndarray: An embedding matrix for each node, based on the sum of the 
        embeddings of all the nodes visited during the walks.
    """
    n = adjacency_matrix.shape[0]
    visited_nodes = np.zeros([walk_length * num_walks, n], dtype=int)

    initial_seed = 123
    for walk in range(num_walks):
        # reset the state to be at the starting nodes:
        state = np.arange(n, dtype=int)
        # use a different seed everytime, otherwise we'll get the same results 
        # on each walk.
        np.random.seed(initial_seed + walk)

        for step in range(walk_length):
            # take a random step
            # TODO: figure out a way to vectorize this.
            for i in range(n):
                state[i] = np.random.choice(n, p=transition_matrix[state[i]])
            # store the visited node.
            visited_nodes[walk * walk_length + step, :] = state
    
    sum_of_embeddings = np.sum(embedding_matrix[visited_nodes], axis=0)
    return sum_of_embeddings

"""
5- (5 points) Write a function hopeneighbormbd(A,H,k) which, given an 
adjacency matrix A, and one-hot node encoding matrix H, generates node 
embedding matrix which represents each node as sum of 1-hot encodings of 
k-hops neighbors.
"""

def hopeneighbormbd(A, H, k):
    return k_hop_neighbours_embeddings(
        adjacency_matrix=A,
        embedding_matrix=H,
        k=k
    )

def k_hop_neighbours_embeddings(adjacency_matrix: np.ndarray,
                                embedding_matrix: np.ndarray,
                                k: int) -> np.ndarray:
    """given an adjacency matrix A, and one-hot node encoding matrix H, 
    generates node embedding matrix which represents each node as sum of 1-hot 
    encodings of k-hops neighbors. 
    
    Args:
        adjacency_matrix (np.ndarray): The adjacency matrix
        embedding_matrix (np.ndarray): The one-hot encoding matrix
        k (int): The number of hops
    
    Returns:
        np.ndarray: The resulting embedding matrix.
    """
    k_hop_neighbours = np.linalg.matrix_power(adjacency_matrix, k)
    return k_hop_neighbours @ embedding_matrix


"""
6- (5 points) Write a function similarnodes(Z) which, given an node embedding 
matrix, find the most similar nodes in the graph. 
"""

def similarnodes(Z: np.ndarray) -> np.ndarray:
    return similar_nodes(
        node_embeddings=Z,
        similarity_func=cosine_similarity
    )


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculates the cosine similarity (dot product) between the two unit 
    vectors.
    
    Args:
        v1 (np.ndarray): a vector
        v2 (np.ndarray): another vector
    
    Returns:
        float: the cosine similarity between the vectors.
    """
    assert len(v1.shape) == len(v2.shape) == 1
    return v1.dot(v2)


def l2_distance(v1: np.ndarray, v2: np.ndarray) -> float:
    diff = v1 - v2
    return diff.dot(diff)


def similar_nodes(node_embeddings: np.ndarray,
                  similarity_func: Callable[[np.ndarray, np.ndarray], float]
                 ) -> np.ndarray:
    """given an node embedding matrix, find the most similar nodes in the graph.
    
    Args:
        node_embeddings (np.ndarray): The node embeddings (will be normalized,
        such that each row will sum to 1)
    
    Returns:
        np.ndarray: For each node, another node of the graph which is most 
        similar to it.
    """
    from itertools import permutations
    n = node_embeddings.shape[0]
    row_mag = np.sum(node_embeddings ** 2, axis=1, keepdims=True)

    # take care of zero embeddings.
    if np.any(np.isclose(row_mag, 0)):
        zero_embedding_indices = np.nonzero(np.isclose(row_mag, 0))[0]
        row_mag[zero_embedding_indices] = 1

    node_embeddings = node_embeddings / row_mag

    # NOTE: here, the similarity of a note to itself is marked as -1.
    similarities = - np.identity(n, dtype=float)
    for (i, emb_i), (j, emb_j) in permutations(enumerate(node_embeddings), 2):
        similarities[i,j] = similarities[j,i] = similarity_func(emb_i, emb_j)
    
    return np.argmax(similarities, axis=0)

"""
7- (10 points) generate a random graph where n=20, and p=0.6, and compare the 
most similar nodes in the graph using randwalkembd (l=4, w=10), 
hopeneighbormbd (k=1) and hopeneighbormbd (k=2).
Justify why similar nodes are different using different node embeddings?
"""

# because the different embedding method capture different scales of structure of the input graph.
# Therefore, under different embedding schemes, nodes can have different closest relatives in the embedding space.

adjacency_matrix = random_connected_adjacency_matrix(20, 0.6)
w = 10
l = 4
print(f"Adjacency Matrix: \n {adjacency_matrix.astype(int)}")
transition_matrix = transionmat(adjacency_matrix)
embedding_matrix = one_hot_embedding_matrix(adjacency_matrix)

random_embeddings = randwalkembd(
    adjacency_matrix,
    transition_matrix,
    embedding_matrix,
    w=w,
    l=l,
)
print("Random walk embeddings:\n", random_embeddings)
one_hop_embeddings = hopeneighbormbd(adjacency_matrix, embedding_matrix, k=1)
print("One hop embeddings:\n", one_hop_embeddings)
two_hop_embeddings = hopeneighbormbd(adjacency_matrix, embedding_matrix, k=2)
print("Two hop embeddings:\n", two_hop_embeddings)

print("Similar Nodes:")
# Each list here represents, for each node, the index of the most similar node in the graph.
print(f"Random walk embedding (cosine similarity, w={10}, l={4}):")
print(similar_nodes(random_embeddings,  cosine_similarity))
print(f"One-hop embeddings (cosine similarity):")
print(similar_nodes(one_hop_embeddings, cosine_similarity))
# the nodes have almost all the same two-hop neighbours, since the graph is highly connected.
print(f"Two-hop embeddings (cosine similarity):")
print(similar_nodes(two_hop_embeddings, cosine_similarity))

print(f"Random walk embedding (L2 distance, w={10}, l={4}):")
print(similar_nodes(random_embeddings,  l2_distance))
print(f"One-hop embeddings (L2 distance):")
print(similar_nodes(one_hop_embeddings, l2_distance))
print(f"Two-hop embeddings (L2 distance):")
print(similar_nodes(two_hop_embeddings, l2_distance))