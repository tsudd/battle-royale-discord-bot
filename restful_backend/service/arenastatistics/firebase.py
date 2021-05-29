from .config import DATETIME_FIELD, DEAD_AMOUNT, PLAYERS_AMOUNT, ROUNDS_AMOUNT
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_topic_ref(tid):
    return db.collection(u"topics").document(str(tid))


def get_player(uid):
    doc = db.collection(u"players").document(str(uid)).get()
    if not doc.exists:
        raise ValueError
    return doc.to_dict()


def serialize_questions(questions):
    ans = []
    for q in questions:
        qq = q.get()
        a = {
            "id": q.id,
            "variants": [v.to_dict() for v in q.get().collection(u"variants").stream()],
            "right_ind": q.right_ind,
            "topic": q.topic.id
        }
        ans.append(a)
    return ans


def session_save(session):
    ref = db.collection(u"sessions").add({
        PLAYERS_AMOUNT: session[PLAYERS_AMOUNT],
        DEAD_AMOUNT: session[DEAD_AMOUNT],
        ROUNDS_AMOUNT: session[ROUNDS_AMOUNT],
        DATETIME_FIELD: session[DATETIME_FIELD]
    })
