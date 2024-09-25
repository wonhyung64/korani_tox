import pandas as pd
from rank_bm25 import BM25Okapi

path = "./product_4_data.csv"
df4 = pd.read_csv("./product_4_data.csv")
df5 = pd.read_csv("./product_5_data.csv")
df7 = pd.read_csv("./product_7_data.csv")
df4["기타내용"].unique()
df7["제품명-영문"].unique()


corpus = df7["제품명-국문"].tolist()
tokenized_corpus = [doc.split(" ") for doc in corpus] # 띄어쓰기 기준 구분
bm25 = BM25Okapi(tokenized_corpus)

query = "파워산소표백 이라는 제품이 안전한지 확인해줘"
tokenized_query = query.split(" ") 
doc_scores = bm25.get_scores(tokenized_query)
result = pd.DataFrame({
    'text': corpus,
    'score': doc_scores
})
result.sort_values(['score'], ascending=False)
