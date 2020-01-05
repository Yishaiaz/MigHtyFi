import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
import sklearn.model_selection as model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, KBinsDiscretizer


class KNearNeighborsPrediction:
    """
    the prediction model of choice.
    this class wraps KNeighborsClassifier from sklearn to MightyFi specific needs.
    """
    def __init__(self, **kwargs):
        """
        if you wish to train the model separately, pass kwarg 'train_model=False'.
        if you wish to change the model n_neighbors parameter, pass kwag 'n_neighbors=YOUR NUM'

        if no arguments were passed the model will be for n_neighbors=20, and will train upon initiation.
        :param kwargs: train_model, n_neighbors
        """
        self.was_trained = False
        self.feature_number = 14
        if kwargs.get('train_model') is not None:
            train_model = kwargs.get('train_model')
        else:
            train_model = True
        if kwargs.get('n_neighbors') is not None:
            self.n_neighbors = kwargs.get('n_neighbors')
        else:
            self.n_neighbors = 20
        self.classifier = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        if train_model:
            dataset = pd.read_csv("ExtractedData/compressed_data_no_name.csv")
            # PRE PROCESSING
            dataset.fillna(dataset.median(), inplace=True)
            # our y axis discretization
            bins = [0, 100000, 500000, 1000000, 100000000, 250000000, 500000000, 1000000000, 10000000000]
            labels = ["{0}-{1}".format(bins[i], bins[i + 1]) for i in range(len(bins) - 1)]
            self.X = dataset.iloc[:, :-1].values
            y = pd.cut(dataset.iloc[:, -1], bins, labels=labels)
            # rescale the data
            self.scaler = StandardScaler()
            self.scaler.fit(self.X)

            # train the model with the entire dataset
            X_train = self.scaler.transform(self.X)
            self.train(self.X, y)

    def train(self, X_train, y_train):
        """
        uses the sklearn model fit() method, marks the model as trained via inner attribute.
        :param X_train:
        :param y_train:
        :return:
        """
        self.classifier.fit(X_train, y_train)
        self.was_trained = True

    def predict(self, X_test):
        """
        returns the predicted label.
        :raises an exception if the model wasn't trained before hand.
        :param X_test:
        :return:
        """
        if self.was_trained:
            return self.classifier.predict(self.scaler.transform(X_test))
        else:
            raise Exception("The model was not trained!")


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
        if kwargs.get('max_iter') is not None:
            self.max_iter = kwargs.get('max_iter')
        else:
            self.max_iter = 50000
        if kwargs.get('hidden_layer_sizes') is not None:
            self.hidden_layer_sizes = kwargs.get('hidden_layer_sizes')
        else:
            self.hidden_layer_sizes = (4, 2, 4)
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
            self.model = model_type(hidden_layer_sizes=self.hidden_layer_sizes, activation=self.activation_func, solver=self.solver, verbose=self.verbose, max_iter=self.max_iter, tol=0.001)

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
        return self.model.predict(X)

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
            self.normalization_model = MinMaxScaler(feature_range=(-1000, 1000))

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
        data_frame.fillna(data_frame.median(), inplace=True)
        X = data_frame.iloc[:, 1:-1].values
        y = data_frame.iloc[:, -1].values
        data = self.normalization_model.fit_transform(X)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(data, y,
                                                                            test_size=test_size,
                                                                            random_state=random_state,
                                                                            shuffle=True)
        return X_train, X_test, y_train, y_test



# # Example for Data Processor
# if __name__ == '__main__':
#     dp = DataPreprocessor()
#     pm = PredictionModule(hidden_layer_sizes=(17, 10, 8), solver='adam', activation_func='tanh')
#
#     #
#     PATH_TO_FILE = "/Users/yishaiazabary/PycharmProjects/MigHtyFi/ExtractedData/data_no_name.csv"
#     #
#     data_frame = pd.read_csv(PATH_TO_FILE)
#     data_frame.fillna(data_frame.median(), inplace=True)
#     bins = [0, 100000, 500000, 1000000, 100000000, 250000000, 500000000, 1000000000, 10000000000]
#     labels = [x for x in bins][:-1]
#     X = data_frame.iloc[:, 1:-1].values
#     y = pd.cut(data_frame.iloc[:, 5], bins, labels=labels)
#     # X_train, X_test, y_train, y_test = dp.pre_proceesing_regression()
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
#     pm.fit_model(X_train, y_train)
#     prediction_vector = pm.predict_model(X_test)
#     print(prediction_vector[prediction_vector==y_test])
