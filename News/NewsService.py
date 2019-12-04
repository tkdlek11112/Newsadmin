import operator
import numpy as np
import warnings
from Adminpage.models import LearnNews,RealNews
from News.CreateModel import tagging_title
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import doc2vec
import pickle


model_file = 'News/trainfiles/current/d2v_news.model'
d2v_model = doc2vec.Doc2Vec.load(model_file)
d2v_model.random = np.random.RandomState(0)

classifier_file = 'News/trainfiles/current/rf_news.sav'
rf_model = pickle.load(open(classifier_file, 'rb'))


class NewsService:
    def classify_news(self, title):
        print(title)
        tokens = tagging_title(title)
        print(tokens)
        vector = d2v_model.infer_vector(tokens)
        target = rf_model.predict([vector])
        print(target)
        return RealNews.objects.create_news(title, tokens, target)

    def get_target(self):
        print('get_target')




ns = NewsService()
print("hihi")