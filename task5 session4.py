#Your corpus​
#Rebuild corpus.jsonl from Posts.xml as one function — or build the same shape from a dataset of your own — with a 20-question evaluation set.​
import pandas as pd
from bs4 import BeautifulSoup
def to_text(html):
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
def build_corpus(path, min_score=1, min_chars=200, max_chars=8000):
    posts = pd.read_xml(path, parser="etree")
    questions = posts[posts["PostTypeId"] == 1]
    answers = posts[posts["PostTypeId"] == 2]
    both = questions.merge(answers[["Id", "Body", "Score"]],
                           left_on="AcceptedAnswerId", right_on="Id",
                           suffixes=("_q", "_a"))
    text = ("Question: " + both["Title"] + "\n" + both["Body_q"].map(to_text)
            + "\nAnswer: " + both["Body_a"].map(to_text))
    keep = (both["Score_a"] >= min_score) & text.str.len().between(min_chars, max_chars)
    records = pd.DataFrame({
        "id": "ai-se-" + both["Id_q"].astype(str),
        "title": both["Title"],
        "text": text,
        "tags": both["Tags"].str.strip("|").str.split("|"),
        "score": both["Score_a"],
        "created": pd.to_datetime(both["CreationDate"]).dt.strftime("%Y-%m-%d"),
        "url": "https://ai.stackexchange.com/q/" + both["Id_q"].astype(str),
    })
    return records[keep].drop_duplicates(subset="text")
rebuilt = build_corpus("Posts.xml")
rebuilt.to_json("corpus.jsonl", orient="records", lines=True, force_ascii=False)
eval_set = rebuilt.sample(20, random_state=42)[["id", "title", "url"]]
eval_set.to_json("eval_set.jsonl", orient="records", lines=True)
print(len(rebuilt), "documents,", len(eval_set), "questions")
print(list(rebuilt.columns))