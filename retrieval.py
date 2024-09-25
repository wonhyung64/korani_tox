#%%
import pandas as pd
from rank_bm25 import BM25Okapi

df7 = pd.read_csv("./product_7_data.csv")
product_names_df = pd.read_csv("./augmented_product_name.csv")
df7["search_name"] = product_names_df.apply(lambda x: f"{x['org_name']} | {x['aug_name']}", axis=1)

corpus = df7["search_name"].tolist()
tokenized_corpus = [doc.split(" ") for doc in corpus] # 띄어쓰기 기준 구분
bm25 = BM25Okapi(tokenized_corpus)

query = "퍼실 듀오캡스 컬러 가 안전한지 확인해줘"
tokenized_query = query.split(" ") 
doc_scores = bm25.get_scores(tokenized_query)
result = pd.DataFrame({
    'text': corpus,
    'score': doc_scores
})
result.sort_values(['score'], ascending=False)


#%%
df4 = pd.read_csv("./product_4_data.csv")
df5 = pd.read_csv("./product_5_data.csv")
df7["제품군명"].unique()
