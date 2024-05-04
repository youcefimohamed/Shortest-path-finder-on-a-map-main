import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Global variables
graph = None
fig = None  # To store the matplotlib figure

def get_map_data(city_name):
    """Retrieve map data for the selected city."""
    place_name = city_name + ", Algeria"
    global graph
    graph = ox.graph_from_place(place_name, network_type='drive')
    print("Graph nodes:", len(graph.nodes))
    return graph


def update_nodes(event=None):
    """Update node lists based on selected city."""
    selected_city = combobox_city.get()
    graph = get_map_data(selected_city)
    listbox_source.delete(0, tk.END)
    listbox_target.delete(0, tk.END)
    for node in get_node_names(graph):
        listbox_source.insert(tk.END, node)
        listbox_target.insert(tk.END, node)

def get_node_names(graph):
    """Retrieve node names from the graph."""
    node_names = {}
    for node in graph.nodes():
        node_names[node] = graph.nodes[node].get('name', f"Unnamed Node {node}")
    return node_names

def a_star_search(graph, source, target):
    """Perform A* search to find the shortest path."""
    path = nx.astar_path(graph, source, target, weight='length')
    return path

def plot_shortest_path(graph, shortest_path):
    """Plot the shortest path on the map."""
    global fig
    fig, ax = ox.plot_graph_route(graph, shortest_path, route_color='g', route_linewidth=3,
                                  node_size=0, show=False, close=False)
    print("Plotting successful:", fig)


def find_shortest_path():
    """Find and display the shortest path between selected source and target nodes."""
    selected_source = listbox_source.get(tk.ACTIVE)
    selected_target = listbox_target.get(tk.ACTIVE)
    
    if selected_source and selected_target:
        shortest_path = a_star_search(graph, selected_source, selected_target)
        plot_shortest_path(graph, shortest_path)
        
        # Display the plot within tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        print("Canvas created successfully.")
    else:
        messagebox.showwarning("Warning", "Please select both source and target nodes.")


# Create main application window
root = tk.Tk()
root.title("Shortest Path Finder")

# Create frames for organization
frame_input = ttk.Frame(root, padding=20)
frame_input.pack(fill='both', expand=True)

# City selection widgets
label_city = ttk.Label(frame_input, text="Select City:")
label_city.grid(row=0, column=0, padx=10, pady=10, sticky='w')

cities = [
    "Adrar", "Ain Defla", "Ain Temouchent", "Alger", "Annaba", "Batna",
    "Bechar", "Bejaia", "Biskra", "Blida", "Bordj Bou Arreridj", "Bouira",
    "Boumerdes", "Chlef", "Constantine", "Djelfa", "El Bayadh", "El Oued",
    "El Tarf", "Ghardaia", "Guelma", "Illizi", "Jijel", "Khenchela",
    "Laghouat", "Muaskar", "Medea", "Mila", "Mostaganem", "Msila", "Naama",
    "Oran", "Ouargla", "Oum el Bouaghi", "Relizane", "Saida", "Setif", "Sidi Bel Abbes",
    "Skikda", "Souk Ahras", "Tamanrasset", "Tebessa", "Tiaret", "Tindouf",
    "Tipaza", "Tissemsilt", "Tizi Ouzou", "Tlemcen", "Adrar", "Ain Defla",
    "Ain Temouchent", "Alger", "Annaba", "Batna", "Bechar", "Bejaia", "Biskra",
    "Blida", "Bordj Bou Arreridj", "Bouira", "Boumerdes", "Chlef", "Constantine",
    "Djelfa", "El Bayadh", "El Oued", "El Tarf", "Ghardaia", "Guelma", "Illizi",
    "Jijel", "Khenchela", "Laghouat", "Muaskar", "Medea", "Mila", "Mostaganem",
    "Msila", "Naama", "Oran", "Ouargla", "Oum el Bouaghi", "Relizane", "Saida",
    "Setif", "Sidi Bel Abbes", "Skikda", "Souk Ahras", "Tamanrasset", "Tebessa",
    "Tiaret", "Tindouf", "Tipaza", "Tissemsilt", "Tizi Ouzou", "Tlemcen"
]

combobox_city = ttk.Combobox(frame_input, values=cities, width=30)
combobox_city.grid(row=0, column=1, padx=10, pady=10)
combobox_city.bind("<<ComboboxSelected>>", update_nodes)

# Source and target node selection lists
label_source = ttk.Label(frame_input, text="Source Place:")
label_source.grid(row=1, column=0, padx=10, pady=10, sticky='w')

listbox_source = tk.Listbox(frame_input, selectmode="browse", height=10, width=40)
listbox_source.grid(row=1, column=1, padx=10, pady=10)

label_target = ttk.Label(frame_input, text="Destination Place:")
label_target.grid(row=2, column=0, padx=10, pady=10, sticky='w')

listbox_target = tk.Listbox(frame_input, selectmode="browse", height=10, width=40)
listbox_target.grid(row=2, column=1, padx=10, pady=10)

# Find shortest path button
btn_find_path = ttk.Button(root, text="Show Shortest Path", command=find_shortest_path)
btn_find_path.pack(pady=20)

# Run the main event loop
root.mainloop()
