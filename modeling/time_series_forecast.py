import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet


class suppress_stdout_stderr(object):
    """
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    """

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


class TimeSeriesForecaster(object):
    """
    Time series forecaster using FBProphet Package
    """

    def __init__(
        self,
        seasonality_mode="multiplicative",
        mcmc_samples=300,
        weekly_seasonality=False,
        daily_seasonality=False,
        **kwargs
    ):
        self.m = Prophet(
            seasonality_mode=seasonality_mode,
            mcmc_samples=mcmc_samples,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
            **kwargs
        )

    def __time_series(self, df):
        df[self.date_col] = pd.to_datetime(df[self.date_col])
        ts_df = (
            df.dropna(subset=[self.date_col])
            .set_index(self.date_col)
            .resample(self.seasonality)
            .agg({self.y_col: self.agg})
            .dropna()
        )
        return ts_df.reset_index().rename(
            columns={self.date_col: "ds", self.y_col: "y"}
        )

    def fit(self, df, date_col, y_col, seasonality, agg="mean"):
        self.date_col = date_col
        self.y_col = y_col
        self.seasonality = seasonality
        self.agg = agg
        self.fb_df = self.__time_series(df)

        with suppress_stdout_stderr():
            self.m.fit(self.fb_df, verbose=False)

    def forecast(self, periods):
        future = self.m.make_future_dataframe(periods=periods, freq=self.seasonality)
        forecast = self.m.predict(future)
        forecast[self.y_col] = np.nan
        forecast.loc[: len(self.fb_df), self.y_col] = self.fb_df.y
        forecast = forecast.rename(columns={"ds": self.date_col})
        self.fcst = forecast
        return self.fcst

    def plot_forecast(self, figsize=(15, 8)):
        fig, ax = plt.subplots(figsize=figsize)
        plt.scatter(
            self.fb_df.ds,
            self.fb_df.y,
            color="k",
            s=10,
            label="Actual Data",
        )
        plt.plot(
            self.fcst[self.date_col],
            self.fcst.yhat,
            color="steelblue",
            label="Prediction",
        )
        ax.fill_between(
            x=self.fcst[self.date_col],
            y1=self.fcst.yhat_lower,
            y2=self.fcst.yhat_upper,
            alpha=0.3,
            color="steelblue",
            label="Prediction Interval: 95%",
        )
        plt.plot(
            self.fcst[self.date_col],
            self.fcst.trend,
            color="darkblue",
            label="Overall Trend",
        )
        plt.legend(bbox_to_anchor=(1.0, 1.0), loc="upper left")

        return fig, ax
