import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
import sklearn.model_selection as model_selection


class PredictionModule:
    """
    wraps DNN's and other regression modules


        other regressors you can use
        sklearn.neighbors.KNeighborsRegressor(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None,
    """
    def __init__(self, **kwargs):
        """
        initializes the model
        :param kwargs:
            'trained_already' - if not None, pass in the file path ('*.sav') for the serialized model. default False (to indicate not trained)
            'model_type' - if not None, pass in the the appropriate input, default is MLPRegressor
            'hidden_layer_sizes' - if not None, pass in the the appropriate input, default is (13,10,8)
            'activation_func' - if not None, pass in the the appropriate input, default is 'relu'
            'solver' - if not None, pass in the the appropriate input, default is 'adam'
            'verbos' - if not None, pass in the the appropriate input, default is True
        """
        if kwargs.get('model_type') is not None:
            model_type = kwargs.get('model_type')
        else:
            model_type = MLPRegressor
        if kwargs.get('hidden_layer_sizes') is not None:
            self.hidden_layer_sizes = kwargs.get('hidden_layer_sizes')
        else:
            self.hidden_layer_sizes = (13, 10, 8)
        if kwargs.get('activation_func') is not None:
            self.activation_func = kwargs.get('activation_func')
        else:
            self.activation_func = 'relu'
        if kwargs.get('solver') is not None:
            self.solver = kwargs.get('solver')
        else:
            self.solver = 'adam'
        if kwargs.get('verbos') is not None:
            self.verbose = kwargs.get('verbos')
        else:
            self.verbose = True
        if kwargs.get('trained_already') is not None:
            trained_already = kwargs.get('trained_already')
            # load the model from disk
            self.model = pickle.load(open(trained_already, 'rb'))
            self.was_trained = True
        else:
            self.was_trained = False
            self.model = model_type(hidden_layer_sizes=self.hidden_layer_sizes, activation=self.activation_func, solver=self.solver, verbose=self.verbose)

    def fit_model(self, x_train: np.ndarray, y_train: np.ndarray):
        self.model = self.model.fit(x_train, y_train)
        params = self.model.get_params()
        self.was_trained = True
        # save the model to disk
        filename = 'finalized_model.sav'
        pickle.dump(self.model, open(filename, 'wb'))

    def predict_model(self, X: np.ndarray, **kwargs):
        if not self.was_trained:
            raise Exception("The model wasn't trained!")
        results = self.model.predict(X)

    def get_model_score(self, X: np.ndarray, Y_true: np.ndarray):
        return self.model.score(X, Y_true)


class DataPreprocessor:
    """
    a class to preprocess the data, preparing it to our
    specific needs.
    uses a default normalizer from the type MinMaxScaler,
    if you want a diffrenet scaler pass it (already initialized) in
    the constructor as an argument (see docs)
    """

    def __init__(self, **kwargs):
        """
        kwargs:
        'normalization_model' - an initialized normalization scaler,
        such as the MinMaxScaler from sklearn
        :param kwargs:
        """
        if kwargs.get('normalization_model') is not None:
            self.normalization_model = kwargs.get('normalization_model')
        else:
            self.normalization_model = MinMaxScaler(feature_range=(-1, 1))

    def pre_proceesing_regression(self, data_frame: pd.DataFrame, **kwargs):
        """
        receives a full data frame with the y axis (prediction), as the last
        feature.
        can get the kwargs:
            test_size = for the the split.
            random_state = for the the split.
        :param df:
        :param kwargs:
        :return:
        """
        if kwargs.get('test_size') is not None:
            test_size = kwargs.get('test_size')
        else:
            test_size = 0.33
        if kwargs.get('random_state') is not None:
            random_state = kwargs.get('random_state')
        else:
            random_state = 42

        X = data_frame.iloc[:, 1:-1].values
        y = data_frame.iloc[:, -1].values
        data = self.normalization_model.fit_transform(X, y)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(data, y,
                                                                            test_size=test_size,
                                                                            random_state=random_state,
                                                                            shuffle=True)
        return X_train, X_test, y_train, y_test


# Example for Data Processor
# dp = DataPreprocessor()
#
# PATH_TO_FILE = "/Users/yishaiazabary/PycharmProjects/MigHtyFi/data_2015.csv"
#
# data_frame = pd.read_csv(PATH_TO_FILE)
# print(dp.pre_proceesing_regression(data_frame))
