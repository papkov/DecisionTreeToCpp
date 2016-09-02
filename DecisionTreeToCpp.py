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


def get_code(tree, feature_names, function_name="decision_tree"):
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, tabs):
        code = ''
        if threshold[node] != -2:
            code += '%sif (feature_vector.at(%s) <= %s) {\n' % (tabs * '\t', feature_names.index(features[node]), round(threshold[node], 2))
            tabs += 1

            if left[node] != -1:
                code += recurse(left, right, threshold, features, left[node], tabs)
            tabs -= 1
            code += '%s}\n%selse {\n' % (tabs * '\t', tabs * '\t')

            tabs += 1
            if right[node] != -1:
                code += recurse(left, right, threshold, features, right[node], tabs)
            tabs -= 1
            code += '%s}\n' % (tabs * '\t')

        else:
            code += '%sreturn %s;\n' % (tabs * '\t', value[node].argmax())

        return code

    code = "inline int %s(const std::vector<double> & feature_vector) \n{\n%s}" \
           % (function_name, recurse(left, right, threshold, features, 0, 1))
    return code


def save_code(tree, feature_names, class_names, function_name="decision_tree"):

    feature_string = ""
    for i in range(0, len(feature_names)):
        feature_string += 'feature_vector[%s] - %s\n' % (i, feature_names[i])
    classes_string = ""
    for i in range(0, len(class_names)):
        classes_string += '%s - %s\n' % (i, class_names[i])

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

    code = '%s#include <vector>\n\n%s' % (preamble, get_code(tree, feature_names, function_name))

    with open(function_name + '.h', "w") as f:
        f.write(code)
        print("File %s was written" % (function_name + '.h'))

    return 0


def main():
    print('This program was not designed to run standalone.')
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
