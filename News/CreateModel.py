import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import doc2vec
from Adminpage.models import LearnNews, LearnLog
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
from News.models import UserDic, StopWord
from ckonlpy.tag import Twitter, Postprocessor
from gensim.models.doc2vec import TaggedDocument
import multiprocessing
import jpype
import ast

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import doc2vec

User_Dic = ['스탁론','투자금','점유율','추천','수혜주','중장기','언론사','매수','수익주','추천','수수료','대환',
            '싹슬이','중장기','바닥주','상한가','투자금','대박주','관심주','시초가','대장주','급등주','카카오톡',
            'VIP','카톡방','저평가','전재','재배포','제레미']

StopWord = {'등', '및', '것', '이'}

# 학습데이터 전체 태깅
def tag_learn_data():
    learnnews_models = LearnNews.objects.filter(tokens='')
    okt = Twitter()
    okt.add_dictionary(User_Dic, 'Noun')
    postprocessor = Postprocessor(okt, stopwords=StopWord)
    jpype.attachThreadToJVM()

    for model in learnnews_models:
        tokens = [word[0] for word in postprocessor.pos(model.title) if word[1] in ['Noun']]
        model.tokens = tokens
        model.save()

# 뉴스 태깅하기
def tagging_title(title):
    okt = Twitter()
    okt.add_dictionary(User_Dic, 'Noun')
    postprocessor = Postprocessor(okt, stopwords=StopWord)
    jpype.attachThreadToJVM()
    tokens = [word[0] for word in postprocessor.pos(title) if word[1] in ['Noun']]
    return tokens


# 사용자 정의사전 로드
def load_user_dic():
    userdic_models = UserDic.objects.all()

    for model in userdic_models:
        User_Dic.append(model.word)


# 불용어 사전 로드
def load_stopword():
    stopword_models = StopWord.objects.all()

    for model in stopword_models:
        StopWord.add(model.word)

# 학습하기
def create_model(version):
    filepath = 'News/trainfiles/'

    learnnews_models = LearnNews.objects.all()

    news_sentence = []
    news_target = []
    news_index = []
    for model in learnnews_models:
        try:
            news_sentence.append(ast.literal_eval(model.tokens))
        except:
            news_sentence.append('')

        news_target.append(str(model.target))
        news_index.append(str(model.pk))

    news_array = [[news_sentence[i], news_index[i], news_target[i]] for i in range(len(news_sentence))]
    tagged_news = [TaggedDocument(d, [c]) for d, c, t in news_array]

    cores = multiprocessing.cpu_count()
    d2v_news = doc2vec.Doc2Vec(vector_size=300,
                               # alpha=0.025,
                               # min_alpha=0.025,
                               hs=1,
                               negative=3,
                               window=5,
                               dm=0,
                               dbow_words=1,
                               min_count=5,
                               workers=cores,
                               seed=0,
                               epochs=20
                               )
    d2v_news.build_vocab(tagged_news)

    d2v_news.train(tagged_news,
                   total_examples=d2v_news.corpus_count,
                   epochs=d2v_news.epochs
                   )

    # save
    try:
        if not (os.path.isdir(filepath + str(version))):
            os.makedirs(os.path.join(filepath + str(version)))
    except OSError:
        print("Failed to create directory!!!!!")

    model_file = filepath + str(version) + '/d2v_news.model'
    d2v_news.save(model_file)
    d2v_news.wv.save_word2vec_format(model_file+'.word2vec_format')

    # 작업공간 정리
    d2v_news.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    y = pd.DataFrame(news_target, columns=['target'])
    df = pd.DataFrame(d2v_news.docvecs.vectors_docs)
    data_Set = pd.concat([df, y], axis=1)
    train_X = data_Set.drop('target', axis=1)
    train_y = data_Set['target']

    rf = RandomForestClassifier()
    model_rf = rf.fit(train_X, train_y)
    classifier_name = filepath + str(version) + '/rf_news.sav'
    pickle.dump(model_rf, open(classifier_name, 'wb'))

    LearnLog.objects.update_learnlog(version)
