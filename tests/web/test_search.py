from src.web.search import WebSearch


search = WebSearch(max_results=5)

results = search.search(
    "latest Formula 1 news"
)

for result in results:
    print("\nTitle:", result["title"])
    print("URL:", result["url"])
    print("Snippet:", result["snippet"])