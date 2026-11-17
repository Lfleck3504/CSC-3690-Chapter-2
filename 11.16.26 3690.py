import pandas as pd
import numpy as np
from pprint import pprint
from pathlib import Path



def entropy(targetCol):
    if len(targetCol) == 0:
        return 0.0

    _, counts = np.unique(targetCol, return_counts=True)
    probabilities = counts / counts.sum()

    return float(-np.sum(probabilities * np.log2(probabilities)))


def informationGain(data, feature, target="species"):
    if data.empty:
        return 0.0

    totalEntropy = entropy(data[target])
    values, counts = np.unique(data[feature], return_counts=True)

    weightedEntropy = np.sum([
        (counts[i] / np.sum(counts)) *
        entropy(data[data[feature] == values[i]][target])
        for i in range(len(values))
    ])

    return float(totalEntropy - weightedEntropy)


def id3(data, originalData, features, target="species",
        parentNodeClass=None, depth=0):

    indent = "    " * depth


    if data.empty:
        if parentNodeClass is not None:
            print(f"{indent}Empty subset -> {parentNodeClass}")
            return parentNodeClass

        if originalData.empty:
            raise ValueError("Cannot build a decision tree without training data.")

        classes, counts = np.unique(
            originalData[target], return_counts=True
        )
        return classes[np.argmax(counts)]


    classes, counts = np.unique(data[target], return_counts=True)


    if len(classes) == 1:
        print(f"{indent}Leaf node -> {classes[0]}")
        return classes[0]


    parentNodeClass = classes[np.argmax(counts)]


    if len(features) == 0:
        print(f"{indent}No features left -> {parentNodeClass}")
        return parentNodeClass


    print(f"\n{indent}----------------------------------")
    print(f"{indent}Samples: {len(data)}")
    print(f"{indent}Class counts: {dict(zip(classes, counts))}")
    print(f"{indent}Entropy: {entropy(data[target]):.5f}")


    gains = []

    for feature in features:
        gain = informationGain(data, feature, target)
        gains.append(gain)

        print(
            f"{indent}Information Gain ({feature}): "
            f"{gain:.5f}"
        )

    bestFeature = features[np.argmax(gains)]

    print(f"{indent}Best feature: {bestFeature}")


    tree = {bestFeature: {}}


    remainingFeatures = [
        feature for feature in features
        if feature != bestFeature
    ]


    for value in np.unique(data[bestFeature]):

        print(f"{indent}Branch: {bestFeature} = {value}")

        subset = data[data[bestFeature] == value]

        subtree = id3(
            subset,
            originalData,
            remainingFeatures,
            target,
            parentNodeClass,
            depth + 1
        )

        tree[bestFeature][value] = subtree

    return tree


def predict(tree, example):

    # Normalize feature names and values
    example = {
        str(key).strip().casefold():
        str(value).strip().casefold()
        for key, value in example.items()
    }

    print("\nPrediction Steps:")

    # Traverse decision tree                                                                                             #imma copy/paste this stuff later
    while isinstance(tree, dict):

        feature = next(iter(tree))
        featureKey = feature.strip().casefold()

        if featureKey not in example:
            raise ValueError(f"Missing feature: {feature}")

        branches = tree[feature]

        matchingValues = [
            value for value in branches
            if str(value).strip().casefold() == example[featureKey]
        ]

        if not matchingValues:
            raise ValueError(
                f"Unknown value for {feature}: "
                f"{example[featureKey]}"
            )

        selectedValue = matchingValues[0]

        print(f"{feature} = {selectedValue}")

        tree = branches[selectedValue]

    print(f"Reached leaf node: {tree}")

    return tree



if __name__ == "__main__":
    csvPath = Path(__file__).resolve().parent.parent / "species.csv"

    data = pd.read_csv(csvPath)

    # Remove extra column names and values
    data.columns = data.columns.str.strip()

    for column in data.columns:
        if data[column].dtype == "object":
            data[column] = data[column].str.strip()


    target = "species"


    features = [
        column for column in data.columns
        if column != target
    ]


    print("\nTraining Dataset:")
    print(data.to_string(index=False))

    print("\n========== ID3 ALGORITHM STEPS ==========")
    tree = id3(
        data,
        data,
        features,
        target=target
    )
    print("\n========== FINAL DECISION TREE ==========")
    pprint(tree, sort_dicts=False)
    newExample = {
        "toothed": "Toothed",
        "Hair": "Hair",
        "Breathes": "not Breathes",
        "Legs": "legs"
    }
    print("\n========== NEW EXAMPLE ==========")
    pprint(newExample)
    predictedSpecies = predict(tree, newExample)
    print("\n========== FINAL PREDICTION ==========")
    print("Predicted species:", predictedSpecies)
