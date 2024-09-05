import pandas as pd
import matplotlib.pyplot as plt


def grafics(df: pd):
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


def grafics_date(df: pd, month: int, year: int):
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


def temperature_filter(df: pd, temp: float):
    return df[df["Day temperature"] >= temp]


def number_filter(df: pd, start: str, end: str):
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    return df.loc[(df["Number"] >= start) & (df["Number"] <= end)]


def groupby_date(df: pd):
    df["Number"] = pd.to_datetime(df["Number"], format="%Y-%m-%d")
    return df.groupby(df["Number"].dt.month)[
        "Day temperature",
        "Night temperature",
        "Fahrenheit (afternoon)",
        "Fahrenheit (night)",
    ].mean()


def statistics(df: pd) -> None:
    print(
        df["Day temperature"].describe(),
        df["Night temperature"].describe(),
        df["Fahrenheit (afternoon)"].describe(),
        df["Fahrenheit (night)"].describe(),
    )


def datafrem() -> pd:
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
    start = "2020-10-08"
    end = "2021-11-17"
    # print(df)
    # print(number_filter(df, start, end))
    # print(groupby_date(df))
    # grafics(df)
    #grafics_date(df, 7, 2012)
    #print(df.loc[2800])
    # temperature_filter(df, 21)
    # statistics(df)
