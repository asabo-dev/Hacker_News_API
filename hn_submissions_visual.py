import requests
import plotly.express as px
from operator import itemgetter

# Make an API call and check the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process overall results.
submission_ids = r.json()
submission_dicts = []

for submission_id in submission_ids[:15]:
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict.get('title', 'N/A'),
        'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict.get('descendants', 0),
    }
    submission_dicts.append(submission_dict)

# Sort the list of dictionaries by the number of comments.
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Process repository information.
submission_links, comments, hover_texts = [], [], []
for submission_dict in submission_dicts:
    title = submission_dict['title']
    hn_link = submission_dict['hn_link']
    submission_link = f"<a href='{hn_link}'>{title}</a>"
    submission_links.append(submission_link)

    comments.append(submission_dict['comments'])

    hover_text = f"{title}<br />{submission_dict['comments']} comments"
    hover_texts.append(hover_text)

# Make visualization.
title = 'Most-Discussed Articles on Hacker News'
labels = {'x': 'Submission', 'y': 'Comments'}
fig = px.bar(x=submission_links, y=comments, title=title, labels=labels, hover_data={'text': hover_texts})

fig.update_layout(title_font_size=28, xaxis_title_font_size=20, yaxis_title_font_size=20)
fig.update_traces(marker_color='violet', marker_opacity=0.6)

fig.show()

# Detailed Explanation of the Code: https://chatgpt.com/share/67868734-04c8-8007-8ed7-cc42e0b8989f