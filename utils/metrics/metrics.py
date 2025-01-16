import numpy as np
import pandas as pd
import ast
from nltk.metrics import agreement as agree
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


CLUSTER_SIZE = 10


def print_CIPHE_metrics(cluster):
    CP = calculate_CIPHE_precision(cluster)
    IA, (A_inc, A_name, L_inc, L_name) = (
        calculate_CIPHE_interpretation_agreement(cluster)
    )
    print("----------------------------------------")
    print(f"Cluster {cluster.cluster_id}")
    print(cluster.name_answers)
    print(f"Cluster Precision: {CP}")
    print(f"Interpretation Agreement: {IA}")
    print(f"A_inc: {A_inc}")
    # print(f"Alpha: {A_alpha}")
    # print(f"A_kappa: {A_kappa}")
    # print(f"A_corr: {A_corr}")
    # print(f"A_seg: {A_seg}")
    print(f"A_name: {A_name}")
    print(f"L_inc: {L_inc}")
    print(f"L_name: {L_name}")


def print_intrusion_scores(cluster, answer_sheet):
    intr = calculate_intrusion(cluster, answer_sheet)
    print("----------------------------------------")
    print(f"Cluster {cluster.cluster_id}")
    print(cluster.name_answers)
    print(f"Intrusion: {intr}")


def calculate_intrusion(cluster, answer_sheet):
    article_answers = cluster.article_answers
    selected = article_answers["selected"]
    scores = []
    for answer in selected: 
        if answer == "[]":
            print("Empty list")
            scores.append(0)
        else:
            eval_answer = ast.literal_eval(answer)[0]
            if eval_answer in answer_sheet:
                scores.append(1)
            else:
                scores.append(0)
    return np.mean(scores)
    

# Calculate CP
def calculate_CIPHE_precision(cluster):
    article_answers = cluster.article_answers
    selected = article_answers["selected"]
    all_articles = article_answers["all_articles"]
    cluster_size = len(all_articles[0])
    scores = []
    for response in selected:
        converted_response = ast.literal_eval(response)
        scores.append(len(converted_response) / cluster_size)
    CP = 1 - np.mean(scores)
    return CP


# Calculate IA
def calculate_CIPHE_interpretation_agreement(cluster):
    A_inc = calculate_agreement_inclusion(cluster)
    # A_corr = calculate_inclusion_correlation(cluster)
    # A_seg = calculate_agreement_segmentation(cluster)
    A_name = calculate_agreement_naming(cluster)
    L_inc = calculate_likert_inclusion(cluster)
    L_name = calculate_likert_naming(cluster)
    IA = (A_inc + A_name + L_inc + L_name) / 4
    return IA, (A_inc, A_name, L_inc, L_name)


# Calculate A_inc
def calculate_agreement_inclusion(cluster):
    def create_code_mapping_dict(codes):
        mapping_dict = {}
        for i, code in enumerate(codes):
            mapping_dict[code] = i
        return mapping_dict
    
    selected = cluster.article_answers["selected"]
    all_articles_in_cluster = cluster.article_answers["all_articles"]
    codes_list = [str(article_list) for article_list in all_articles_in_cluster]
    unique_codes = set(codes_list)
    code_mapping = create_code_mapping_dict(unique_codes)
    survey_list = [code_mapping[code] for code in codes_list]
    df = pd.DataFrame({"selected": selected, "all_articles": all_articles_in_cluster, "survey": survey_list})
    A_inc_all = []
    for survey_id, _ in enumerate(unique_codes):
        df_survey = df[df.survey==survey_id]
        selected = df_survey.selected.to_list()
        all_articles_list = df_survey.all_articles.to_list()
        responses = []
        zipped_responses = zip(selected, all_articles_list) 
        for user_id, (selected_articles, all_articles) in enumerate(zipped_responses):
            selected_processed = ast.literal_eval(selected_articles)
            selected_processed = [int(s) for s in selected_processed]
            selected_processed = convert_to_bool_list(selected_processed, all_articles)

            for article_id, article_response in enumerate(selected_processed):
                responses.append((str(user_id), str((10*survey_id)+article_id), article_response))
        A_inc = agree.AnnotationTask(responses).avg_Ao()
        A_inc_all.append(A_inc)
    A_inc = np.mean(A_inc_all)
    return A_inc


# Calculate A_corr
def calculate_inclusion_correlation(cluster):
    selected = cluster.article_answers["selected"]
    all_articles_in_cluster = cluster.article_answers["all_articles"]
    responses = []
    zipped_responses = zip(selected, all_articles_in_cluster)
    for _, (selected_articles, all_articles) in enumerate(zipped_responses):
        selected_processed = ast.literal_eval(selected_articles)
        selected_processed = [int(s) for s in selected_processed]
        selected_processed = convert_to_ones_list(selected_processed, all_articles)
        responses.append(selected_processed)
    binary_matrix = np.array(responses)
    correlation_matrix = np.corrcoef(binary_matrix, rowvar=False)
    correlation_matrix = np.nan_to_num(correlation_matrix, nan=1.0)
    upper_triangle_indices = np.triu_indices_from(correlation_matrix, k=1)
    average_correlation = np.mean(correlation_matrix[upper_triangle_indices])
    print(f"Average Correlation: {average_correlation}")
    (cs, _, _) = avg_cosine_sim(binary_matrix)
    A_corr = (cs, average_correlation)
    return A_corr


# Calculate A_seg
def calculate_agreement_segmentation(cluster):
    selected = cluster.article_answers["selected"]
    all_articles_in_cluster = cluster.article_answers["all_articles"]

    segmentation_responses = []
    unique_segmentations = []
    segmentation_counts = {} 
    
    zipped_responses = zip(selected, all_articles_in_cluster) # 
    for i, (selected_articles, all_articles) in enumerate(zipped_responses):     
        selected_processed = ast.literal_eval(selected_articles)
        selected_processed = convert_to_bool_list(
            selected_processed, all_articles
        )
        if selected_articles not in unique_segmentations:
            unique_segmentations.append(selected_articles)
            segmentation_counts[selected_articles] = 0

        segmentation_counts[selected_articles] += 1
        segmentation_responses.append((str(i), 0, selected_articles))
    agreement_segmentations = agree.AnnotationTask(data=segmentation_responses)
    u = len(unique_segmentations)
    n = len(selected)
    min_n_segmentations = n_evaluation_set_from_all_articles_list(all_articles_in_cluster)
    A_seg = 1 - ((u - min_n_segmentations) / (n - min_n_segmentations))
    return A_seg, segmentation_counts, agreement_segmentations.avg_Ao()


# Calculate A_name
def calculate_agreement_naming(cluster, normalization_const=0.6):
    names = cluster.name_answers
    embeddings = inference_sentence_t5(names)
    cos_sim, min_sim, max_sim = avg_cosine_sim(embeddings)
    # norm_sim = (cos_sim - normalization_const) / (max_sim - normalization_const)
    return cos_sim


# Calculate L_inc
def calculate_likert_inclusion(cluster):
    likert_answers = cluster.likert_answers["inclusion"]
    L_inc = calculate_likert_average(likert_answers)
    return L_inc


# Calculate L_name
def calculate_likert_naming(cluster):
    likert_answers = cluster.likert_answers["naming"]
    L_name = calculate_likert_average(likert_answers)
    return L_name


def calculate_likert_average(likert_answers):
    """Calculates the average score for a list of Likert scale answers (strings)."""
    values = []
    likert_scale_map = {
        "strongly_disagree": 0.0,
        "disagree": 0.25,
        "neutral": 0.5,
        "agree": 0.75,
        "strongly_agree": 1.0,
    }

    for answer in likert_answers:
        if answer:
            values.append(likert_scale_map.get(answer, 0))
    if values:
        return np.mean(values)
    return None 


def convert_to_bool_list(selected, all_articles):
    selected_processed = []
    for a in all_articles:
        if a not in selected:
            selected_processed.append(True)
        else:
            selected_processed.append(False)
    return selected_processed

def convert_to_ones_list(selected, all_articles):
    selected_processed = []
    for a in all_articles:
        if a not in selected:
            selected_processed.append(1)
        else:
            selected_processed.append(-1)
    return selected_processed


def inference_sentence_t5(texts):
    model = SentenceTransformer("sentence-transformers/sentence-t5-base")
    device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
    model.to(device)

    embeddings = []
    for i, text in enumerate(texts):
        embedding = model.encode(text, convert_to_numpy=True)
        embeddings.append(embedding)
        # print("Done {} out of {}".format(i + 1, len(texts)))
    return embeddings


def avg_cosine_sim(vectors):
    similarities = cosine_similarity(vectors)  # NxN
    np.fill_diagonal(similarities, np.nan)
    min_sim = np.nanmin(similarities)
    max_sim = np.nanmax(similarities)
    average_cosine_similarity = np.nanmean(similarities)
    return average_cosine_similarity, min_sim, max_sim


def n_evaluation_set_from_all_articles_list(all_articles_list):
    stringified_list = [str(article_list) for article_list in all_articles_list]
    unique_article_lists = set(stringified_list)
    n_unique = len(unique_article_lists)
    return n_unique

# A_kappa = agree.AnnotationTask(responses).multi_kappa()
# A_kappa = 0
# A_alpha = agree.AnnotationTask(responses).alpha()