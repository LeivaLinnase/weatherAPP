import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from matplotlib.patches import FancyBboxPatch


def get_background_image(condition, is_day):
    folder = "day" if is_day == 1 else "night"
    condition = condition.lower()
    if "rain" in condition:
        return f"images/{folder}/rain.jpg"
    elif "snow" in condition:
        return f"images/{folder}/snow.jpg"
    elif "thunder" in condition:
        return f"images/{folder}/thunder.jpg"
    elif "partly" in condition:
        return f"images/{folder}/slight_cloudy.jpg"
    elif "cloudy" in condition:
        return f"images/{folder}/overcast.jpg"
    elif "clear" in condition:
        return f"images/{folder}/clear.jpg"
    else:
        return f"images/{folder}/clear.jpg"


def create_weather_visualization(csv_file):
    weather_data = pd.read_csv(csv_file).set_index("City").to_dict(orient="index")
    city_list = list(weather_data.keys())
    num_cities = len(city_list)
    rows, cols = 2, 4

    fig, axes = plt.subplots(rows, cols, figsize=(16, 10))
    fig.subplots_adjust(wspace=0.4, hspace=0.5)
    fig.patch.set_facecolor('papayawhip')

    for i, city in enumerate(city_list):
        row, col = divmod(i, cols)
        ax = axes[row, col]
        data = weather_data[city]
        temp = data["Temperature (°C)"]
        condition = data["Condition"]
        humidity = data["Humidity (%)"]
        wind_speed = data["Wind Speed (kph)"]
        precipitation = data["Precipitation"]
        is_day = data["Is Day"]
        uv_index = data["UV-index"]

        # background image
        bg_path = get_background_image(condition, is_day)
        if os.path.exists(bg_path):
            img = mpimg.imread(bg_path)
        else:
            img = None

        rect = FancyBboxPatch(
            (0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.1", linewidth=0,
            edgecolor=None, facecolor="none", transform=ax.transAxes
        )
        ax.add_patch(rect)

        if img is not None:
            ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto', clip_path=rect)

        # Display weather details
        text_color = 'white'
        ax.text(
            0.5, 0.9, f"{city}", fontsize=18, color=text_color, fontweight="bold", ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )
        ax.text(
            0.5, 0.7, f"{temp}°C", fontsize=16, color=text_color, fontweight="semibold", ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )
        ax.text(
            0.5, 0.6, f"{condition}", fontsize=12, color=text_color, ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )

        ax.text(
            0.5, 0.55, f"Humidity: {humidity}%", fontsize=12, color=text_color, ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )
        ax.text(
            0.5, 0.50, f"Wind: {wind_speed} kph", fontsize=12, color=text_color, ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )
        ax.text(
            0.5, 0.45, f"Precipitation: {precipitation} mm", fontsize=12, color=text_color, ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )
        ax.text(
            0.5, 0.4, f"UV Index: {uv_index}", fontsize=12, color=text_color, ha="center",
            va="center", transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5, boxstyle="round,pad=0.1")
        )

        # Hide axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    # Remove empty subplot spaces
    for j in range(len(city_list), rows * cols):
        fig.delaxes(axes.flatten()[j])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    csv_file = "weather_data.csv"  # Default file name
    create_weather_visualization(csv_file)
