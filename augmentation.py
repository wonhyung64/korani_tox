import openai
from  assets.cred.chatgpt import OPENAICRED

def chat(sample, cred, prompt):
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=cred,
    )
    if sample is None:
        raise ValueError

    prompt = prompt + sample
    
    messages = []
    messages.extend([
        {"role": "system", "content": "You're a helpful assistant that transforms given product name into different one while maintaining the same meaning."},
        {"role": "user", "content": prompt}])

    # @retry(
    #     wait=wait_random_exponential(min=1, max=60), ### API 호출 사이의 시간 간격은 지수분포로부터 샘플링
    #     stop=stop_after_attempt(100)) ### 오류가 발생하더라도 100번을 시도
    def completions_with_backoff(client, **kwargs):
        return client.chat.completions.create(**kwargs)

    response = completions_with_backoff(
        client=client, model="gpt-4o-mini", messages=messages)
    
    return response


if __name__ == "__main__":

    sample = "테크 산소크린_에이"
    response = chat(sample, OPENAICRED)
    response_message = response.choices[0].message.content
    print(response_message)
