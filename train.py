"""Train a small classifier on the Iris dataset and save it to disk."""
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

joblib.dump(
    {"model": model, "classes": list(iris.target_names)},
    "model.joblib",
)
print("Saved model.joblib")
