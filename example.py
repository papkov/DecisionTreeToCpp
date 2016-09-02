from sklearn.datasets import load_iris
from sklearn import tree
import DecisionTreeToCpp as to_cpp

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

print(to_cpp.get_code(clf, iris.feature_names))
to_cpp.save_code(clf, iris.feature_names, iris.target_names, function_name="iris_decision_tree")
