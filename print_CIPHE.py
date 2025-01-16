import pandas as pd 
import argparse
import ast
from utils.metrics.metrics import print_CIPHE_metrics, print_intrusion_scores


'''Calculates and prints CIPHE metrics after extracting a json file from sql
    with sqlite3_to_json.py.
    If an answer_sheet is provided the parser assumes that data is from
    an intrusion experiment.
    
    Example usage:
    python print_CIPHE.py --json_path "exp3_news_aa.json"
    python print_CIPHE.py --json_path "exp1_news_data.json" 
        --answer_sheet [5, 20, 27, 31, 41, 52, 68]
    
    Example json_path:
    "exp2_aa.json"
        
    Example answer_sheet for intrusion:
    [3, 12, 23, 32, 44, 58, 70] # wiki random
    [6, 16, 25, 40, 44, 57, 70] # yelp random
    [5, 20, 27, 31, 41, 52, 68] # news random
'''

def load_df(json_path):
    df = pd.read_json(json_path)
    print(df)
    return df

def process_df(df, args):
    for _, cluster_row in df.iterrows():
        if args.answer_sheet is not None:
            answer_sheet = ast.literal_eval(args.answer_sheet[0])
            answer_sheet = [str(answer) for answer in answer_sheet]
            print_intrusion_scores(cluster_row, answer_sheet)
        else:
            print_CIPHE_metrics(cluster_row)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CIPHE metrics.")
    parser.add_argument("--json_path", type=str, required=True, help="Path to the JSON file.")
    parser.add_argument("--answer_sheet", nargs='+', help="List of answer sheet IDs.")
    args = parser.parse_args()
    df = load_df(args.json_path)
    process_df(df, args)
    