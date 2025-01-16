import sqlite3
import pandas as pd
from collections import defaultdict
import ast

CLUSTER_SIZE = 10
SURVEY_ID = 1
HAS_ORIGINAL_LABEL = True
HAS_STYLE = True
DB_NAME = 'db_exp2_fixed_inverse.sqlite3'
SAVE_NAME = "exp2_aa.json"
IDS_NEWS_EXP1 = [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                 16, 17, 18, 19, 20, 22, 23, 24, 25, 27, 28, 30, 31, 34]
IDS_YELP_EXP1 = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33]
IDS_WIKI_EXP1 = [2, 3, 5, 6, 7, 8, 9, 10, 13, 14, 15,
                 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
IDS_NEWS_EXP3 = [33, 35, 36, 37, 38, 39, 41, 42, 44, 45,
                 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
IDS_YELP_EXP3 = [31, 32, 33, 36, 37, 38, 39, 40, 41, 42,
                 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
IDS_WIKI_EXP3 = [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15,
                 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
IDS_EXP2 = [2, 3, 4, 5, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32, 35, 36, 37, 39, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 71, 72, 73, 74, 75, 78, 80, 81, 83, 85, 88, 89, 90, 92, 93, 94, 95, 96, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 122, 123, 124,
            125, 126, 128, 130, 131, 132, 133, 135, 136, 137, 140, 142, 143, 144, 145, 146, 148, 149, 150, 152, 154, 155, 157, 158, 160, 161, 163, 164, 165, 167, 168, 169, 170, 172, 174, 175, 176, 178, 179, 181, 182, 183, 184, 185, 187, 188, 189, 190, 191, 193, 194, 195, 196, 197, 199, 200, 202, 203, 205, 206, 207, 208, 209, 212, 213, 214, 215, 218, 219, 220, 221, 222, 224, 225, 228, 229, 232, 233]


USER_IDS = IDS_EXP2

LABEL_MAPPING = pd.read_json("original_label_link.json")


def calculate_model_score(response):
    converted_response = ast.literal_eval(response)    
    return len(converted_response) / CLUSTER_SIZE


def convert_to_original_label(cluster_id, original_label=None):
    mapping = LABEL_MAPPING
    if HAS_ORIGINAL_LABEL:
        django_eval_set_label = original_label
        original_label = mapping.label[
            mapping.evaluation_set_label == django_eval_set_label
        ].unique()[0]
        return original_label
    else:
        return cluster_id


def generate_likert_query():
    if HAS_ORIGINAL_LABEL:
        if HAS_STYLE:
            query = """
                        SELECT cluster.id, cluster.original_cluster, likert.inclusion, likert.naming, likert.opinion, likert.emotion, likert.interest, likert.style
                        FROM survey_likertscalequestion likert
                        JOIN survey_page p ON likert.page_id = p.id
                        JOIN survey_cluster cluster ON p.cluster_id = cluster.id
                        WHERE p.user_id = ?
                    """
        else:    
            query = """
                        SELECT cluster.id, cluster.original_cluster, likert.inclusion, likert.naming, likert.opinion, likert.emotion, likert.interest
                        FROM survey_likertscalequestion likert
                        JOIN survey_page p ON likert.page_id = p.id
                        JOIN survey_cluster cluster ON p.cluster_id = cluster.id
                        WHERE p.user_id = ?
                    """
    else:
        if HAS_STYLE:
            query = """
                        SELECT cluster.id, likert.inclusion, likert.naming, likert.opinion, likert.emotion, likert.interest, likert.style
                        FROM survey_likertscalequestion likert
                        JOIN survey_page p ON likert.page_id = p.id
                        JOIN survey_cluster cluster ON p.cluster_id = cluster.id
                        WHERE p.user_id = ?
                    """
        else:
            query = """
                        SELECT cluster.id, likert.inclusion, likert.naming, likert.opinion, likert.emotion, likert.interest
                        FROM survey_likertscalequestion likert
                        JOIN survey_page p ON likert.page_id = p.id
                        JOIN survey_cluster cluster ON p.cluster_id = cluster.id
                        WHERE p.user_id = ?
                    """
    return query

def generate_naming_query():
    if HAS_ORIGINAL_LABEL:
        query = """
            SELECT cluster.id, cluster.original_cluster, name.text_answer
            FROM survey_namequestion name
            JOIN survey_page p ON name.page_id = p.id
            JOIN survey_cluster cluster ON p.cluster_id = cluster.id
            WHERE p.user_id = ?
        """
    else:
        query = """
            SELECT cluster.id, name.text_answer
            FROM survey_namequestion name
            JOIN survey_page p ON name.page_id = p.id
            JOIN survey_cluster cluster ON p.cluster_id = cluster.id
            WHERE p.user_id = ?
        """
    return query

def generate_article_query():
    if HAS_ORIGINAL_LABEL:
        query = """
            SELECT cluster.id, cluster.original_cluster, article.selected, article.id
            FROM survey_articlequestion article
            JOIN survey_page p ON article.page_id = p.id
            JOIN survey_cluster cluster ON p.cluster_id = cluster.id
            WHERE p.user_id = ?
        """
    else:
        query = """
            SELECT cluster.id, article.selected, article.id
            FROM survey_articlequestion article
            JOIN survey_page p ON article.page_id = p.id
            JOIN survey_cluster cluster ON p.cluster_id = cluster.id
            WHERE p.user_id = ?
        """
    return query


def get_all_articles(cluster_id):
    '''Note: If the import_data command has been used to add articles 
        to the survey, the cluster_id from the db is enough for 
        identifying all articles for that survey.
    '''
    all_articles = [i for i in range((cluster_id-1)*10+1, cluster_id*10+1)]
    return all_articles


def process_name_answers(cluster_name_answers, answer):
    if HAS_ORIGINAL_LABEL:
        (cluster_id, original_label, text_answer) = answer  
        cluster_id = convert_to_original_label(cluster_id, original_label)
    else:
        (cluster_id, text_answer) = answer
    cluster_name_answers[cluster_id].append(text_answer)
    
def process_article_answers(cluster_article_answers, cluster_article_scores, answer):
    if HAS_ORIGINAL_LABEL:
        (cluster_id, original_label, selected, article_id) = answer
        all_articles = get_all_articles(cluster_id)
        cluster_id = convert_to_original_label(cluster_id, original_label)
    else:
        (cluster_id, selected, article_id) = answer
        all_articles = get_all_articles(cluster_id)        
    cluster_article_answers[cluster_id]["selected"].append(selected)
    cluster_article_answers[cluster_id]["all_articles"].append(all_articles)
    score = calculate_model_score(selected)
    cluster_article_scores[cluster_id].append(score)


def process_likert_answers(cluster_likert_answers, answer):
    if HAS_ORIGINAL_LABEL:
        if HAS_STYLE:
            (cluster_id, original_label, inclusion, naming, opinion, emotion, interest, style) = answer
        else:
            (cluster_id, original_label, inclusion, naming, opinion, emotion, interest) = answer
        cluster_id = convert_to_original_label(cluster_id, original_label)
    else:
        if HAS_STYLE:
            (cluster_id, inclusion, naming, opinion, emotion, interest, style) = answer
        else:
            (cluster_id, inclusion, naming, opinion, emotion, interest) = answer
        cluster_id = convert_to_original_label(cluster_id, original_label=None)
            
    cluster_likert_answers[cluster_id]["inclusion"].append(inclusion)
    cluster_likert_answers[cluster_id]["naming"].append(naming)
    cluster_likert_answers[cluster_id]["opinion"].append(opinion)
    cluster_likert_answers[cluster_id]["emotion"].append(emotion)
    cluster_likert_answers[cluster_id]["interest"].append(interest)
    if HAS_STYLE:
        cluster_likert_answers[cluster_id]["style"].append(style)

def fetch_cluster_data(user_ids):
    cluster_likert_answers = defaultdict(lambda: defaultdict(list))
    cluster_article_answers = defaultdict(lambda: defaultdict(list))
    cluster_article_scores = defaultdict(list)
    cluster_name_answers = defaultdict(list)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for user_id in user_ids:
        print(user_id)
        query = generate_naming_query()
        cursor.execute(query, (user_id,))
        name_answers = cursor.fetchall()
        for answer in name_answers:
            process_name_answers(cluster_name_answers, answer)

        query = generate_article_query()
        cursor.execute(query, (user_id,))
        article_answers = cursor.fetchall()
        for answer in article_answers:
            process_article_answers(cluster_article_answers, cluster_article_scores, answer)

        query = generate_likert_query()
        cursor.execute(query, (user_id,))
        likert_answers = cursor.fetchall()
        for answer in likert_answers:
            process_likert_answers(cluster_likert_answers, answer)
                
    conn.close()

    data = []
    all_cluster_ids = (
        set(cluster_likert_answers.keys())
        | set(cluster_article_answers.keys())
        | set(cluster_article_scores.keys())
        | set(cluster_name_answers.keys())
    )

    for cluster_id in all_cluster_ids:
        row = {
            "cluster_id": cluster_id,
            "likert_answers": cluster_likert_answers.get(cluster_id, {}),
            "article_answers": cluster_article_answers.get(cluster_id, {}),
            "article_scores": cluster_article_scores.get(cluster_id, []),
            "name_answers": cluster_name_answers.get(cluster_id, []),
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_json(SAVE_NAME, index=False)

user_ids = USER_IDS
fetch_cluster_data(user_ids)
