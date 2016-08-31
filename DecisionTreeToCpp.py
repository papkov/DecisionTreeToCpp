# -*- coding: utf-8 -*-
# 
# DecisionTreeToCpp converter allows you to export and use sklearn decision tree in your C++ projects
# It can be useful if you want only to use decision rules produced by powerful and simple scikit 
# (you can easy create and test different models, but compile only the best one)
# 
# This code was written as a modification of Daniele's answer in StackOverflow topic "how to extract the decision rules from scikit-learn decision-tree"
# http://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
# http://stackoverflow.com/users/1885917/daniele
#
# This is also my first open piece of code, so please do not expect too much - at least it works :)

def get_code(tree, feature_names, function_name="decision_tree"):
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, tabs):
        code = ''
        if threshold[node] != -2:
            code += (tabs * "\t") + "if (feature_vector->at(" + str(feature_names.index(features[node])) + ") <= " + str(round(threshold[node], 2)) + " ) {\n"
            tabs += 1

            if left[node] != -1:
                code += recurse(left, right, threshold, features, left[node], tabs)
            tabs -= 1
            code += (tabs * "\t") + "}\n" + (tabs * "\t") + "else {\n"

            tabs += 1
            if right[node] != -1:
                code += recurse(left, right, threshold, features, right[node], tabs)
            tabs -= 1
            code += (tabs * "\t") + "}\n"

        else:
            code += (tabs * "\t") + "return " + str(value[node].argmax()) + ";\n"

        return code

    code = "inline int %s(std::vector * feature_vector) \n{\n" % function_name
    code += recurse(left, right, threshold, features, 0, 1)
    code += "}"
    return code


def save_code(tree, feature_names, class_names, function_name="decision_tree"):

    feature_string = ""
    for i in range(0, len(feature_names)):
        feature_string += 'feature_vector[' + str(i) + '] - ' + feature_names[i] + '\n'
    classes_string = ""
    for i in range(0, len(class_names)):
        classes_string += str(i) + ' - ' + class_names[i] + '\n'

    preamble = """
/*
This inline function was automatically generated using DecisionTreeToCpp Converter

It takes feature vector as single argument:
%s

It returns index of predicted class:
%s

Simply include this file to your project and use it
*/

""" % (feature_string, classes_string)

    code = preamble + get_code(tree, feature_names, function_name)

    with open(function_name + '.h', "w") as f:
        f.write(code)
        print("File %s was written" % (function_name + '.h'))

    return 0


def main():
    print('This program was not designed to run standalone.')
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
