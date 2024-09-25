#%%
import pandas as pd
from tqdm import tqdm
from augmentation import chat
from assets.cred.chatgpt import OPENAICRED


# %%
df7 = pd.read_csv("./product_7_data.csv")
product_names = df7["제품명-국문"].tolist()
aug_names = []

for i, prod in tqdm(enumerate(product_names)):
    response = chat(prod, OPENAICRED)
    response_message = response.choices[0].message.content
    aug_names.append(response_message)

#%%
columns = ["org_name", "aug_name"]
augmented_df = pd.DataFrame(columns=columns, data=zip(product_names, aug_names))
augmented_df.to_csv("augmented_product_name.csv")
