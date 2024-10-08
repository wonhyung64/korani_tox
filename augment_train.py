#%%
import pandas as pd
from tqdm import tqdm
from augmentation import chat
from assets.cred.chatgpt import OPENAICRED


# %%
df = pd.read_csv("./train_2warnings.csv")
product_names = df["제품명-국문"].tolist()

prompt = f"""\
주어진 지시에 대한 적절한 응답을 생성해주세요. 이러한 작업 지침은 ChatGPT 모델에 주어지며, ChatGPT 모델이 지침을 완료하는지 평가합니다.

요구 사항은 다음과 같습니다:
1. 결과물 이외의 텍스트는 생성 금지.

주어진 지시: 다음 제품명의 최소 의미 단위로 구분하여 공백을 삽입해주세요.: 
"""

aug_names = []
for i, prod in tqdm(enumerate(product_names)):
    response = chat(prod, OPENAICRED)
    response_message = response.choices[0].message.content
    aug_names.append(response_message)

#%%
columns = ["org_name", "aug_name"]
augmented_df = pd.DataFrame(columns=columns, data=zip(product_names, aug_names))
augmented_df.to_csv("augmented_product_name.csv")
