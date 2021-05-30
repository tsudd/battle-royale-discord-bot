from .config import SESSIONS_COLLECTION
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from .config import *
from .models import *

import random

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_topic_ref(tid):
    return db.collection(u"topics").document(str(tid))


def _get_player_or_default(data):
    doc = db.collection(PLAYERS_ACCESSOR).document(
        str(data[ID_ACCESSOR])).get()
    if not doc.exists:
        return Player(
            dis_id=data[ID_ACCESSOR],
            nick=data[NAME_ACCESSOR],
        )
    return Player.from_dict(doc.to_dict())


def save_player_and_part(data: dict, session: Session):
    p = _get_player_or_default(data)
    p.update_info(data, session.rounds_amount)
    db.collection(PLAYERS_ACCESSOR).document(str(p.id)).set(p.to_dict())
    db.collection(PARTICIPATIONS_COLLECTION).add(
        {
            SESSION_ACCESSOR: db.document(f"{SESSIONS_COLLECTION}/{session.id}"),
            PLAYER_ACCESSOR: db.document(f"{PLAYERS_ACCESSOR}/{p.id}")
        }
    )


def add_session_and_return(data):
    new_doc = db.collection(SESSIONS_COLLECTION).add({
        PLAYERS_AMOUNT: data[PLAYERS_AMOUNT],
        DEAD_AMOUNT: data[DEAD_AMOUNT],
        ROUNDS_AMOUNT: data[ROUNDS_AMOUNT],
        DATETIME_FIELD: data[DATETIME_FIELD],
        TOPIC_QUERY: data[TOPIC_QUERY]
    })
    doc = new_doc[1].get()
    if not doc.exists:
        raise ValueError
    serialized = doc.to_dict()
    serialized.update({ID_ACCESSOR: doc.id})
    return Session.from_dict(serialized)


def add_rounds(data: list, session: Session):
    s_ref = db.collection(SESSIONS_COLLECTION).document(session.id)
    num = 0
    for r in data:
        num += 1
        q_ref = _get_question_ref(r[QUESTION_ID_ACCESSOR])
        round_doc = s_ref.collection(ROUNDS_ACCESSOR).add(
            {
                QUESTION_ID_ACCESSOR: q_ref,
                ID_ACCESSOR: num
            }
        )
        _add_player_answers(
            round_doc[1], r[ANSWERS_ACCESSOR])


def get_player(uid):
    doc = _get_player_ref(uid).get()
    if doc.exists:
        return doc.to_dict()


def _get_question_ref(qid):
    # maybe there is no need in str
    return db.collection(QUESIONS_COLLECTION).document(str(qid))


def _add_player_answers(r_ref, answers: list):
    for a in answers:
        r_ref.collection(ANSWERS_ACCESSOR).add(a)


def _get_player_ref(uid):
    return db.collection(PLAYERS_ACCESSOR).document(str(uid))


def _get_topic_ref(tid):
    return db.collection(TOPICS_COLLECTION).document(str(tid))


def _get_variant_ref(qid, vid):
    return db.collection(QUESIONS_COLLECTION).document(
        str(qid)).collection(VARIANTS_ACCESSOR).document(str(vid))


def get_topics():
    return _get_dicts_by_refs(TOPICS_COLLECTION)


def _get_variants(doc):
    ans = []
    for d in doc.stream():
        ans.append(d.to_dict())
        ans[-1][ID_ACCESSOR] = d.id
    return ans


def get_player_sessions(uid, amount=10):
    parts = db.collection(PARTICIPATIONS_COLLECTION).where(
        PLAYER_ACCESSOR, u"==", _get_player_ref(uid))

    ans = []
    c = amount
    for d in parts.stream():
        ans.append(d.to_dict()[SESSION_ACCESSOR].get().to_dict())
        c -= 1
        if c == 0:
            break
    return ans


def _get_dicts_by_refs(collection):
    ans = []
    docs = db.collection(collection).stream()
    for d in docs:
        ans.append(d.to_dict())
        ans[-1][ID_ACCESSOR] = d.id
    return ans


def get_questions(topic, amount=10):
    ans = []
    docs = db.collection(QUESIONS_COLLECTION).where(
        TOPIC_QUERY, "==", _get_topic_ref(topic)).stream()
    refs = []
    for d in docs:
        refs.append(d)
    random.shuffle(refs)
    for d in refs[:amount]:
        q_ser = d.to_dict()
        q = {
            ID_ACCESSOR: d.id,
            QUESTION_STRING_FIELD: q_ser[QUESTION_STRING_FIELD],
            QUESTION_RIGHT_ANSWER: int(q_ser[QUESTION_RIGHT_ANSWER]),
            TOPIC_QUERY: q_ser[TOPIC_QUERY].id,
            VARIANTS_ACCESSOR: _get_variants(db.collection(
                f"{QUESIONS_COLLECTION}/{d.id}/{VARIANTS_ACCESSOR}"))
        }
        ans.append(q)
    return ans


def get_session(sid):
    s_ref = db.collection(SESSIONS_COLLECTION).document(sid)
    s = s_ref.get()
    if s.exists:
        ans = s.to_dict()
        ans[ROUNDS_ACCESSOR] = _get_rounds(s_ref)
        return ans


def _get_rounds(s_ref):
    rounds = s_ref.collection(ROUNDS_ACCESSOR).stream()
    ans = []
    for r in rounds:
        r_ser = r.to_dict()
        variants = r_ser[QUESTION_ID_ACCESSOR].collection(
            VARIANTS_ACCESSOR).get()
        ans.append({
            ANSWERS_ACCESSOR: _get_answers(s_ref.collection(ROUNDS_ACCESSOR).document(r.id), variants),
            QUESTION_ID_ACCESSOR: r_ser[QUESTION_ID_ACCESSOR].get().to_dict()[
                QUESTION_STRING_FIELD]
        })
    return ans


def _get_answers(r_ref, variants):
    answers = r_ref.collection(ANSWERS_ACCESSOR).stream()
    ans = []
    for a in answers:
        ser_a = a.to_dict()
        ans.append({
            PLAYER_ACCESSOR: ser_a[UID_ACCESSOR],
            ANSWER_STATUS_ACCESSOR: ser_a[ANSWER_STATUS_ACCESSOR],
            ANSWER_ACCESSOR: variants[ser_a[QUESTION_VARIANT] -
                                      1].get(QUESTION_VARIANT)
        })
    return ans
