import requests
import json
import os
from bs4 import BeautifulSoup

product_id = input("Enter the product ID: ")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
response = requests.get(url)
first = True

if response.status_code != requests.codes.ok:
    print("The product does not exist")
    exit(1)

all_reviews = []
review_counter = 0

def get_one(dom, sel):
    return dom.select_one(sel)

def get_stripped_one_checked(dom, sel):
    el = get_one(dom, sel)
    return el.text.strip() if el else None

def get_stripped_one(dom, sel):
    return get_one(dom, sel).text.strip()

while url:
    if not first:
        response = requests.get(url)
    else:
        first = False
    
    page_dom = BeautifulSoup(response.text, "html.parser")
    reviews = page_dom.select(".js_product-review")

    if len(reviews) == 0:
        print("There are no reviews for this product")
        exit(1)

    for r in reviews:
        published_date = get_one(r, ".user-post__published > time:nth-child(1)")["datetime"].strip()
        purchased_date = get_one(r, ".user-post__published > time:nth-child(2)")

        pros = r.select(".review-feature__col:has(> .review-feature__title--positives) > .review-feature__item")
        pros = [p.text.strip() for p in pros]

        cons = r.select(".review-feature__col:has(> .review-feature__title--negatives) > .review-feature__item")
        cons = [c.text.strip() for c in cons]

        recommendation = get_stripped_one_checked(r, ".user-post__author-recomendation > em")

        review = {
            "id": r["data-entry-id"].strip(),
            "author": get_stripped_one(r, ".user-post__author-name"),
            "text": get_stripped_one(r, ".user-post__text"),
            "score": get_stripped_one(r, ".user-post__score-count"),
            "likes": get_stripped_one(r, "span[id^=votes-yes]"),
            "dislikes": get_stripped_one(r, "span[id^=votes-no]"),
            "published_date": published_date,
            "purchased_date": purchased_date["datetime"].strip() if purchased_date else None,
            "pros": pros,
            "cons": cons,
            "recommendation": recommendation
        }

        all_reviews.append(review)

        review_counter += 1
        print(f"Found {review_counter} reviews so far...             \r", end="")

    next_page = page_dom.select_one(".pagination__next")
    url = f"https://ceneo.pl/{next_page['href'].strip()}" if next_page else None

if not os.path.exists("reviews"):
    os.mkdir("reviews")

with open(f"./reviews/{product_id}.json", "w") as file:
    json.dump(all_reviews, file, indent=4, ensure_ascii=False)

print(f"Found {len(all_reviews)} reviews and saved them as ./reviews/{product_id}.json")