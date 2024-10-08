
# #%%
# import numpy as np
# import pandas as pd
# import gradio as gr
# from sentence_transformers import SentenceTransformer, util  # SBERT 사용
# import torch


# #%%
# # 1. 챗봇 응답을 처리하는 함수 정의
# def chatbot_response(query, chat_history):
#     # DB, model 불러오기
#     global search_db, product_db, chemical_db, corpus, sbert_model

#     # 쿼리와 문서의 임베딩 계산
#     query_embedding = sbert_model.encode(query, convert_to_tensor=True)  # 쿼리 임베딩
#     corpus_embeddings = sbert_model.encode(corpus, convert_to_tensor=True)  # 코퍼스 임베딩
    
#     # 코사인 유사도 계산
#     cosine_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)
    
#     # Top-1 유사한 문서 선택
#     top1_idx = torch.argmax(cosine_scores).item()  # 가장 높은 유사도 인덱스 선택
#     top1_master_num = search_db.iloc[top1_idx]["제품마스터번호"]
#     product_name = search_db.loc[search_db["제품마스터번호"] == top1_master_num, "제품명-국문"].item()  # 제품명 추출

#     # 제품 성분 조회
#     search_cols = ["물질명-영문", "predict", "confidence score"]
#     condition1 = (chemical_db["제품마스터번호"] == top1_master_num)
#     condition2 = ~chemical_db["predict"].isna()
#     condition3 = chemical_db["predict"] >= 0.5
#     compositions = chemical_db.loc[condition1 & condition2 & condition3, search_cols].reset_index(drop=True)
#     confidence_dict = {
#         "999.0": 1.0,
#         "Reliable": 0.9,
#         "Unreliable": 0.1,
#     }
#     compositions["confidence score"] = compositions["confidence score"].map(lambda x: confidence_dict[x])
#     total_tox_num = len(compositions)

#     # 제품 사용 주의사항 (KoGPT로 대체)
#     caution = product_db.loc[product_db["제품마스터번호"] == top1_master_num, "사용상 주의사항"].item()

#     # 메세지 생성
#     message1 = f'"{product_name}"에는 {total_tox_num}건의 유해물질이 포함되어 있습니다.\n'

#     if total_tox_num:
#         message2 = ""
#         for i in range(total_tox_num):
#             chemical_message = f'\t({i+1}) {compositions.loc[i, "물질명-영문"]}\n'
#             predict_message = f'\t\t유해도 {int(round(compositions.loc[i,"predict"]*10)) * "■" + int(round((1 - compositions.loc[i,"predict"]))*10) * "□"}\n'
#             confidence_message = f'\t\t신뢰도 {int(round(compositions.loc[i,"confidence score"])*10) * "■" + int(round((1 - compositions.loc[i,"predict"]))*10) * "□"}\n'
#             message2 = message2 + chemical_message + predict_message + confidence_message
#         message2 += "\n"
            
#         message3 = f"{caution}"
#     else:
#         message2, message3 = "", ""

#     response = message1 + message2 + message3

#     # 대화 기록 업데이트
#     chat_history.append((query, response))

#     return chat_history, chat_history  # chat history를 반환

# # 2. Gradio 인터페이스 정의
# with gr.Blocks() as demo:
#     # 대화 내용을 저장하는 State
#     chat_history = gr.State([])

#     # Gradio UI 컴포넌트
#     with gr.Row():
#         chatbot = gr.Chatbot(label="챗봇", height=1000)
#     with gr.Row():
#         with gr.Column(scale=6):
#             user_input = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요.", lines=1)
#         with gr.Column(scale=1):
#             send_button = gr.Button("전송")

#     # 버튼 클릭 시 chatbot_response 함수 호출
#     send_button.click(
#         chatbot_response,
#         inputs=[user_input, chat_history],
#         outputs=[chatbot, chat_history],
#         queue=True
#     )

# # 3. Gradio 인터페이스 실행
# if __name__ == "__main__":
    
#     #%%
#     search_db = pd.read_csv("./database.csv")  # 검색DB
#     chemical_db = pd.read_csv("./product_5_data.csv")  # 화학물질 정보
#     product_db = pd.read_csv("./product_4_data.csv")  # 제품정보
#     corpus = search_db["search_name"].tolist()  # 코퍼스
    
#     sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # SBERT 모델 로드

#     demo.launch()
import numpy as np
import pandas as pd
import gradio as gr
from rank_bm25 import BM25Okapi

# n-gram을 생성하는 함수 정의
def generate_ngrams(text, n):
    text = text.replace(" ", "")  # 띄어쓰기 제거 후 n-gram 생성
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return ngrams

# 1. 챗봇 응답을 처리하는 함수 정의
def chatbot_response(query, chat_history):
    # DB, model 불러오기
    global search_db, product_db, chemical_db, bm25

    # 쿼리에 n-gram 2, 3을 적용
    query_2gram = generate_ngrams(query, 2)
    query_3gram = generate_ngrams(query, 3)
    tokenized_query = query_2gram + query_3gram  # n-gram 2와 3을 합침

    # BM25로 유사도 계산
    doc_scores = bm25.get_scores(tokenized_query)  # 유사도 계산
    result = pd.DataFrame({
        'text': corpus,
        'master_num': search_db["제품마스터번호"],
        'score': doc_scores,
    })
    top1_master_num = result.iloc[result["score"].argmax(), 1]
    product_name = search_db.loc[search_db["제품마스터번호"] == top1_master_num, "제품명-국문"].item()  # 제품명 추출

    # 제품 성분 조회
    search_cols = ["물질명-영문", "predict", "confidence score"]
    condition1 = (chemical_db["제품마스터번호"] == top1_master_num)
    condition2 = ~chemical_db["predict"].isna()
    condition3 = chemical_db["predict"] >= 0.5
    compositions = chemical_db.loc[condition1 & condition2 & condition3, search_cols].reset_index(drop=True)
    confidence_dict = {
        "999.0": 1.0,
        "Reliable": 0.9,
        "Unreliable": 0.1,
    }
    compositions["confidence score"] = compositions["confidence score"].map(lambda x: confidence_dict[x])
    total_tox_num = len(compositions)

    # 제품 사용 주의사항 (KoGPT로 대체)
    caution = product_db.loc[product_db["제품마스터번호"] == top1_master_num, "사용상 주의사항"].item()

    # 메세지 생성
    message1 = f'"{product_name}"에는 {total_tox_num}건의 유해물질이 포함되어 있습니다.\n'

    if total_tox_num:
        message2 = ""
        for i in range(total_tox_num):
            chemical_message = f'\t({i+1}) {compositions.loc[i, "물질명-영문"]}\n'
            predict_message = f'\t\t유해도 {int(round(compositions.loc[i,"predict"]*10)) * "■" + int(round((1 - compositions.loc[i,"predict"]))*10) * "□"}\n'
            confidence_message = f'\t\t신뢰도 {int(round(compositions.loc[i,"confidence score"])*10) * "■" + int(round((1 - compositions.loc[i,"predict"]))*10) * "□"}\n'
            message2 = message2 + chemical_message + predict_message + confidence_message
        message2 += "\n"
            
        message3 = f"{caution}"
    else:
        message2, message3 = "", ""

    response = message1 + message2 + message3

    # 대화 기록 업데이트
    chat_history.append((query, response))

    return chat_history, chat_history  # chat history를 반환

# 2. Gradio 인터페이스 정의
with gr.Blocks() as demo:
    # 대화 내용을 저장하는 State
    chat_history = gr.State([])

    # Gradio UI 컴포넌트
    with gr.Row():
        # 윈도우 창 크기에 맞게 대화창의 높이와 너비 설정
        chatbot = gr.Chatbot(label="챗봇", height=1000)  # height=600으로 기본 높이 설정, 필요시 조정 가능
    with gr.Row():
        with gr.Column(scale=6):
            user_input = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요.", lines=1)
        with gr.Column(scale=1):
            send_button = gr.Button("전송")


    # 버튼 클릭 시 chatbot_response 함수 호출
    send_button.click(
        chatbot_response,   # 호출할 함수
        inputs=[user_input, chat_history],  # 입력값
        outputs=[chatbot, chat_history],    # 출력값
        queue=True
    )

# 3. Gradio 인터페이스 실행
if __name__ == "__main__":
    search_db = pd.read_csv("./database.csv")  # 검색DB
    chemical_db = pd.read_csv("./product_5_data.csv")  # 화학물질 정보
    product_db = pd.read_csv("./product_4_data.csv")  # 제품정보
    corpus = search_db["search_name"].tolist()  # 코퍼스

    # n-gram 2, 3을 각 문서에 대해 적용
    tokenized_corpus = []
    for doc in corpus:
        ngrams_2 = generate_ngrams(doc, 2)
        ngrams_3 = generate_ngrams(doc, 3)
        tokenized_corpus.append(ngrams_2 + ngrams_3)  # n-gram 2와 3을 합침

    bm25 = BM25Okapi(tokenized_corpus)

    demo.launch()


# # 3. Gradio 인터페이스 실행
# if __name__ == "__main__":
#     search_db = pd.read_csv("./search_image_db.csv") ## 검색DB
#     chemical_db = pd.read_csv("./product_5_data.csv") ##화학물질 정보
#     product_db = pd.read_csv("./product_4_data.csv") ## 제품정보
#     corpus = search_db["search_image_name"].tolist() ##
#     tokenized_corpus = [doc.split(" ") for doc in corpus] # 띄어쓰기 기준 구분
#     bm25 = BM25Okapi(tokenized_corpus)

#     demo.launch()


# #%%


#%%