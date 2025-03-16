# Re-import necessary libraries after execution state reset
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# Define platforms and workflows
platforms = ["x86", "ARM", "L@E", "Space", "GCP"]
workflows = ["Data Retrieval", "Data Processing", "Inference"]

# Base latencies (ms) for AWS x86
base_latency = {
    "Data Retrieval": 232,
    "Data Processing": 164,
    "Inference": 84
}

# GCP Latency values
gcp_latency = {
    "Data Retrieval": 215,
    "Data Processing": 274,
    "Inference": 85
}

# Latency adjustments for AWS-based platforms
latency_factors = {
    "x86": 1.0,
    "ARM": 1.1,  # ARM is 1.1x slower than x86
    "L@E": 0.5,  # Edge is 2x faster
    "Space": 0.167  # Space is 3x faster than L@E
}

# Compute adjusted latencies
latency_data = {
    wf: {pl: base_latency[wf] * latency_factors[pl] if pl != "GCP" else gcp_latency[wf] for pl in platforms}
    for wf in workflows
}

# Base costs for AWS x86
base_cost = {
    "Data Retrieval": 2.331,
    "Data Processing": 3.211,
    "Inference": 17.3086
}

# GCP cost values
gcp_cost = {
    "Data Retrieval": 1.3324,
    "Data Processing": 1.47029,
    "Inference": 62.5884
}

# Cost adjustments for AWS-based platforms
cost_factors = {
    "x86": 1.0,
    "ARM": 1.0,  # ARM has the same cost as x86
    "L@E": 1.5,  # L@E is 1.5x more expensive than x86
    "Space": 7.5  # Space is 5x more expensive than L@E
}

# Compute adjusted costs
cost_data = {
    wf: {pl: base_cost[wf] * cost_factors[pl] if pl != "GCP" else gcp_cost[wf] for pl in platforms}
    for wf in workflows
}

# Collect points for plotting
points = []
labels = []

for wf in workflows:
    for pl in platforms:
        points.append([latency_data[wf][pl], cost_data[wf][pl]])
        labels.append(f"{wf} ({pl})")

points = np.array(points)

# Compute Pareto front
def pareto_front(points):
    hull = ConvexHull(points)
    pareto_points = points[hull.vertices]
    pareto_points = pareto_points[np.argsort(pareto_points[:, 0])]  # Sort by latency
    return pareto_points

pareto_points = pareto_front(points)

# Compute Utopia point (Ideal min latency & min cost)
utopia_point = [min(points[:, 0]), min(points[:, 1])]

# Plot configurations
plt.figure(figsize=(10, 6))
colors = {"x86": "orange", "ARM": "red", "L@E": "blue", "Space": "purple", "GCP": "black"}
markers = {"Data Retrieval": "o", "Data Processing": "s", "Inference": "D"}

for i, (lat, cost) in enumerate(points):
    wf, pl = labels[i].split(" (")
    pl = pl[:-1]  # Remove closing parenthesis
    plt.scatter(lat, cost, color=colors[pl], marker=markers[wf], label=labels[i] if labels[i] not in plt.gca().get_legend_handles_labels()[1] else "")

# Plot Pareto front
plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label="Pareto Front")

# Plot Utopia point
plt.scatter(utopia_point[0], utopia_point[1], color='green', marker='*', s=150, label="Utopia Point")

plt.xlabel("Latency (ms)")
plt.ylabel("Cost (USD per 1M requests)")
plt.title("Cost vs. Latency for Different Configurations (AWS & GCP)")
plt.legend()
plt.grid(True)
plt.show()

