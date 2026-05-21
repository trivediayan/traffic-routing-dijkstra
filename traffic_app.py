import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import os

# Set matplotlib to non-interactive Agg backend to avoid GUI issues
matplotlib.use('Agg')

# Set page configuration for a premium visual identity
st.set_page_config(
    page_title="Traffic Routing System with Congestion Model using Dijkstra's Algorithm",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using glassmorphism and modern gradient designs
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply modern typography globally */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Main Layout Aesthetics */
    .reportview-container {
        background: #0f172a;
    }
    
    /* Title and Header Gradients */
    .main-title {
        background: linear-gradient(135deg, #60A5FA 0%, #34D399 50%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    .sub-title {
        color: #94A3B8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Premium glassmorphic metric cards */
    .card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.3);
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.4);
    }
    
    /* Custom style for sidebar */
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* Style path visualization text */
    .path-bubble {
        display: inline-block;
        background: rgba(96, 165, 250, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.2rem;
    }
    
    .path-arrow {
        color: #94A3B8;
        font-weight: bold;
        margin: 0 0.5rem;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38BDF8;
        margin-top: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)

# Render main page title
st.markdown('<div class="main-title">🚦 Traffic Routing System with Congestion Model using Dijkstra\'s Algorithm</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time Traffic Congestion Mitigation & Path Optimization</div>', unsafe_allow_html=True)

# Absolute path resolution to prevent incorrect working directory errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nodes_path = os.path.join(BASE_DIR, "nodes.csv")
edges_path = os.path.join(BASE_DIR, "edges.csv")

@st.cache_data
def load_base_data():
    nodes_df = pd.read_csv(nodes_path)
    edges_df = pd.read_csv(edges_path)
    return nodes_df, edges_df

try:
    nodes, base_edges = load_base_data()
except Exception as e:
    st.error(f"❌ Failed to load project CSV data. Details: {e}")
    st.info("Ensure nodes.csv and edges.csv are in the project folder: " + BASE_DIR)
    st.stop()

# We maintain interactive states in Streamlit Session State or read-write local copy
edges = base_edges.copy()

# Sidebar: Congestion configuration with clean aesthetics
st.sidebar.markdown("### 🎛️ Congestion Control")
st.sidebar.markdown("Simulate real-time traffic volume (vehicles/hour) on individual road segments.")

# Set up sliders for each edge
st.sidebar.markdown("---")
for i in range(len(edges)):
    edge_row = edges.iloc[i]
    from_id = int(edge_row['from'])
    to_id = int(edge_row['to'])
    
    # Lookup node names
    from_name = nodes.loc[nodes['node_id'] == from_id, 'name'].values[0]
    to_name = nodes.loc[nodes['node_id'] == to_id, 'name'].values[0]
    
    capacity = int(edge_row['capacity'])
    current_load = int(edge_row['current_load'])
    
    new_load = st.sidebar.slider(
        label=f"🚗 {from_name} → {to_name}",
        min_value=0,
        max_value=capacity * 2,
        value=current_load,
        step=50,
        key=f"edge_slider_{from_id}_{to_id}"
    )
    edges.at[i, 'current_load'] = new_load

ALPHA = 1.5

# Construct Graph using NetworkX
G = nx.DiGraph()

for _, row in nodes.iterrows():
    G.add_node(int(row['node_id']), name=row['name'])

for _, row in edges.iterrows():
    length_m = float(row['length_m'])
    speed = float(row['speed_limit_kmph'])
    capacity = float(row['capacity'])
    load = float(row['current_load'])
    
    # Calculate travel time in seconds factoring in congestion (BPR-like formula)
    base_time = length_m / (speed * 1000 / 3600)  # free-flow time in seconds
    
    if capacity <= 0:
        multiplier = 9999.0  # infinite cost for closed roads
    else:
        ratio = load / capacity
        multiplier = 1.0 + ALPHA * max(0.0, ratio - 1.0)
    
    travel_time = base_time * multiplier
    
    G.add_edge(
        int(row['from']), 
        int(row['to']), 
        time=travel_time,
        length=length_m,
        speed=speed,
        capacity=capacity,
        load=load
    )

# App Layout: Two columns for Routing controls vs Network visualization
col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    st.markdown('<div class="card"><h4>📍 Route Selector</h4>', unsafe_allow_html=True)
    
    source_name = st.selectbox("Origin Point", nodes['name'], index=0)
    target_name = st.selectbox("Destination Point", nodes['name'], index=3)
    
    src_row = nodes.loc[nodes['name'] == source_name]
    tgt_row = nodes.loc[nodes['name'] == target_name]
    
    src_id = int(src_row['node_id'].values[0])
    tgt_id = int(tgt_row['node_id'].values[0])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if src_id == tgt_id:
        st.warning("⚠️ Origin and Destination are the same. Pick different locations.")
    else:
        try:
            # Run Dijkstra
            path = nx.shortest_path(G, source=src_id, target=tgt_id, weight='time')
            total_time = nx.shortest_path_length(G, source=src_id, target=tgt_id, weight='time')
            
            # Extract details
            path_names = [G.nodes[p]['name'] for p in path]
            
            st.markdown('<div class="card"><h4>✨ Best Computed Path</h4>', unsafe_allow_html=True)
            
            # Draw pretty bubbles for path
            path_html = ""
            for idx, name in enumerate(path_names):
                path_html += f'<span class="path-bubble">{name}</span>'
                if idx < len(path_names) - 1:
                    path_html += '<span class="path-arrow">→</span>'
            
            st.markdown(path_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Metric blocks
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"""
                <div class="card" style="text-align: center;">
                    <div class="metric-label">Estimated Travel Time</div>
                    <div class="metric-value">{total_time:.2f}s</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                # Calculate total physical distance of path
                total_dist = 0
                for u, v in zip(path[:-1], path[1:]):
                    total_dist += G[u][v]['length']
                st.markdown(f"""
                <div class="card" style="text-align: center;">
                    <div class="metric-label">Route Distance</div>
                    <div class="metric-value">{total_dist:.0f} m</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Path breakdown table
            st.markdown("#### 📋 Route Segment Details")
            segment_data = []
            for u, v in zip(path[:-1], path[1:]):
                edge = G[u][v]
                congestion_pct = (edge['load'] / edge['capacity']) * 100
                status = "🟢 Clear"
                if congestion_pct > 150:
                    status = "🔴 Severely Congested"
                elif congestion_pct > 100:
                    status = "🟠 Congested"
                elif congestion_pct > 50:
                    status = "🟡 Moderate"
                    
                segment_data.append({
                    "Segment": f"{G.nodes[u]['name']} → {G.nodes[v]['name']}",
                    "Travel Time": f"{edge['time']:.1f}s",
                    "Congestion Level": f"{congestion_pct:.1f}%",
                    "Condition": status
                })
            
            st.table(pd.DataFrame(segment_data))
            
        except nx.NetworkXNoPath:
            st.error("🚨 Routing Failure: No valid path found between the selected points.")

with col2:
    st.markdown('<div class="card" style="height: 100%;"><h4>🗺️ Live Traffic Map Graph</h4>', unsafe_allow_html=True)
    
    # Thread-safe matplotlib canvas creation
    fig, ax = plt.subplots(figsize=(7, 6), facecolor='none')
    ax.set_facecolor('none')
    
    pos = nx.spring_layout(G, seed=42)
    
    # High aesthetics drawing:
    # 1. Base edges (inactive)
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color="#475569",  # Slate 600
        width=1.5,
        alpha=0.4,
        arrows=True,
        arrowsize=15,
        connectionstyle="arc3,rad=0.1"  # curved edges to distinguish bi-directional links!
    )
    
    # 2. Highlighted path edges
    if 'path' in locals() and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edgelist=path_edges,
            edge_color="#EF4444",  # Coral / Red
            width=4.0,
            alpha=0.9,
            arrows=True,
            arrowsize=20,
            connectionstyle="arc3,rad=0.1"
        )
        
    # 3. Dynamic node colors based on origin, destination, transit, or inactive
    node_colors = []
    for node in G.nodes:
        if 'path' in locals() and node in path:
            if node == src_id:
                node_colors.append("#10B981")  # Emerald green (origin)
            elif node == tgt_id:
                node_colors.append("#EF4444")  # Rose red (dest)
            else:
                node_colors.append("#F59E0B")  # Transit Orange
        else:
            node_colors.append("#1E293B")  # Slate 800 (inactive)
            
    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=1200,
        edgecolors="#64748B",  # Slate 500 border
        linewidths=1.5
    )
    
    # Draw labels with elegant layout
    labels = {n: G.nodes[n]['name'] for n in G.nodes}
    label_colors = {
        n: "#FFFFFF" if ('path' in locals() and n in path) else "#94A3B8"
        for n in G.nodes
    }
    
    for node, position in pos.items():
        ax.text(
            position[0], position[1] + 0.08,  # shift slightly upwards for beautiful spacing
            s=labels[node],
            color=label_colors[node],
            fontsize=11,
            fontweight="bold" if ('path' in locals() and node in path) else "normal",
            horizontalalignment="center",
            verticalalignment="center"
        )
        
    ax.axis("off")
    plt.tight_layout()
    
    # Premium rendering into streamlit without global state leakage
    st.pyplot(fig, clear_figure=True)
    st.markdown("""
    💡 **Map Legend:** 
    * <span style="color:#10B981; font-weight:bold;">🟢 Origin Node</span>
    * <span style="color:#EF4444; font-weight:bold;">🔴 Destination Node</span>
    * <span style="color:#F59E0B; font-weight:bold;">🟡 Path Nodes</span>
    * <span style="color:#EF4444; font-weight:bold;">➖ Best Route Link</span>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
