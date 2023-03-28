import requests

# product_id = input("Enter the product ID: ")
product_id = "129901214"
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
response = requests.get(url)

print(response.status_code)