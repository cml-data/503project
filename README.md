# 503project
Final project

------------------

-- Notes from Haleigh:

Potential scrapers:
1. stocks (S&P 100? all 500? could also consider nasdaq if want more techy stuff. or we could compare nasdaq to s&p. see how it changes with news?)
2. currency rates (compare to news stories? compare to foreign etfs in nyse? (if so, will also have to pull those from first scraper bc I don't think there are many, if any, foreign etfs in S&P or nasdaq))
3. crypto (compare to stocks? also see how it changes with news?)
4. news: use perigon api?
- https://www.goperigon.com/products/demo
- They have a "sentiment" column which gives numeric values for positive, neutral, and negative for whatever is pulled. Can pull top stories where it counts how many unique sources are talking about that story. And/or could pull individual articles (like top 100 per week or so). This option allows us to see the keywords in those articles and how much each one is weighed. Also has same sentiment column as the top stories option and a categories option that shows us what topics the article was talking about. It also has a "entities" column that lists keywords and how many times each of those keywords were named in the article. We could use some of the things we've learned in ML to synthesize this info.
- Problem: only 14d free trial. We would have to each make an account after 14 days of each other to keep scraping the data until our final project is due
- I got this to work though!! I didn't push to github though since it had my api key in it and I forgot how to hide that
5. news: use 538?
- They have poll results added each day
- The APIs I found were all out of date
- I tried using web2db to pull the data from the tables on the main page, but it didn't work (I verified it worked with other websites that had tables, so it must be the issue that Jed was talking about from slide 7 of week 7)
6. other ideas??
