from category_encoders import BinaryEncoder
from numpy import ravel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from reformat import *


class Classifier:
    def __init__(self, model="RF", verbose=0, fract=2, cv_val=True, format="A", test_size=0.25, encoding=1,
                 scaling=False, n_fold=10, two_class=False):
        self.model = model
        self.verbose = verbose
        self.fract = fract
        self.cv_val = cv_val
        self.format = format
        self.test_size = test_size
        self.binary_encoding = encoding
        self.scaling = scaling
        self.n_fold = n_fold
        self.two_class = two_class

        df = pd.read_csv('export_dataframe.csv')
        self.dataset = reformat_to(df, format=self.format, verbose=self.verbose, two_class=self.two_class)

        self.x, self.y = self.load_dataset()

        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.classifier = None

        self.accuracy_list = []
        self.confusion_list = []
        self.cv_list = []

    def fit(self):
        if self.binary_encoding == 1:
            be = BinaryEncoder()
            self.x = be.fit_transform(self.x)
            print("x binary encoded:\n", self.x, self.x.shape)
        elif self.binary_encoding == 2:
            ohe = OneHotEncoder()
            self.x = ohe.fit_transform(self.x)
            print("x one hot encoded:\n", self.x, self.x.shape)
        else:
            print("No encoding needed")

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y,
                                                                                test_size=self.test_size,
                                                                                random_state=0)

        if self.scaling:
            ss = StandardScaler()
            self.x_train = ss.fit_transform(self.x_train)
            self.x_test = ss.fit_transform(self.x_test)

        if self.model == "SVM":
            print("SVM classifier")
            self.classifier = SVC(kernel='rbf', random_state=0, verbose=0)
        # XXX rf
        elif self.model == "RF":
            # max_depth = None
            print("Random Forest classifier")
            self.classifier = RandomForestClassifier(random_state=0, verbose=0)
        elif self.model == "DT":
            N = self.dataset.shape[0]
            N = int(N / self.fract)
            # max_depth = None
            min_samples_leaf = int(N / 500)
            print("Decision Tree classifier")
            self.classifier = DecisionTreeClassifier(random_state=0)
        else:
            # XXX default
            print("Error Model")
            print("*** setting the default classifier SVM ***")
            print("SVM classifier")
            self.classifier = SVC(kernel='rbf', random_state=0, verbose=0)

        self.classifier.fit(self.x_train, self.y_train)
        y_pred = self.classifier.predict(self.x_test)

        # if self.verbose == 3:
        #     self.print_preds(y_pred, self.y_test)

        accuracy = accuracy_score(self.y_test, y_pred)
        print("accuracy:\n", accuracy)
        print()
        self.accuracy_list.append(accuracy)

        confusion = confusion_matrix(self.y_test, y_pred)
        print("confusion matrix:\n", confusion)
        print()
        self.confusion_list.append(confusion)

        if self.cv_val:
            cv = cross_val_score(self.classifier, self.x, self.y, cv=self.n_fold, scoring='accuracy')
            print("cross validation:\n", cv)
            print()
            self.cv_list.append(cv)

        if self.verbose:
            print("************************** END format", str(self.format), "model", self.model,
                  "**************************")

    def load_dataset(self):
        N = self.dataset.shape[0]
        N = int(N / self.fract)

        y = self.dataset.loc[:N, self.dataset.columns.isin(['placement'])]
        if self.verbose:
            print("y")
            print(y.shape)
            print(y.head())

        x = self.dataset.loc[:N, ~self.dataset.columns.isin(['placement'])]
        if self.verbose:
            print("x")
            print(x.shape)
            print(x.head())

        return x.values, ravel(y.values)

    def print_preds(self, y_pred, y_test):
        count_ok = 0
        count_NOT_ok = 0
        for i in range(len(y_pred)):
            if 1 <= y_pred[i] <= 4:
                if 1 <= y_test[i] <= 4:
                    count_ok = count_ok + 1
                else:
                    count_NOT_ok = count_NOT_ok + 1
            else:
                if 4 < y_test[i] <= 8:
                    count_ok = count_ok + 1
                else:
                    count_NOT_ok = count_NOT_ok + 1
        print("OK", count_ok)
        print("NOT", count_NOT_ok)


if __name__ == "__main__":
    cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="K", test_size=0.25, encoding=0,
                    two_class=True)
    cc.fit()

    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="C", test_size=0.25, encoding=1,
    #                 two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="A", test_size=0.25, encoding=1,
    #                 two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="D", test_size=0.25, encoding=1,
    #                 two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="T", test_size=0.25, encoding=0,
    #                 two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="I", test_size=0.25, encoding=0,
    #                 two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=1, fract=3, cv_val=False, format="X", test_size=0.25, encoding=0,
    #                 two_class=True)
    # cc.fit()

    # fig = plt.figure(figsize=(100, 50))
    # _ = plot_tree(cc.classifier, feature_names=cc.dataset.columns.values.tolist(), class_names=["tette", "win"],
    #               filled=True)
    # # plt.show()
    # fig.savefig("decistion_tree.png")

    ## import graphviz
    ## dot_data = export_graphviz(cc, out_file=None)
    ## graph = graphviz.Source(dot_data)
    ## graph.render("iris")

    # cc = Classifier(model="DT", verbose=4, fract=3, cv_val=False, format="A", test_size=0.25, binary_encoding=True, two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=4, fract=3, cv_val=False, format="C", test_size=0.25, binary_encoding=True, two_class=True)
    # cc.fit()
    #
    # cc = Classifier(model="DT", verbose=4, fract=3, cv_val=False, format="D", test_size=0.25, binary_encoding=True, two_class=True)
    # cc.fit()
