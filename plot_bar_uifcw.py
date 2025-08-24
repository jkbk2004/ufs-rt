import matplotlib.pyplot as plt

# Sample data
cases = ['Case A', 'Case B', 'Case C', 'Case D']
case_numbers = [120, 90, 60, 30]

# Create horizontal bar plot
plt.figure(figsize=(8, 5))
plt.barh(cases, case_numbers, color='skyblue')
plt.xlabel('Number of Cases')
plt.title('Case Numbers Overview')
plt.gca().invert_yaxis()  # Optional: highest value at the top
plt.tight_layout()
plt.show()
