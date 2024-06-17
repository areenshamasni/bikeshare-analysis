from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Define the path to the data files
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


# Helper function to load data based on user input
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Convert to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name().str.lower()

    # Apply filters if specified
    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month.lower()) + 1
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day.lower()]

    return df


# Function to generate time statistics
def time_stats(df):
    popular_month = df["month"].mode()[0]
    popular_day = df["day_of_week"].mode()[0].title()
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]

    return (
        f"Most Popular Month: {popular_month}",
        f"Most Popular Day: {popular_day}",
        f"Most Popular Start Hour: {popular_hour}",
    )


# Function to generate station statistics
def station_stats(df):
    popular_start_station = df["Start Station"].mode()[0]
    popular_end_station = df["End Station"].mode()[0]
    df["trip"] = df["Start Station"] + " to " + df["End Station"]
    popular_trip = df["trip"].mode()[0]

    return (
        f"Most Commonly Used Start Station: {popular_start_station}",
        f"Most Commonly Used End Station: {popular_end_station}",
        f"Most Common Trip: {popular_trip}",
    )


# Function to generate trip duration statistics
def trip_duration_stats(df):
    total_duration = df["Trip Duration"].sum()
    mean_duration = df["Trip Duration"].mean()

    return (
        f"Total Travel Time: {total_duration} seconds",
        f"Mean Travel Time: {mean_duration} seconds",
    )


# Function to generate user statistics
def user_stats(df):
    user_types_output = df["User Type"].value_counts().to_string()

    if "Gender" in df.columns:
        gender_counts_output = df["Gender"].value_counts().to_string()
    else:
        gender_counts_output = "Gender data not available"

    if "Birth Year" in df.columns:
        birth_year_stats_output = df["Birth Year"].describe().to_string()
    else:
        birth_year_stats_output = "Birth year data not available"

    return user_types_output, gender_counts_output, birth_year_stats_output


# Function to display raw data
def display_raw_data(df):
    return df.head().to_html(classes="table table-striped")


# Function to plot hourly distribution (example)
def plot_hourly_distribution(df):
    plt.figure(figsize=(10, 6))
    df["hour"] = df["Start Time"].dt.hour
    hourly_counts = df["hour"].value_counts().sort_index()
    plt.bar(hourly_counts.index, hourly_counts.values, color="skyblue")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Trips")
    plt.title("Distribution of Trips by Hour")
    plt.xticks(range(24))
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/explore", methods=["POST"])
def explore():
    city = request.form["city"]
    month = request.form["month"]
    day = request.form["day"]

    df = load_data(city, month, day)
    time_stats_output = time_stats(df)
    station_stats_output = station_stats(df)
    trip_duration_output = trip_duration_stats(df)
    user_stats_output = user_stats(df)
    raw_data_output = display_raw_data(df)

    # Generate plot
    hourly_distribution = plot_hourly_distribution(df)

    return render_template(
        "explore.html",
        city=city.title(),
        month=month.title(),
        day=day.title(),
        time_stats_output=time_stats_output,
        station_stats_output=station_stats_output,
        trip_duration_output=trip_duration_output,
        user_stats_output=user_stats_output,
        raw_data_output=raw_data_output,
        hourly_distribution=hourly_distribution,
    )


if __name__ == "__main__":
    app.run(debug=True)
