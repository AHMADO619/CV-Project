import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Load the already-cleaned file
df = pd.read_csv("Superstore_cleaned_last2.csv", encoding="UTF-8")

df['Ship Days'] = (df['Ship Date'] - df['Order Date']).dt.days
