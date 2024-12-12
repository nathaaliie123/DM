import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import folium
import json
from streamlit_folium import st_folium

# Data koordinat kota
city_coordinates = {
    "West Java": {
        "Bandung": [-6.9175, 107.6191],
        "Bekasi": [-6.2383, 106.9756],
        "Bogor": [-6.5950, 106.8166],
        "Cimahi": [-6.8721, 107.5422],
        "Tasikmalaya": [-7.3274, 108.2207],
        "Depok": [-6.4025, 106.7942],
        "Purwakarta": [-6.5560, 107.4464],
        "Ciamis": [-7.3346, 108.3535],
        "Garut": [-7.2147, 107.8992],
        "Subang": [-6.5651, 107.7636]
    },
    "Central Java": {
        "Semarang": [-6.9667, 110.4167],
        "Solo": [-7.5667, 110.8167],
        "Magelang": [-7.4706, 110.2176],
        "Pekalongan": [-6.8894, 109.6753],
        "Tegal": [-6.8692, 109.1402],
        "Brebes": [-6.8712, 109.0381],
        "Salatiga": [-7.3305, 110.5084]
    },
    "East Java": {
        "Surabaya": [-7.2504, 112.7688],
        "Malang": [-7.9839, 112.6214],
        "Kediri": [-7.8162, 112.0116],
        "Blitar": [-8.0954, 112.1627],
        "Madiun": [-7.6298, 111.5300],
        "Ngawi": [-7.4009, 111.4483],
        "Tulungagung": [-8.0655, 111.9023]
    }
}

# Load koneksi antar kota dari file JSON
with open("connect.json", "r") as file:
    city_connections = json.load(file)

# Fungsi untuk membuat graf dari data koneksi kota
def create_graph(city_data):
    graph = nx.Graph()
    for city, neighbors in city_data.items():
        for neighbor in neighbors:
            graph.add_edge(city, neighbor)
    return graph

# Judul aplikasi
st.title("City Connections Across Java Provinces")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Profile", "Graph Visualization", "City Map"])

# Halaman Profile
if menu == "Profile":
    st.header("Team Members' Profiles")
    members = [
        {"name": "Nathalie Djuranovik", "study program": "Actuarial Science", "photo": "https://github.com/nathaaliie123/DM/blob/main/WhatsApp%20Image%202024-12-12%20at%2020.35.00_1290e537.jpg?raw=true"},
        {"name": "Liska Desryani Purba", "study program": "Actuarial Science", "photo": "https://github.com/nathaaliie123/DM/blob/main/WhatsApp%20Image%202024-12-12%20at%2019.23.13_af537960.jpg?raw=true"},
        {"name": "Natalia Maria Sitorus", "study program": "Actuarial Science", "photo": "https://github.com/nathaaliie123/DM/blob/main/WhatsApp%20Image%202024-12-12%20at%2021.52.38_45c750e4.jpg?raw=true"}
    ]

    for idx, member in enumerate(members, start=1):
        st.subheader(f"Person {idx}: {member['name']}")
        st.write(f"Study Program: {member['study program']}")
        st.image(member['photo'], caption=f"{member['name']}'s Photo")


# Halaman Graph Visualization
elif menu == "Graph Visualization":
    st.header("Graph Visualization: Directed and Undirected Graphs")

    graph_type = st.radio("Select Graph Type:", ["Undirected", "Directed"])

    # Input nodes and edges
    nodes = st.number_input("Enter the number of nodes:", min_value=1, step=1)
    edges = st.number_input("Enter the number of edges:", min_value=1, step=1)

    if nodes > 0 and edges > 0:
        G = nx.DiGraph() if graph_type == "Directed" else nx.Graph()

        for i in range(edges):
            edge_input = st.text_input(f"Enter edge {i + 1} (e.g., 1 2):", key=f"edge_{i}")
            if edge_input:
                u, v = map(int, edge_input.split())
                G.add_edge(u, v)

        plt.figure(figsize=(6, 4))
        nx.draw(G, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=12)
        st.pyplot(plt)
    else:
        st.warning("Please enter valid number of nodes and edges.")

# Halaman City Map
elif menu == "City Map":
    st.header("City Map Visualization")
    province = st.selectbox("Select a Province:", ["West Java", "Central Java", "East Java"])
    selected_cities = st.multiselect("Select Cities:", list(city_coordinates[province].keys()))

    if selected_cities:
        # Create the map centered on the chosen province
        m = folium.Map(location=[-7.0, 110.0], zoom_start=7)

        # Add markers for selected cities
        for city in selected_cities:
            folium.Marker(location=city_coordinates[province][city], popup=city).add_to(m)

        # Add connection lines between cities
        for city in selected_cities:
            for neighbor in city_connections.get(city, []):
                if neighbor in selected_cities:
                    folium.PolyLine(
                        [city_coordinates[province][city], city_coordinates[province][neighbor]],
                        color="blue", weight=2.5
                    ).add_to(m)

        # Display the map
        st_folium(m, width=700, height=500)

        # Create a graph from the selected cities and connections
        graph = create_graph({
            city: [neighbor for neighbor in city_connections.get(city, []) if neighbor in selected_cities]
            for city in selected_cities
        })

        st.subheader("Graph Representation")
        plt.figure(figsize=(8, 6))
        nx.draw(
            graph, with_labels=True, node_color="lightgreen", edge_color="blue", node_size=2000, font_size=10
        )
        st.pyplot(plt)
    else:
        st.warning("Please select at least one city.")
