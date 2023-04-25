import requests
import json
import os
from bs4 import BeautifulSoup

product_id = input("Enter the product ID: ")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
response = requests.get(url)
first = True
has_received = False

if response.status_code != requests.codes.ok:
    print("The product does not exist")
    exit(1)

all_reviews = []
review_counter = 0

def get_element(dom, selector = None, attribute = None):
    try:
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
        pros = r.select(".review-feature__col:has(> .review-feature__title--positives) > .review-feature__item")
        pros = [p.text.strip() for p in pros]

        cons = r.select(".review-feature__col:has(> .review-feature__title--negatives) > .review-feature__item")
        cons = [c.text.strip() for c in cons]

        review = {
            "id": r["data-entry-id"].strip(),
            "author": get_element(r, ".user-post__author-name"),
            "text": get_element(r, ".user-post__text"),
            "score": get_element(r, ".user-post__score-count"),
            "likes": get_element(r, "span[id^=votes-yes]"),
            "dislikes": get_element(r, "span[id^=votes-no]"),
            "published_date": get_element(r, ".user-post__published > time:nth-child(1)", "datetime"),
            "purchased_date": get_element(r, ".user-post__published > time:nth-child(2)", "datetime"),
            "pros": pros,
            "cons": cons,
            "recommendation": get_element(r, ".user-post__author-recomendation > em")
        }

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