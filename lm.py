#%%
# 설치 참고
# https://github.com/SKTBrain/KoBERT/issues/102
# %%
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel

tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

def get_kobert_model(model_path, vocab_file, ctx="cpu"):
    bertmodel = BertModel.from_pretrained(model_path)
    device = torch.device(ctx)
    bertmodel.to(device)
    bertmodel.eval()
    vocab_b_obj = nlp.vocab.BERTVocab.from_sentencepiece(vocab_file,
                                                         padding_token='[PAD]')
    return bertmodel, vocab_b_obj



from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm, tqdm_notebook
import pandas as pd

import numpy as np
np.bool = np.bool_
import gluonnlp as nlp

# %%
device = torch.device("cuda:0") 


bertmodel, vocab = get_kobert_model('skt/kobert-base-v1',tokenizer.vocab_file)
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower = False)

# %% data sample
columns = ["query", "label"]
{
    "인체에 무해한 세탁세제 추천해줘": "제품추천",
    "유전독성 물질이 적은 세탁세제": "성분확인",
}

