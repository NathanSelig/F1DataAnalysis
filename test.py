# Importing libraries
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sns.set(style="ticks")

# Loading the dataset
df = sns.load_dataset("anscombe")

# Show the results of a linear regression
sns.lmplot(x="x", y="y", data=df)


plt.show()
