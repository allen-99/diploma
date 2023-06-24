import string
import warnings

import joblib
import nltk
import pandas as pd
import spacy
from django.db.models import Q
from nltk import word_tokenize
from nltk.stem.snowball import RussianStemmer
from spacy.matcher import Matcher

from manage import create_bag_of_words
from reviews.learning.learn import stop_words
from reviews.models.models import Text, Theme, Model


class Analysis:
    def __init__(
            self,
            company_id,
            model_id,
            sets_id,
            theme_id,
            add_additional
    ):
        self.company_id = company_id
        self.model_id = model_id
        self.sets_id = sets_id
        self.theme_id = theme_id
        self.add_additional = add_additional

    def lemmatize_text(self, text):
        stemmer = RussianStemmer()
        words = text.split(",")
        return [stemmer.stem(w.strip()) for w in words]

    def get_reviews(self):
        sets = [int(i) for i in self.sets_id.split(',')]
        reviews = Text.objects.filter(Q(company_id=int(self.company_id)) & Q(set__in=sets))
        return pd.DataFrame(reviews.values('text_id', 'text', 'date'))

    def preprocessing_data(self):
        warnings.filterwarnings('ignore')
        nlp = spacy.load("ru_core_news_sm")
        stemmer = RussianStemmer()

        reviews = self.get_reviews()
        reviews = reviews.drop_duplicates(subset=['text'])
        matchers = []
        if len(self.theme_id) != 0:
            matchers = self.get_themes()
            
        opinions = []
        for op in matchers:
            opinions.append({op['name']: []})
        opinions.append({"Все": []})

        for index, review in reviews.iterrows():
            sentences = nltk.tokenize.sent_tokenize(review['text'], language='russian')
            for sentence in sentences:
                doc = word_tokenize(sentence, language='russian')
                tokens = [word.lower() for word in doc if word not in string.punctuation]
                filtered_words = [stemmer.stem(w.strip()) for w in tokens if w not in stop_words]
                sent = ' '.join(filtered_words)
                match_sentence = nlp(' '.join(filtered_words))
                has_theme = False

                for i, obj in enumerate(matchers):
                    matcher = obj['matcher']
                    matches = matcher(match_sentence)
                    if len(matches):
                        has_theme = True
                        opinions[i][obj['name']].append([sent, review['date']])
                if not has_theme:
                    opinions[-1]["Все"].append([sent, review['date']])
        return opinions

    def analysis(self):
        ml_model = Model.objects.get(id=self.model_id)
        model_path = ml_model.model_data.path
        vectorizer_path = ml_model.vectorizer.path

        clf = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        vectorizer.analyzer = None
        vectorizer.analyzer = create_bag_of_words

        result = []

        opinions = self.preprocessing_data()
        for opinion in opinions:
            for theme, review in opinion.items():
                df = pd.DataFrame(review, columns=['text', 'date'])
                X_test = vectorizer.transform(df['text'])
                y_pred = clf.predict(X_test)
                df = df.assign(sa=y_pred)
                df = df.sort_values('date')
                result.append(df)

        return result

    def get_themes(self):
        nlp = spacy.load("ru_core_news_sm")
        themes = [int(i) for i in self.theme_id.split(',')]
        themes = Theme.objects.filter(theme_id__in=themes)
        themes_df = pd.DataFrame(themes.values('theme_name', 'theme_description'))
        themes_df['theme_description'] = [self.lemmatize_text(desc) for desc in themes_df['theme_description']]
        opinions_matchers = []
        for index, theme in themes_df.iterrows():
            matcher = Matcher(nlp.vocab)
            pattern_employees_opinion = [{'LEMMA': {'IN': theme['theme_description']}}]
            matcher.add(theme['theme_name'], [pattern_employees_opinion])
            opinions_matchers.append({'name': theme['theme_name'], 'matcher': matcher})
        return opinions_matchers
