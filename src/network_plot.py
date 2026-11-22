import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def plot_network(nodes, edges, dept_id, R, out_path):
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    pos = nx.spring_layout(graph, seed=R, k=1.1 / max(1, len(nodes)) ** 0.5,
                           iterations=150)

    fig, ax = plt.subplots(figsize=(11, 9))
    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_size=360 if len(nodes) < 30 else 230,
        node_color="#1687c9", edgecolors="white", linewidths=0.7
    )
    nx.draw_networkx_labels(
        graph, pos, ax=ax, font_size=8 if len(nodes) < 30 else 6,
        font_color="black"
    )
    nx.draw_networkx_edges(
        graph, pos, ax=ax, arrows=True, arrowstyle="-|>", arrowsize=10,
        width=0.65, edge_color="#333333", alpha=0.65,
        connectionstyle="arc3,rad=0.04",
        min_source_margin=8, min_target_margin=10
    )
    ax.set_title(
        f"Directed Email Network — Department {dept_id} (R = {R})\n"
        f"{graph.number_of_nodes()} nodes, {graph.number_of_edges()} directed edges"
    )
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
