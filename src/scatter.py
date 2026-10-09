import argparse
import math
from pathlib import Path

from fire_gdp import get_fire_gdp_year_data

import matplotlib

matplotlib.use("Agg")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COUNTRIES = ("Brazil", "Canada", "China", "India")


def pearson_correlation(x_values, y_values):
    """Return Pearson's r, or None when it is undefined."""
    if len(x_values) < 2 or len(x_values) != len(y_values):
        return None

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    x_deviations = [value - x_mean for value in x_values]
    y_deviations = [value - y_mean for value in y_values]
    denominator = math.sqrt(
        sum(value ** 2 for value in x_deviations)
        * sum(value ** 2 for value in y_deviations)
    )
    if denominator == 0:
        return None

    numerator = sum(
        x_deviation * y_deviation
        for x_deviation, y_deviation in zip(x_deviations, y_deviations)
    )
    return numerator / denominator


def plot_country(country, observations, output_dir):
    import matplotlib.pyplot as plt

    years, forest_fires, gdp = zip(*observations)
    correlation = pearson_correlation(forest_fires, gdp)
    correlation_label = (
        f"Pearson r = {correlation:.3f}"
        if correlation is not None
        else "Pearson r undefined"
    )

    figure, axis = plt.subplots(figsize=(7.5, 5.5), constrained_layout=True)
    points = axis.scatter(
        forest_fires,
        gdp,
        c=years,
        cmap="viridis",
        s=42,
        edgecolors="white",
        linewidths=0.5,
    )
    figure.colorbar(points, ax=axis, label="Year")
    axis.set_title(f"{country}: forest-fire emissions and GDP")
    axis.set_xlabel("Forest-fire CO2 emissions (dataset units)")
    axis.set_ylabel("GDP (local currency; dataset units)")
    axis.text(
        0.03,
        0.97,
        f"n = {len(observations)}\n{correlation_label}",
        transform=axis.transAxes,
        verticalalignment="top",
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
    )
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    file_name = f"{country.lower().replace(' ', '_')}.png"
    output_path = output_dir / file_name
    figure.savefig(output_path, dpi=180, facecolor="white")
    plt.close(figure)

    return correlation, output_path


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Plot forest-fire emissions against GDP separately by country."
        )
    )
    parser.add_argument(
        "--co2-file",
        type=Path,
        default=PROJECT_ROOT / "data" / "Agrofood_co2_emission.csv",
        help="Path to the agrofood CO2 emissions CSV.",
    )
    parser.add_argument(
        "--gdp-file",
        type=Path,
        default=PROJECT_ROOT / "data" / "IMF_GDP.csv",
        help="Path to the IMF GDP CSV.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "plots",
        help="Directory in which to save the country plots.",
    )
    parser.add_argument(
        "--countries",
        nargs="+",
        default=DEFAULT_COUNTRIES,
        help=(
            "Country names to plot "
            "(default: Brazil Canada China India)."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for country in args.countries:
        observations = get_fire_gdp_year_data(
            str(args.co2_file), str(args.gdp_file), country
        )
        if not observations:
            raise SystemExit(f"No paired observations found for {country}.")

        correlation, output_path = plot_country(
            country, observations, args.output_dir
        )
        years = [row[0] for row in observations]
        correlation_text = (
            f"{correlation:.3f}" if correlation is not None else "undefined"
        )
        print(
            f"{country}: n={len(observations)}, "
            f"years={min(years)}-{max(years)}, r={correlation_text}; "
            f"saved {output_path}"
        )


if __name__ == "__main__":
    main()
