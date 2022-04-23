import pandas as pd
from category_encoders import BinaryEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import aux_function as af

model = "rf"
verbose_level = 0
fract = 1  # setting the usage of samples (eg. 4 ==> usiamo un quarto dei dati, 1 ==> usiamo tutti i dati)
cv_val = True
traits_encoding = False

dataset = pd.read_csv('export_dataframe.csv')
print(dataset.columns.values)
print(dataset.shape)
if traits_encoding:
    af.merge_traits(dataset)

N = dataset.shape[0]
N = int(N / fract)

y = dataset.iloc[:N, 6].values
print("y:\n", y[:5], y.shape)  # first 5  y-values
print()
if traits_encoding:
    to_remove = ["trait_" + str(i) for i in range(28)]
    dataset = dataset.drop(to_remove, axis=1, errors='ignore')
    x = dataset.loc[:(N - 1), ~dataset.columns.isin(['match_id', 'placement'])]
    print(x.columns)
    x = x.values
else:
    x = dataset.loc[:(N - 1), ~dataset.columns.isin(['match_id', 'placement', 'merged_traits'])]
    print(x.columns)
    x = x.values
print("x:\n", x[0, :], x.shape)  # first x-row
print()

# binary encoding
be = BinaryEncoder()
x = be.fit_transform(x)
print("x binary encoded:\n", x, x.shape)
print()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# feature scaling
ss = StandardScaler()
x_train = ss.fit_transform(x_train)
x_test = ss.fit_transform(x_test)

# XXX svm
if model == "SVM":
    print("SVM classifier")
    classifier = SVC(kernel='rbf', random_state=0, verbose=verbose_level)
# XXX rf
elif model == "rf":
    # TODO hyperparameter tuning (check session buddy) on MAX_DEPTH
    # max_depth = None
    print("Random Forest classifier")
    classifier = RandomForestClassifier(random_state=0, verbose=verbose_level)
# XXX default
else:
    print("Error Model")
    print("*** setting the default classifier SVM ***")
    print("SVM classifier")
    classifier = SVC(kernel='rbf', random_state=0, verbose=verbose_level)

classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print("accuracy:\n", accuracy)
print()

confusion = confusion_matrix(y_test, y_pred)
print("confusion matrix:\n", confusion)
print()

if cv_val:
    cv = cross_val_score(classifier, x, y, cv=10, scoring='accuracy')
    print("cross validation:\n", cv)
    print()

