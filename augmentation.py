import openai
from  assets.cred.chatgpt import OPENAICRED

def chat(sample, cred):
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=cred,
    )
    if sample is None:
        raise ValueError

    prompt = f"""\
    주어진 지시에 대한 적절한 응답을 생성해주세요. 이러한 작업 지침은 ChatGPT 모델에 주어지며, ChatGPT 모델이 지침을 완료하는지 평가합니다.

    요구 사항은 다음과 같습니다:
    2. 결과물 이외의 텍스트는 생성 금지.

    주어진 지시: 다음 제품명의 최소 의미 단위로 구분하여 공백을 삽입해주세요.: "{sample}"
    """
    
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
