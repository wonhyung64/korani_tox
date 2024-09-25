import gradio as gr

# 1. 챗봇 응답을 처리하는 함수 정의
def chatbot_response(user_input, chat_history):
    # 여기서 간단한 챗봇 로직을 정의하거나, GPT 같은 모델을 사용할 수 있습니다.
    # 예시: 간단한 인사말 응답
    if "안녕" in user_input:
        response = "안녕하세요! 무엇을 도와드릴까요?"
    else:
        response = "죄송합니다, 잘 이해하지 못했어요."

    # 대화 기록 업데이트
    chat_history.append(("User", user_input))
    chat_history.append(("Bot", response))

    return chat_history, chat_history  # chat history를 반환

# 2. Gradio 인터페이스 정의
with gr.Blocks() as demo:
    # 대화 내용을 저장하는 State
    chat_history = gr.State([])

    # Gradio UI 컴포넌트
    with gr.Row():
        chatbot = gr.Chatbot(label="챗봇")
    with gr.Row():
        with gr.Column(scale=6):
            user_input = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요.")
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
    demo.launch()
