import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(snakemake.input[0])
country = snakemake.wildcards.country
plot = snakemake.wildcards.plot

fig, ax = plt.subplots(figsize=(7, 4.5))

if df.empty:
    ax.text(0.5, 0.5, f"No data for {country}", ha="center", va="center")
    ax.set_axis_off()
elif plot == "timeseries":
    ax.plot(df["Year"], df["Forest_fires"], color="tab:red", marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Forest fires", color="tab:red")
    ax2 = ax.twinx()
    ax2.plot(df["Year"], df["GDP"], color="tab:blue", marker="s")
    ax2.set_ylabel("GDP", color="tab:blue")
    ax.set_title(f"{country}: forest fires and GDP over time")
elif plot == "scatter":
    sc = ax.scatter(df["GDP"], df["Forest_fires"], c=df["Year"], cmap="viridis")
    fig.colorbar(sc, ax=ax, label="Year")
    ax.set_xlabel("GDP")
    ax.set_ylabel("Forest fires")
    ax.set_title(f"{country}: forest fires vs GDP")
else:
    raise ValueError(f"Unknown plot type: {plot}")

fig.tight_layout()
fig.savefig(snakemake.output[0], dpi=150)
