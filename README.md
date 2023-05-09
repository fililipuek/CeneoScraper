# CeneoScraper

:)

### CSS selectors of all necessary components

|Component|Variable/Dictionary key|Data type|Selector|
| :- | :- | :- | :- |
|review|`r/review`|`Tag, dictionary`|`div.js_product-review`|
|review ID|`id`|`string`|`["data-entry-id"]`|
|review author|`author`|`string`|`span.user-post__author-name`|
|whether the author recommends the product|`recommendation`|`bool`|`span.user-post__author-recomendation > em`|
|score expressed in star count|`score`|`float`|`span.user-post__score-count`|
|review content|`text`|`string`|`div.user-post__text`|
|list of product advantages|`pros`|`string`|`div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item`|
|list of product disadvantages|`cons`|`string`|`div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item`|
|how many users thought the review was helpful|`likes`|`int`|`button.vote-yes["data-total-vote"]`, `button.vote-yes > span`, `span[id^=votes-yes]`|
|how many users thought the review was unhelpful|`dislikes`|`int`|`button.vote-no["data-total-vote"]`, `button.vote-no > span`, `span[id^=votes-no]`|
|publishing date|`published_date`|`string`|`span.user-post__published > time:nth-child(1) ["datetime"]`|
|purchase date|`purchased_date`|`string`|`span.user-post__published > time:nth-child(2) ["datetime"]`|

## Python libraries used in the project

- requests
- BeautifulSoup
- json
- os
- numpy
- translate
- matplotlib