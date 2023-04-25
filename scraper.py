import requests
import json
import os
from bs4 import BeautifulSoup
import numpy as np
from translate import Translator

product_id = input("Enter the product ID: ")
from_lang = "pl"
to_lang = "en"
translator = Translator(to_lang, from_lang)
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
response = requests.get(url)
first = True
has_received = False

selectors = {
    "id": [None, "data-entry-id"],
    "author": [".user-post__author-name"],
    "text": [".user-post__text"],
    "score": [".user-post__score-count"],
    "likes": ["span[id^=votes-yes]"],
    "dislikes": ["span[id^=votes-no]"],
    "published_date": [".user-post__published > time:nth-child(1)", "datetime"],
    "purchased_date": [".user-post__published > time:nth-child(2)", "datetime"],
    "pros": [".review-feature__col:has(> .review-feature__title--positives) > .review-feature__item", None, True],
    "cons": [".review-feature__col:has(> .review-feature__title--negatives) > .review-feature__item", None, True],
    "recommendation": [".user-post__author-recomendation > em"]
}

if response.status_code != requests.codes.ok:
    print("The product does not exist")
    exit(1)

all_reviews = []
review_counter = 0

def text_cleanup(text):
    return " ".join(text.replace(r"\s", " ").split())

def get_element(dom, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            tag_list = dom.select(selector)
            return ", ".join([tag.text.strip() for tag in tag_list])

        if attribute:
            if selector:
                return dom.select_one(selector)[attribute].strip()
            return dom[attribute].strip()
        
        return dom.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

while url:
    if not first:
        response = requests.get(url)
    else:
        first = False
    
    page_dom = BeautifulSoup(response.text, "html.parser")
    reviews = page_dom.select(".js_product-review")

    if len(reviews) == 0:
        if not has_received:
            print("There are no reviews for this product")
            exit(1)
        else:
            break

    has_received = True

    for r in reviews:
        review = {}

        for key, value in selectors.items():
            review[key] = get_element(r, *value)
        review["recommendation"] = True if review["recommendation"] == "Polecam" else False if review["recommendation"] == "Nie polecam" else None
        review["score"] = np.divide(*[float(score.replace(",", ".")) for score in review["score"].split("/")])
        review["likes"] = int(review["likes"])
        review["dislikes"] = int(review["dislikes"])
        review["text"] = text_cleanup(review["text"])
        review["text_en"] = translator.translate(review["text"][:min(500, len(review["text"]))])
        review["pros_en"] = translator.translate(review["pros"][:min(500, len(review["pros"]))])
        review["cons_en"] = translator.translate(review["cons"][:min(500, len(review["cons"]))])

        all_reviews.append(review)

        review_counter += 1
        print(f"Found {review_counter} reviews so far...             \r", end="")

    next_page = get_element(page_dom, "a.pagination__next", "href")
    url = f"https://ceneo.pl/{next_page}" if next_page else None

if not os.path.exists("reviews"):
    os.mkdir("reviews")

with open(f"./reviews/{product_id}.json", "w") as file:
    json.dump(all_reviews, file, indent=4, ensure_ascii=False)

print(f"Found {len(all_reviews)} reviews and saved them as ./reviews/{product_id}.json")