import pandas as pd

# Define possible values for features
colors = [0, 1, 2, 3, 4]
chemicals = [0, 1]

# Create an empty list to store dataset rows
data = []

# Generate rows based on combinations of color and chemical values
for color in colors:
    for chemical in chemicals:
        # Determine the label based on the given conditions
        if color in [1, 3, 4] and chemical == 1:
            ripen = "Ripen with chemical"
        elif color in [1, 3, 4] and chemical == 0:
            ripen = "Ripen without chemical"
        else:
            ripen = "No ripening"

        # Append row to data
        data.append({"Color": color, "Chemical": chemical, "Ripen": ripen})

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("ripening_data.csv", index=False)
print("Dataset saved as ripening_data.csv")
