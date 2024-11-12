
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


def train(data):
    df = pd.read_csv(data)

    #------------------------train set split ---------------------------

    from sklearn.model_selection import train_test_split

    # Define features and target variable
    X = df.drop(columns=['label'])
    y = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    #--------------------------TRAINING TIME ----------------------------------
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)


    #---------------------------EVALUATION TIME---------------------------------

    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    #-----------------------------SAVE THE TRAINED MODEL---------------------------------------

    # Save trained model
    joblib.dump(clf, "trained_model.pkl")

    return X_test



#-----------------------------FUTURE USES(only for not forgetting, don't use atm)------------------------------
# Load the saved model
loaded_model = joblib.load("preprocessed_sensor_data.pkl")

# Use the loaded model for predictions
predictions = loaded_model.predict(train("2_mal_trinken.csv"))
