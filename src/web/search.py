from ddgs import DDGS


class WebSearch:

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def search(self, query: str) -> list[dict]:

        results = DDGS().text(
            query,
            max_results=self.max_results,
        )

        return [
            {
                "title": result.get("title"),
                "url": result.get("href"),
                "snippet": result.get("body"),
            }
            for result in results
        ]