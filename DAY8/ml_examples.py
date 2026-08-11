examples = {
    "Email Spam Detection": "Supervised Learning - Classification",
    "House Price Prediction": "Supervised Learning - Regression",
    "Student Marks Prediction": "Supervised Learning - Regression",
    "Customer Segmentation": "Unsupervised Learning - Clustering",
    "News Article Grouping": "Unsupervised Learning - Clustering",
    "Fraud Detection": "Supervised Learning - Classification"
}

print("Real-Life Machine Learning Examples\n")

for example, ml_type in examples.items():
    print(example, "->", ml_type)