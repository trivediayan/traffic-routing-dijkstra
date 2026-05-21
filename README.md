# 🚦 SmartFlow: Traffic Routing System with a Congestion Model

Let's face it—traffic is frustrating. We've all been there: sitting in a bumper-to-bumper queue on the main road, wishing we had taken that slightly longer detour which was probably completely clear. 

This project was created to solve exactly that problem! It's a friendly, highly interactive simulation dashboard that models how traffic piles up on roads and uses **Dijkstra's Shortest Path Algorithm** to dynamically recalculate the absolute fastest way to get to your destination in real-time.

---

## 🚗 The Story: Getting from College to the Station

Imagine you just finished a long lecture at **College** (Node 1) and need to catch a train at the **Station** (Node 4) as quickly as possible. 

Normally, the route through **Main Road** is the fastest. But during rush hour, everyone takes that road, causing massive jams. Our app lets you play the role of a traffic controller:
* Slide the congestion bars in the sidebar to simulate cars piling up.
* Watch the live graph update instantly.
* See the routing engine dynamically steer the red path away from congested roads (like Main Road) and onto clearer detours (like the **Market**), even if they are physically longer!

---

## 🧠 How It Works under the Hood (Simply Explained)

Instead of just looking at physical distance (meters), our routing engine measures **travel time (seconds)**. 

To make this realistic, we use a classic civil engineering formula (the Bureau of Public Roads model) to calculate how much a road slows down as more cars enter:

$$\text{Actual Travel Time} = \text{Free Flow Time} \times \left(1 + 1.5 \times \max\left(0, \frac{\text{Current Traffic Load}}{\text{Road Capacity}} - 1\right)\right)$$

### In plain English:
1. **Clear Road**: If the simulated traffic load is below the road's natural capacity, cars zip through at the speed limit.
2. **Congestion Trigger**: Once the traffic exceeds capacity, every extra car slows traffic down exponentially.
3. **Closed Roads**: If a road is completely blocked (capacity is zero), our algorithm gives it an enormous time penalty so cars are routed away.

---

## 🎨 What Makes this App Special?

We wanted this project to feel alive and premium, rather than like a dry academic script:
* **Glassmorphic Theme**: A modern dashboard look with glowing gradients and glass-like card elements.
* **Smart Map Legend**: Color-coded guides so you instantly understand what the network is telling you.
* **Curved Road Connections**: Distinct curved paths on the graph so you can easily distinguish two-way roads.
* **Visual Node Indicators**: 
  * **🟢 Green** is where your journey starts (Origin).
  * **🔴 Red** is where you want to end up (Destination).
  * **🟡 Yellow** are your transit stops along the optimal path.
  * **⚫ Dark Slate** are inactive nodes not needed for your current trip.

---

## 📁 What's Inside?

Here is a quick map of the files in this folder:

* `nodes.csv` — The list of places in our network (College, Main Road, Market, Station).
* `edges.csv` — The roads connecting those places, including their lengths, speed limits, and capacities.
* `traffic_app.py` — The heart of the project: the gorgeous, interactive Streamlit dashboard.
* `traffic_routing.py` — A simple command-line version of the tool that calculates the path and saves a static image (`traffic_routing_output.png`) to your disk.
* `install_libraries.py` — A handy helper script that checks and installs any libraries you might be missing.

---

## 🚀 Try It Yourself!

Getting the project up and running takes less than two minutes:

### Step 1: Install what you need
We built a simple setup script that checks your Python environment and installs missing packages automatically. Open your terminal in this folder and run:
```bash
python install_libraries.py
```

### Step 2: Launch the interactive web app
Start the dashboard server:
```bash
python -m streamlit run traffic_app.py
```
Streamlit will launch a browser window automatically. If it doesn't, just open **`http://localhost:8503`** in your browser!

### Step 3: Run the lightweight console script (Optional)
If you just want a quick text output and want to save a graph image directly to your folder without launching a browser:
```bash
python traffic_routing.py
```
This prints the optimal route breakdown directly in your terminal and saves `traffic_routing_output.png` next to your files.

---

## ❤️ Made with Care
This project was engineered to be highly robust and user-friendly:
* **No Folder path headaches**: It automatically figures out where your data CSVs are located, so you can run it from any terminal folder without path errors.
* **Safe for multi-tasking**: The graph rendering uses safe isolated canvas flows, so it never mixes up graphs if multiple users load the page at the same time.
* **Terminal-friendly**: Emojis are stripped from command-line outputs to prevent Windows terminal printing crashes.
