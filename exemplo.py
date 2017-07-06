import MySQLdb as mdb
from MySQLdb import cursors
from nltk import word_tokenize
import gensim


class MySqlHelper(object):
    def __init__(self):
        self.con = mdb.connect(**MYSQL[CONLINE_DB])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.con:
            self.con.close()

    def fetch_resumes(self, num_train_examples):
        query = """query sql :P""".format(num_train_examples)
        cursor = self.con.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            yield row['???']
        cursor.close()


def train_word2vec(num_train_examples=100000, min_count=100):
    with MySqlHelper() as db:
        resumes = db.fetch_resumes(num_train_examples)

        tokenized_resumes = [
            word_tokenize(curriculo.lower(), language='portuguese')
            for curriculo in resumes
        ]
        phrases = gensim.models.Phrases(tokenized_resumes)

        model = gensim.models.Word2Vec(
            phrases[tokenized_resumes],
            min_count=min_count
        )
        model.init_sims(replace=True)
    return model

model = train_word2vec()
model.save('word2vec_model')
