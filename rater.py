from rapidfuzz import process, fuzz
import numpy as np

def judge_pages(content, valid_para, threshold=50, verbose: bool = False):
    result = {}
    valid_url = []

    for url, content_data in content.items():
        for para in content_data['paragraphs']:
            if len(para.split()) < 5:
                continue

            # Get all matches for this paragraph
            matches = list(process.extract_iter(valid_para, [para], scorer=fuzz.token_set_ratio))

            # Track the best match score for this paragraph
            best_match_score = 0
            for match in matches:
                if match[1] > threshold:
                    best_match_score = max(best_match_score, match[1])

            # If a valid match is found, update the result dictionary
            if best_match_score > 0:
                result[content_data['title']] = best_match_score
                if verbose:
                    print("\n" + content_data['title'] + " : \n" + para)
                valid_url.append(url)

    matches_array = np.array(list(result.items()))
    return matches_array, valid_url

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def softmax_output(matches_array):
    scores = matches_array[:, 1].astype(float)
    softmax_scores = softmax(scores)
    output = np.column_stack((matches_array[:, 0], softmax_scores))
    return output

def print_output(output):
    for title, score in sorted(output, key=lambda x: x[1], reverse=True):
        percentage = float(score) * 100
        print(f"Title: {title}, Score: {percentage:.2f}%")
