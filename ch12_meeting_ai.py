import streamlit as st
from openai import OpenAI

# 텍스트 줄바꿈 함수 정의
def format_transcription(text):
	sentences = text.replace('. ', '.  \n')
	return sentences

# 텍스트 요약 함수 정의
def summarize_text(input_text: str, client):
	initial_prompt = """
	다음 회의록을 요약해줘.
	- 마크다운으로 요약해줘.
	"""
	prompt = f"{initial_prompt}\n\n{input_text}"
	response = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[{"role": "user", "content": prompt}],
	)
	return response.choices[0].message.content

def main():
	# 페이지 설정 및 사이드바 구현
	st.set_page_config(layout="wide")
	st.title("회의록 요약 프로그램")
	st.caption("회의를 녹음한 음성 파일을 업로드하면 원본 텍스트와 요약본을 출력합니다.")
	with st.sidebar:
		openai_api_key = st.text_input(
			"OpenAI API Key",
			type="password",
		)
		st.markdown(
			"[OpenAI API Key 받기](https://platform.openai.com/account/api-keys)"
		)
	if "messages" not in st.session_state:
		st.session_state.messages = []
	# 파일 업로드 위젯 생성
	mp3_file = st.file_uploader("mp3 파일을 업로드하세요.", type=["mp3"])
	if st.button("음성-텍스트 변환"):
		if not openai_api_key:
			st.info("계속하려면 OpenAI API Key를 추가하세요.")
			st.stop()
		if not mp3_file:
			st.warning("mp3 파일을 업로드하세요.")
			st.stop()
		client = OpenAI(api_key=openai_api_key)
		with st.spinner("텍스트 추출 및 요약 중..."):
			# 음성-텍스트 변환을 위한 API 요청 및 응답 처리
			transcription = client.audio.transcriptions.create(
				model="whisper-1",
				file=mp3_file,
				response_format="text",
			)
			# 두 개의 탭 생성 및 결과 출력
			tab1, tab2 = st.tabs(["원본 텍스트", "요약본"])
			with tab1:
				st.write(format_transcription(transcription))
			with tab2:
				# 텍스트 요약 함수 호출 및 결과 출력
				st.write(summarize_text(transcription, client))

if __name__ == "__main__":
	main()
