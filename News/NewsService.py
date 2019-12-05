import operator
import numpy as np
import warnings
from Adminpage.models import LearnNews,RealNews
from News.CreateModel import tagging_title
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import doc2vec
import pickle

# 모델 로딩
model_file = 'News/trainfiles/current/d2v_news.model'
d2v_model = doc2vec.Doc2Vec.load(model_file)
d2v_model.random = np.random.RandomState(0)

classifier_file = 'News/trainfiles/current/rf_news.sav'
rf_model = pickle.load(open(classifier_file, 'rb'))

# 뉴스 분류기
class NewsService:
    def classify_news(self, title):
        print(title)
        # 1. 토크나이징
        tokens = tagging_title(title)
        print(tokens)

        # 2. 벡터라이징
        vector = d2v_model.infer_vector(tokens)

        # 3. 추측
        target = rf_model.predict([vector])
        print(target)
        return RealNews.objects.create_news(title, tokens, target)




ns = NewsService()
print("NCS START!!!! 얄루~")