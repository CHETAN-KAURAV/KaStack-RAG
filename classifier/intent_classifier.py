import joblib

model = joblib.load("classifier/intent_model.pkl")

while True:

    text = input("\nMessage: ")

    if text.lower() == "exit":
        break

    prediction = model.predict([text])[0]

    print("Intent:", prediction)