import pandas as pd
import matplotlib.pyplot as plt


def grafics(df: pd.DataFrame) -> None:
    """
    Plots bar charts for day and night temperatures.
    parametrs:
    df: pandas DataFrame containing the temperature data. 
    """
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(40, 8))
    plt.subplots_adjust(wspace=0.3, hspace=0.3)

    axes[0].bar(df["Number"], df["Day temperature"], color="#5900A6")
    axes[0].set(title="Day temperature")
    axes[0].set_xlabel("date")
    axes[0].set_ylabel("temp")

    axes[1].bar(df["Number"], df["Night temperature"], color="#5900A6")
    axes[1].set(title="Night temperature")
    axes[1].set_xlabel("date")
    axes[1].set_ylabel("temp")

    plt.show()


def grafics_date(df: pd.DataFrame, month: int, year: int) -> None:
    """
    Plots day temperature, median, and mean for a specific month and year.
    parametrs:
    df: pandas DataFrame containing the temperature data.
    month: month to filter the data for (1 to 12).
    year: year to filter the data for.
    """
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(40, 8))
    tmp_df = df.loc[(df["Number"].dt.year == year) & (df["Number"].dt.month == month)]
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    axes[0].plot(tmp_df["Number"], tmp_df["Day temperature"], color="#5900A6")
    axes[0].set(title="Day temperature")
    axes[0].set_xlabel("date")
    axes[0].set_ylabel("temp")

    axes[1].plot(
        tmp_df["Number"],
        tmp_df["Day temperature"].rolling(20).median(),
        color="#5900A6",
    )
    axes[1].set(title="Median")
    axes[1].set_xlabel("date")
    axes[1].set_ylabel("temp")

    axes[2].plot(
        tmp_df["Number"], tmp_df["Day temperature"].rolling(20).mean(), color="#5900A6"
    )
    axes[2].set(title="Mean")
    axes[2].set_xlabel("date")
    axes[2].set_ylabel("temp")

    plt.show()


def temperature_filter(df: pd.DataFrame, temp: float) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows where 'Day temperature'
    is greater than or equal to a given temperature.
    """
    return df[df["Day temperature"] >= temp]


def number_filter(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    Filters the DataFrame by date range.
    """
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    return df.loc[(df["Number"] >= start) & (df["Number"] <= end)]


def groupby_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups the DataFrame by month and calculates the average values of various temperature columns
    parametrs:
    df: A pandas DataFrame containing the temperature data.
    return:
    df: A pandas DataFrame with the mean values of temperature columns grouped by month.
    """
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    return df.groupby(df["Number"].dt.month)[
        "Day temperature",
        "Night temperature",
        "Fahrenheit (afternoon)",
        "Fahrenheit (night)",
    ].mean()


def statistics(df: pd.DataFrame) -> None:
    """
    Prints statistics for various temperature columns in the DataFrame.
    parametrs:
    df: A pandas DataFrame containing the temperature data.
    """
    print(
        df["Day temperature"].describe(),
        df["Night temperature"].describe(),
        df["Fahrenheit (afternoon)"].describe(),
        df["Fahrenheit (night)"].describe(),
    )


def datafrem() -> pd.DataFrame:
    """
    Uploads a CSV file to a DataFrame and processes the data.
    return:
    df: DataFrame with processed data
    """
    df = pd.read_csv("dataset.csv", sep=",")
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    df.fillna(
        {
            "Day temperature": df["Day temperature"].mean(),
            "Day pressure": "no data",
            "Day wind": "no data",
            "Night temperature": df["Night temperature"].mean(),
            "Night pressure": "no data",
            "Night wind": "no data",
        },
        inplace=True,
    )
    df["Fahrenheit (afternoon)"] = df["Day temperature"] * 1.8 + 32
    df["Fahrenheit (night)"] = df["Night temperature"] * 1.8 + 32
    return df


if __name__ == "__main__":
    df = datafrem()