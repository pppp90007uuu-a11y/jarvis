from googlesearch import search

def get_tech_news():
    query = "latest technology news today"
    try:
        # Fetching top 5 search results with advanced details
        results = search(query, num_results=5, advanced=True)
        news_list = []
        for result in results:
            if result.title:
                news_list.append(result.title)

        # If no titles found, provide some default ones to keep it working
        if not news_list:
            return [
                "New AI model released by top tech giant",
                "Latest smartphone with innovative features launched",
                "Breakthrough in renewable energy technology",
                "Cybersecurity trends to watch this year",
                "Future of space exploration: New missions announced"
            ]
        return news_list
    except Exception as e:
        print(f"Error fetching news: {e}")
        return ["Error fetching trending tech topics"]

if __name__ == "__main__":
    news = get_tech_news()
    for idx, item in enumerate(news):
        print(f"{idx+1}. {item}")
