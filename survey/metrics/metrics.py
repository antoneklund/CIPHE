import numpy as np
import ast
from nltk.metrics import agreement as agree
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


CLUSTER_SIZE = 10


def print_CIPHE_metrics(cluster):
    CP = calculate_CIPHE_precision(cluster)
    IA, (A_inc, A_seg, A_name, L_inc, L_name) = (
        calculate_CIPHE_interpretation_agreement(cluster)
    )
    print("----------------------------------------")
    print(f"Cluster {cluster.cluster_id}")
    print(cluster.name_answers)
    print(f"Cluster Precision: {CP}")
    print(f"Interpretation Agreement: {IA}")
    print(f"A_inc: {A_inc}")
    print(f"A_seg: {A_seg}")
    print(f"A_name: {A_name}")
    print(f"L_inc: {L_inc}")
    print(f"L_name: {L_name}")


# Calculate CP
def calculate_CIPHE_precision(cluster):
    scores = cluster.article_scores
    CP = 1 - np.mean(scores)
    return CP


# Calculate IA
def calculate_CIPHE_interpretation_agreement(cluster):
    A_inc = calculate_agreement_inclusion(cluster)
    A_seg, _, _ = calculate_agreement_segmentation(cluster)
    A_name = calculate_agreement_naming(cluster)
    L_inc = calculate_likert_inclusion(cluster)
    L_name = calculate_likert_naming(cluster)
    IA = (A_inc + A_name + A_seg + L_inc + L_name) / 5
    return IA, (A_inc, A_seg, A_name, L_inc, L_name)


# Calculate A_inc
def calculate_agreement_inclusion(cluster):
    selected = cluster.article_answers["selected"]
    all_articles_in_cluster = cluster.article_answers["all_articles"]
    responses = []
    zipped_responses = zip(selected, all_articles_in_cluster)
    for i, (selected_articles, all_articles) in enumerate(zipped_responses):
        selected_processed = ast.literal_eval(selected_articles)
        selected_processed = [int(s) for s in selected_processed]
        selected_processed = convert_to_bool_list(selected_processed, all_articles)

        for j, a in enumerate(selected_processed):
            responses.append(
                (str(i), str(j), a)
            )  # Tuple of (user_id, article_id, bool(response))
    A_inc = agree.AnnotationTask(responses).avg_Ao()
    return A_inc


# Calculate A_seg
def calculate_agreement_segmentation(cluster):
    selected = cluster.article_answers["selected"]
    all_articles_in_cluster = cluster.article_answers["all_articles"]

    segmentation_responses = []
    unique_segmentations = []
    segmentation_counts = {}  # Dictionary to store counts of unique segmentations

    for i, selected_articles in enumerate(selected):  # (articles, uf)
        selected_processed = ast.literal_eval(selected_articles)
        selected_processed = convert_to_bool_list(
            selected_processed, all_articles_in_cluster
        )
        if (
            selected_articles not in unique_segmentations
        ):  # Checking if segmentation is already in the list
            unique_segmentations.append(selected_articles)
            segmentation_counts[selected_articles] = 0

        segmentation_counts[selected_articles] += 1
        segmentation_responses.append((str(i), 0, selected_articles))
    agreement_segmentations = agree.AnnotationTask(data=segmentation_responses)
    u = len(unique_segmentations)
    n = len(selected)
    min_n_segmentations = 1
    A_seg = 1 - ((u - min_n_segmentations) / (n - min_n_segmentations))
    return A_seg, segmentation_counts, agreement_segmentations.avg_Ao()


# Calculate A_name
def calculate_agreement_naming(cluster, normalization_const=0.6):
    names = cluster.name_answers
    embeddings = inference_sentence_t5(names)
    cos_sim, min_sim, max_sim = avg_cosine_sim(embeddings)
    norm_sim = (cos_sim - normalization_const) / (max_sim - normalization_const)
    return norm_sim


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
        if answer:  # Check if there's an answer
            values.append(likert_scale_map.get(answer, 0))

    if values:
        return np.mean(values)
    return None  # If there are no values to average


def calculate_model_score(cluster):
    scores = []
    article_responses = cluster.article_answers.to_list()

    responses = article_responses  # zip(article_responses, uf_responses)
    for response in responses:  # , uf
        # if uf == "none":
        #     converted_response = []
        # else:
        converted_response = ast.literal_eval(response)
        scores.append(len(converted_response) / CLUSTER_SIZE)
    return np.mean(scores), scores


def convert_to_bool_list(selected, all_articles):
    selected_processed = []
    for a in all_articles:
        if a in selected:
            selected_processed.append(True)
        else:
            selected_processed.append(False)
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
    np.fill_diagonal(
        similarities, np.nan
    )  # Remove the diagonal entries (distances between identical vectors)
    min_sim = np.nanmin(similarities)
    max_sim = np.nanmax(similarities)
    average_cosine_similarity = np.nanmean(similarities)
    return average_cosine_similarity, min_sim, max_sim


# def calculate_agreement(articles_df, uf_df, cluster_id):
#     all_articles = ALL_ARTICLE_IDS[cluster_id - 1]

#     article_answers = articles_df.selected.to_list()

#     responses = []
#     segmentation_responses = []
#     unique_segmentations = []
#     segmentation_counts = {}  # Dictionary to store counts of unique segmentations

#     for i, selected_articles in enumerate(article_answers):  # (articles, uf)
#         selected_processed = ast.literal_eval(selected_articles)
#         selected_processed = convert_to_bool_list(selected_processed, all_articles)

#         for j, a in enumerate(selected_processed):
#             responses.append(
#                 (str(i), str(j), a)
#             )  # Tuple of (user_id, article_id, bool(response))

#         if (
#             selected_articles not in unique_segmentations
#         ):  # Checking if segmentation is already in the list
#             unique_segmentations.append(selected_articles)
#             segmentation_counts[selected_articles] = 0

#         segmentation_counts[selected_articles] += 1
#         segmentation_responses.append((str(i), 0, selected_articles))

#     agreement = agree.AnnotationTask(data=responses)
#     segmentation_agree = agree.AnnotationTask(data=segmentation_responses)
#     nr_unique = len(unique_segmentations)

#     return agreement, segmentation_agree, nr_unique, segmentation_counts
