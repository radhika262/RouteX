
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import AnchoredText

# Fixed station positions (manually defined to match the image)
fixed_positions = {
    "DDN": (0, 1),    # Dehradun
    "HW": (1, 1),      # Haridwar
    "RK": (0, 0),      # Roorkee
    "KGM": (3, 0.5),   # Kathgodam
    "LD": (1.5, 0.5),  # Laksar
    "RMR": (2, 1),     # Ramnagar
    "TPZ": (2.5, 1.5), # Tanakpur
    "KPV": (1.5, 0),   # Kichha
    "HLD": (2, 0),     # Haldwani
    "KPT": (3, 1.5),   # Khatima
    "LRJ": (3.5, 0.5), # Lalkuan
    "UKA": (2.5, 0.5), # Udham Singh Nagar
    "PBE": (1, 1.5),   # Pauri
    "SPE": (0.5, 1.5), # Srinagar
    "CH": (0, 1.5),    # Chamoli
    "BHT": (0.5, 0.5), # Bharatpur
    "ALM": (3.5, 1),   # Almora
    "NAE": (3, 1),     # Nainital
    "PTH": (0.5, 2),   # Pithoragarh
    "RUD": (3, 0)      # Rudrapur
}

# Station codes and names (updated to match your JSON)
station_codes = {
    "DDN": "Dehradun",
    "HW": "Haridwar", 
    "RK": "Roorkee",
    "KGM": "Kathgodam",
    "LD": "Laksar",
    "RMR": "Ramnagar",
    "TPZ": "Tanakpur",
    "KPV": "Kichha",
    "HLD": "Haldwani",
    "KPT": "Khatima",
    "LRJ": "Lalkuan",
    "UKA": "Udham Singh Nagar",
    "PBE": "Pauri",
    "SPE": "Srinagar",
    "CH": "Chamoli",
    "BHT": "Bharatpur",
    "ALM": "Almora",
    "NAE": "Nainital",
    "PTH": "Pithoragarh",
    "RUD": "Rudrapur"
}

def draw_station_code_legend(ax):
    legend_entries = [f"{name} → {code}" for code, name in station_codes.items()]
    col1 = legend_entries[:len(legend_entries)//2]
    col2 = legend_entries[len(legend_entries)//2:]
    
    legend_text = ""
    for i in range(max(len(col1), len(col2))):
        line = ""
        if i < len(col1):
            line += col1[i].ljust(25)
        if i < len(col2):
            line += col2[i]
        legend_text += line + "\n"
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    ax.text(1.05, 0.5, legend_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='center', bbox=props)

def draw_scale(ax):
    scale_text = "Scale:\n1 unit = 25 km\n2 units = 50 km"
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    ax.text(1.05, 0.9, scale_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='center', bbox=props)

def visualize_path_with_full_graph():
    try:
        # Load the full graph data
        with open("data/uttarakhand_railway.json") as f:
            full_data = json.load(f)

        # Load the path data
        with open("data/uttarakhand_dijkstra_distance_result.json") as f:
            path_data = json.load(f)

        path = path_data["path"]
        cost = path_data.get("cost", None)

        # Create the full graph
        G_full = nx.DiGraph()
        edge_labels = {}
        for src, details in full_data.items():
            G_full.add_node(src)
            for conn in details.get("connections", []):
                dst = conn["to"]
                dist = conn["distance"]
                G_full.add_edge(src, dst, weight=dist)
                edge_labels[(src, dst)] = f"{dist} km"

        # Create the path graph
        G_path = nx.DiGraph()
        for i in range(len(path) - 1):
            G_path.add_edge(path[i], path[i + 1])

        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Draw the full graph (grayed out)
        nx.draw_networkx_nodes(G_full, fixed_positions, node_color='lightgray', 
                             node_size=1000, ax=ax)
        nx.draw_networkx_edges(G_full, fixed_positions, edge_color='lightgray', 
                             width=1, arrows=True, ax=ax)
        
        # Draw the path (highlighted)
        nx.draw_networkx_nodes(G_path, fixed_positions, nodelist=path, 
                             node_color='lightgreen', node_size=1500, ax=ax)
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G_path, fixed_positions, edgelist=path_edges, 
                             edge_color='green', width=3, arrows=True, ax=ax)
        
        # Draw labels for all nodes
        nx.draw_networkx_labels(G_full, fixed_positions, font_weight='bold', ax=ax)
        
        # Draw edge labels for the path
        path_edge_labels = {(u, v): edge_labels[(u, v)] for (u, v) in path_edges 
                           if (u, v) in edge_labels}
        nx.draw_networkx_edge_labels(G_full, fixed_positions, 
                                   edge_labels=path_edge_labels, ax=ax)
        
        # Train animation
        x_vals = [fixed_positions[station][0] for station in path]
        y_vals = [fixed_positions[station][1] for station in path]

        train_dot, = ax.plot([], [], 'ro', markersize=14)
        
        def init():
            train_dot.set_data([], [])
            return train_dot,

        def animate(i):
            if i < len(x_vals):
                train_dot.set_data([x_vals[i]], [y_vals[i]])
            return train_dot,

        ani = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=len(x_vals)+1, interval=1000, 
                                    blit=True, repeat=False)

        title = f"Train Journey (Total Distance: {cost} km)" if cost else "Train Journey"
        ax.set_title(title)
        
        draw_station_code_legend(ax)
        draw_scale(ax)
        
        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e:
        print(f"Error: File not found - {str(e)}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON data in file.")
    except KeyError as e:
        print(f"Error: Missing expected data - {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def visualize_full_graph():
    try:
        with open("data/uttarakhand_railway.json") as f:
            data = json.load(f)

        G = nx.DiGraph()
        edge_labels = {}
        for src, details in data.items():
            G.add_node(src)
            for conn in details.get("connections", []):
                dst = conn["to"]
                dist = conn["distance"]
                G.add_edge(src, dst, weight=dist)
                edge_labels[(src, dst)] = f"{dist} km"

        fig, ax = plt.subplots(figsize=(14, 8))
        
        nx.draw_networkx_nodes(G, fixed_positions, node_color='skyblue', 
                             node_size=1500, ax=ax)
        nx.draw_networkx_edges(G, fixed_positions, edge_color='gray', 
                             width=2, arrows=True, ax=ax)
        nx.draw_networkx_labels(G, fixed_positions, font_weight='bold', ax=ax)
        nx.draw_networkx_edge_labels(G, fixed_positions, edge_labels=edge_labels, ax=ax)
        
        plt.title("Uttarakhand Railway Network", pad=20)
        draw_station_code_legend(ax)
        draw_scale(ax)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Error: Railway data file not found. Run the C++ program first.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON data in railway file.")

def main():
    choice = input("Enter 1 to visualize whole graph or 2 to visualize path from source to destination: ")
    
    if choice == '1':
        visualize_full_graph()
    elif choice == '2':
        visualize_path_with_full_graph()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

