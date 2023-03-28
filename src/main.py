import argparse
from random import random, randint
from itertools import product, combinations

from graph import *
from algorithms import pa_bfs, pa_kl, pa_fm, pa_sb, pa_scc_kl

set_logger('logs/')


def generate_graph(n, p, directed=True,):
    g = Graph()
    for idx in range(n):
        g.addVertex(idx)
    possible_edges = product(
        range(n), repeat=2) if directed else combinations(range(n), 2)
    for u, v in possible_edges:
        if random() < p:
            weight = randint(1, 2*n)
            g.addEdge(u, v, weight)
            if not directed:
                g.addEdge(v, u, weight)
    return g


if __name__ == '__main__':
    # Configure logging
    FORMAT = '%(asctime)s.%(msecs)03d %(message)s'
    logging.basicConfig(format=FORMAT, datefmt='%H:%M:%S')
    parser = argparse.ArgumentParser(
        description="Compute the partition of a graph.")

    # for generating graph randomly
    parser.add_argument('--number_nodes', '-n',
                        help='Total nodes of graph', type=int, default=10)
    parser.add_argument(
        '--edge_prob', '-p', help='Probability for choose edge', type=float, default=0.5)
    parser.add_argument('--is_directed', '-d',
                        help='Probability for choose edge', type=bool, default=False)

    # for performing algorithms
    parser.add_argument(
        '--threshold', '-t', help='Threshold for BFS partitioning', type=int, default=3)
    parser.add_argument(
        '--algorithm', '-a', type=str, help='Algorithm for compute the partition of a graph.'
        'bfs: Breadth First Search, kl: Kerninghan-Lin (KL) algorithm, fm: Fiduccia-Mattheyses (FM) algorithm, sb: Spectral Bisection', default='bfs')

    args = parser.parse_args()
    print(args)

    g = generate_graph(args.number_nodes, args.edge_prob, args.is_directed)

    logging.info('Performing graph partition algorithm')
    if args.algorithm == 'bfs':
        group_a, group_b = pa_bfs(g, vertex_ith=0, threshold=args.threshold)
    elif args.algorithm == 'kl':
        cutset_size, group_a, group_b = pa_kl(g)
    elif args.algorithm == 'fm':
        cutset_size, group_a, group_b = pa_fm(g)
    elif args.algorithm == 'sb':
        group_a, group_b = pa_sb(g)
    elif args.algorithm == 'scc_kl':
        group_a, group_b = pa_scc_kl(g)
    else:
        logging.warning('Algorithm not supported')
