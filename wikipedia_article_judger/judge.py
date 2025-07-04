from . import rater
from . import keywords
from . import paragraphs
import numpy as np
from . import knowledgebase as kb

def judge(para:str, threshold:int = 50, pass2: bool = False, threshold2:int = 53, visit_all_pages:bool = False) -> dict:

    empty_para = paragraphs.para_empty(para)
    invalid_para = paragraphs.validate_para(para)

    if empty_para or invalid_para:
        print("Invalid Paragraph Length. The length should be between 10 and 600 words.")
        return {"Invalid Paragraph"}
    
    cleaned_para = paragraphs.clean(para)

    keywords_in_paragraph = keywords.extract_keywords_tfidf(para)

    relevant_pages = kb.search_wikipedia_pages(keywords_in_paragraph)

    url_list = kb.extract_unique_url(relevant_pages)

    # Pass - 1 

    content = kb.fetch_content(url_list)

    matches_array, urls = rater.judge_pages(content, cleaned_para)

    if len(matches_array) == 0:
        print("No Matches Found!")
        return {"\nNo matches were found on Wikipedia\n"}

    output = rater.softmax_output(matches_array)

    rater.print_output(output)

    print()
    kb.tests(urls)

    if not pass2:
        return output
    
    # Pass - 2

    start_points = list(set(urls))
    
    first_neighbours = kb.get_hrefs_from_urls(start_points, global_= visit_all_pages)

    url_list.extend(first_neighbours)

    content = kb.fetch_content(url_list)

    matches_array, urls = rater.judge_pages(content, cleaned_para, threshold=threshold2)
    
    if len(matches_array) == 0:
        print("No Matches Found!")
        return {"\nNo matches were found on Wikipedia\n"}

    output = rater.softmax_output(matches_array)

    print("\nPass 2 Results: \n")

    rater.print_output(output)

    return output
