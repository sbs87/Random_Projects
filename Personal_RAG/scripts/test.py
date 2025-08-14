
import joblib
def embeddings_alt():
    EMBEDDINGS = joblib.load("embeddings.joblib")
    print(EMBEDDINGS)

embeddings_alt()