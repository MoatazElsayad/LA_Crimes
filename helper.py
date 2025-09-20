import seaborn as sns
import matplotlib.pyplot as plt


# Seaborn theme (dark grid + white text)
sns.set_theme(
    style="darkgrid",
    palette="deep",
    font="DejaVu Sans",
    font_scale=1.2
)

# dark-blue background
plt.rcParams.update({
    "figure.facecolor": "#0a1a2f",      # dark blue background for figure
    "axes.facecolor": "#0a1a2f",        # dark blue inside plots
    "axes.edgecolor": "white",            # white borders
    "axes.labelcolor": "white",      # white axis labels
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.color": "white",          # white x ticks
    "ytick.color": "white",          # white y ticks
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "grid.color": "gray",            # grid lines (lighter)
    "grid.alpha": 0.3,
    "legend.facecolor": "#0a1a2f",   # legend background matches
    "legend.edgecolor": "white",
    "legend.fontsize": 12,
    "text.color": "white",           # general text color
    "figure.autolayout": True
})

descent_map = {
    "A": "Other Asian",
    "B": "Black",
    "C": "Chinese",
    "D": "Cambodian",
    "F": "Filipino",
    "G": "Guamanian",
    "H": "Hispanic/Latin/Mexican",
    "I": "American Indian/Alaskan Native",
    "J": "Japanese",
    "K": "Korean",
    "L": "Laotian",
    "O": "Other",
    "P": "Pacific Islander",
    "S": "Samoan",
    "U": "Hawaiian",
    "V": "Vietnamese",
    "W": "White",
    "X": "Unknown",
    "Z": "Asian Indian"
}