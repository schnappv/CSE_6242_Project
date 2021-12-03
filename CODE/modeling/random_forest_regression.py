import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor


class RFRegressor(object):
    """
    Random Forest Regressor for AQI x Mortality data
    """

    def __init__(self, target, features=None, random_seed=None, **kwargs):
        """
        Args:
            target (str): The target variable name
            features (list(str), optional): The feature variables. Defaults
                    to None, which will select all incoming dataframe columns
                    aside from target variable a feature.
            random_seed (int, optional): Give a random state to model for
                    reproducability. Defaults to None.
        """
        self.rf_reg = RandomForestRegressor(random_state=random_seed)
        self.seed = random_seed
        self.target = target
        self.features = features

    def _format_x(self, X):
        """
        Format the X variable dataframe to encode categorical features

        Args:
            X (pd.DataFrame): Dataframe of the feature variables

        Returns:
            updated_X (pd.DataFrame): Updated dataframe with binary
                    encoded features
        """
        categorical_cols = []
        for col in X.columns:
            if X[col].dtype == "object":
                categorical_cols.append(col)

        updated_X = pd.get_dummies(X, columns=categorical_cols)
        return updated_X

    def prep(self, df):
        """
        Prepare the data for model

        Args:
            df (pd.DataFrame): The initial dataframe to train on

        Returns:
            X (pd.DataFrame): The features dataframe formatted
            y (pd.Series): The target series
        """
        y = df[self.target]
        if self.features is None:
            X = df.drop(columns=[self.target])
            self.features = X.columns.tolist()
        else:
            X = df[self.features]

        X = self._format_x(X)
        return X, y

    def split_and_train(self, df, test_size=0.25):
        """
        Splits the data into training and testing and fits the inital model

        Args:
            df (pd.DataFrame): The initial dataframe to train on
            test_size (float, optional): Percentage of the data to be used
                    for testing. Defaults to 0.25.
        """
        self.X, self.y = self.prep(df)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=test_size,
            shuffle=True,
            random_state=self.seed,
        )
        self.rf_reg.fit(self.X_train, self.y_train)

    def hypertune(self, parameters=None):
        """
        Function to take the current model and hypertune it using the
        cross-validation method for specified parameters and then re-trains the
        model with the best parameters

        Args:
            parameters (dict, optional): Dictionary of parameters to try in
                    the cross-validation. Defaults to None, which set it as
                        # parameters = {
                        #    "n_estimators": [50, 100, 150, 200, 500],
                        #    "max_features": ["auto", "sqrt", "log2"],
            }
        """
        if parameters is None:
            parameters = {
                "n_estimators": [50, 100, 150, 200, 500],
                "max_features": ["auto", "sqrt", "log2"],
            }
        gscv_rfr = GridSearchCV(self.rf_reg, parameters)
        gscv_rfr.fit(self.X_train, self.y_train)

        best_params = gscv_rfr.best_params_
        print(best_params)
        self.rf_reg = RandomForestRegressor(**best_params)
        self.rf_reg.fit(self.X_train, self.y_train)

    def predict_score_train(self, round_target=True):
        """
        Gets the score of the prediction from the training set

        Args:
            round_target (bool, optional): If you want to round your target
                    variable. Defaults to True.

        Returns:
            y_predict_train (np.array): The array for the prediction
            score (float): The score of the prediction
        """
        y_predict_train = self.rf_reg.predict(self.X_train)
        if round_target:
            y_predict_train = np.round(y_predict_train)
        score = self.rf_reg.score(self.X_train, y_predict_train)

        return y_predict_train, score

    def predict_score_test(self, round_target=True):
        """
        Gets the score of the prediction from the testing set

        Args:
            round_target (bool, optional): If you want to round your target
                    variable. Defaults to True.

        Returns:
            y_predict_train (np.array): The array for the prediction
            score (float): The score of the prediction
        """
        y_predict_test = np.round(self.rf_reg.predict(self.X_test))
        if round_target:
            y_predict_test = np.round(y_predict_test)
        score = self.rf_reg.score(self.X_test, y_predict_test)

        return y_predict_test, score

    def predict_data(self, features_df, round_target=True):
        """
        Predict the value of the target from a dataframe that includes all
        the features as fields

        Args:
            features_df (pd.DataFrame): Dataframe you want to predict on
            round_target (bool, optional): If you want to round your target
                    variable. Defaults to True.

        Returns:
            new_df (pd.DataFrame): The given dataframe with an additional
                    column for the predicted target value
        """
        features_formatted = features_df[self.features]
        features_formatted = self._format_x(features_formatted)
        preds = self.rf_reg.predict(features_formatted)

        if round_target:
            preds = np.round(preds)
            features_df[self.target] = np.round(features_df[self.target])

        new_df = features_df
        pred_target_col_name = "predicted_{}".format(self.target)
        new_df[pred_target_col_name] = preds

        return new_df
