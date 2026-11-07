import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plot = snakemake.wildcards.plot
fig, ax = plt.subplots(figsize=(8, 5))

for country, path in zip(snakemake.params.countries, snakemake.input):
    df = pd.read_csv(path)
    if df.empty:
        continue
    if plot == "timeseries":
        ax.plot(df["Year"], df["Forest_fires"], marker="o", label=country)
    elif plot == "scatter":
        ax.scatter(df["GDP"], df["Forest_fires"], label=country)

if plot == "timeseries":
    ax.set_xlabel("Year")
else:
    ax.set_xlabel("GDP")
ax.set_ylabel("Forest fires")
ax.set_title(f"Forest fires across countries ({plot})")
ax.legend()

fig.tight_layout()
fig.savefig(snakemake.output[0], dpi=150)
