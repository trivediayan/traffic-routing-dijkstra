import pandas as pd
import networkx as nx
import os
import matplotlib
# Use non-interactive backend to prevent CLI blocking or window-manager dependency issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ALPHA = 1.5

# Absolute path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nodes_path = os.path.join(BASE_DIR, "nodes.csv")
edges_path = os.path.join(BASE_DIR, "edges.csv")

nodes = pd.read_csv(nodes_path)
edges = pd.read_csv(edges_path)

G = nx.DiGraph()

for _, row in nodes.iterrows():
    G.add_node(int(row['node_id']), name=row['name'])

for _, row in edges.iterrows():
    length_m = float(row['length_m'])
    speed = float(row['speed_limit_kmph'])
    capacity = float(row['capacity'])
    load = float(row['current_load'])

    base_time = length_m / (speed * 1000 / 3600)

    if capacity <= 0:
        multiplier = 9999.0  # road closed
    else:
        ratio = load / capacity
        multiplier = 1.0 + ALPHA * max(0.0, ratio - 1.0)

    travel_time = base_time * multiplier

    G.add_edge(int(row['from']), int(row['to']),
               length_m=length_m,
               speed_kmph=speed,
               capacity=capacity,
               current_load=load,
               time=travel_time)


source = 1   # College
target = 4   # Station

path = nx.shortest_path(G, source=source, target=target, weight='time')
total_time = nx.shortest_path_length(G, source=source, target=target, weight='time')

path = [int(x) for x in path]
print(f"Best path (considering congestion): {path}")
print(f"Estimated travel time: {total_time:.2f} seconds")

print("\nDetails per road:")
for i in range(len(path)-1):
    u, v = path[i], path[i+1]
    edge = G[u][v]
    print(f"{G.nodes[u]['name']} -> {G.nodes[v]['name']} | time: {edge['time']:.2f}s | load: {edge['current_load']:.1f}/{edge['capacity']:.1f}")

# Plotting the result
fig, ax = plt.subplots(figsize=(8, 6))

pos = nx.spring_layout(G, seed=42)

# Draw non-highlighted edges
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=2, alpha=0.5, connectionstyle="arc3,rad=0.1")

# Draw shortest path edges
edge_list = list(zip(path[:-1], path[1:]))
nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edge_list, edge_color="red", width=3, connectionstyle="arc3,rad=0.1")
                 
# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue", node_size=800)
nx.draw_networkx_labels(G, pos, ax=ax, labels={n: G.nodes[n]['name'] for n in G.nodes})

plt.title("Traffic Routing System with Congestion Model using Dijkstra's Algorithm")
plt.axis("off")

# Save result as an image instead of using plt.show() which blocks CLI execution
output_image_path = os.path.join(BASE_DIR, "traffic_routing_output.png")
plt.savefig(output_image_path, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"\nGraph visualization successfully generated and saved to: {output_image_path}")
