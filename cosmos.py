import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define data
data = {
    "Workflow": [
        "Data Retrieval", "Data Retrieval", "Data Retrieval", "Data Retrieval", "Data Retrieval",
        "Data Processing", "Data Processing", "Data Processing", "Data Processing", "Data Processing",
        "Inference", "Inference", "Inference", "Inference", "Inference"
    ],
    "Platform": [
        "x86", "arm", "L@E", "Space", "GCP",
        "x86", "arm", "L@E", "Space", "GCP",
        "x86", "arm", "L@E", "Space", "GCP"
    ],
    "Latency (ms)": [
        232, 236, 125.28, 69.6, 215,
        164, 168, 88.56, 49, 274,
        84, 86, 45.36, 25, 85
    ],
    "Cost (USD per 1M requests)": [
        2.331, 2.2847, 3.14685, 490, 1.3324,
        3.211, 3.1647, 4.33485, 490, 1.47029,
        17.3086, 17.2623, 23.36661, 490, 62.5884
    ]
}

df = pd.DataFrame(data)

# Collect points for plotting
points = []
labels = []

for i, row in df.iterrows():
    points.append([row["Latency (ms)"], row["Cost (USD per 1M requests)"]])
    labels.append(f"{row['Workflow']} ({row['Platform']})")

points = np.array(points)

# Compute Pareto front
def pareto_front(points):
    pareto_points = []
    sorted_points = points[np.argsort(points[:, 0])]  # Sort by latency
    min_cost = float('inf')
    
    for point in sorted_points:
        if point[1] <= min_cost + 1e-6:  # Allow small floating-point tolerance
            pareto_points.append(point)
            min_cost = point[1]
    
    # Ensure the Pareto front extends to the maximum latency
    max_latency_point = sorted_points[-1]  # The point with max latency
    if not any(np.all(max_latency_point == p) for p in pareto_points):
        pareto_points.append(max_latency_point)
    
    return np.array(pareto_points)

pareto_points = pareto_front(points)

# Compute Utopia point (Ideal min latency & min cost)
utopia_point = [min(points[:, 0]), min(points[:, 1])]

# SLO constraints
slo_budget = 50  # USD
slo_latency = 75  # ms

# Plot configurations
plt.figure(figsize=(10, 6))
colors = {"x86": "orange", "arm": "red", "L@E": "blue", "Space": "purple", "GCP": "black"}
markers = {"Data Retrieval": "o", "Data Processing": "s", "Inference": "D"}

for i, (lat, cost) in enumerate(points):
    wf, pl = labels[i].split(" (")
    pl = pl[:-1]  # Remove closing parenthesis
    plt.scatter(lat, cost, color=colors[pl], marker=markers[wf], label=labels[i] if labels[i] not in plt.gca().get_legend_handles_labels()[1] else "")

# Plot Pareto front
plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label="Pareto Front")

# Plot Utopia point
plt.scatter(utopia_point[0], utopia_point[1], color='green', marker='*', s=150, label="Utopia Point")

# Draw SLO lines
plt.axhline(y=slo_budget, color='gray', linestyle='dotted', linewidth=1)
plt.axvline(x=slo_latency, color='gray', linestyle='dotted', linewidth=1)

# Annotate SLO constraints on axes
plt.text(plt.xlim()[0] + 5, slo_budget + 2, "Cost SLO (50 USD)", fontsize=10, color='gray')
plt.text(slo_latency + 2, plt.ylim()[0] + 2, "Latency SLO (75 ms)", fontsize=10, color='gray', rotation=90)

plt.xlabel("Latency (ms)")
plt.ylabel("Cost (USD per 1M requests)")
plt.title("Cost vs. Latency for Different Configurations")
plt.legend()
plt.grid(True)
plt.show()
