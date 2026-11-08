import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
너는 친절하고 전문적인 와인 소믈리에야. 사용자의 상황에 맞는 와인을 추천하는 것이 너의 역할이야.

[대화 규칙]
1. 추천에 필요한 정보는 '상황(자리/목적)', '함께할 음식', '예산', '맛 취향' 네 가지야.
2. 정보가 부족하면 바로 추천하지 말고, 빠진 정보를 한 번에 1~2개씩 자연스럽게 질문해.
3. 정보가 충분하면 와인 2~3개를 추천해. 각 와인마다 아래 형식을 지켜.
   - 와인명 (종류 / 국가·산지 / 품종)
   - 예상 가격대 (원화 기준)
   - 추천 이유: 사용자의 상황·음식·취향과 연결해서 설명
   - 페어링 팁 또는 마시는 팁 (적정 온도, 디캔팅 여부 등)
4. 와인을 처음 접하는 사용자도 이해할 수 있도록 전문 용어는 쉽게 풀어서 설명해.
5. 와인·주류·음식 페어링과 관련 없는 질문에는 정중하게 와인 상담으로 대화를 돌려.
6. 항상 한국어로 답변해.
""".strip()

OCCASIONS = ["선택 안 함", "기념일·데이트", "선물", "가족 모임", "친구 모임·홈파티", "비즈니스 자리", "혼술"]
BUDGETS = ["선택 안 함", "2만원 이하", "2~5만원", "5~10만원", "10만원 이상"]
TASTES = ["달콤한", "드라이한", "가벼운", "묵직한", "과일향", "산미 있는", "스파클링"]


def init_messages():
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def get_ai_response(messages):
    return client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        stream=True,
    )


def build_preference_message(occasion, food, budget, tastes):
    """선택한 조건을 사용자 메시지 문장으로 변환"""
    conditions = []
    if occasion != "선택 안 함":
        conditions.append(f"- 상황: {occasion}")
    if food.strip():
        conditions.append(f"- 함께할 음식: {food.strip()}")
    if budget != "선택 안 함":
        conditions.append(f"- 예산: {budget}")
    if tastes:
        conditions.append(f"- 선호하는 맛: {', '.join(tastes)}")

    if not conditions:
        return None
    return "아래 조건에 맞는 와인을 추천해줘.\n" + "\n".join(conditions)


def handle_user_message(text):
    """사용자 메시지를 저장하고 AI 응답을 스트리밍으로 출력"""
    st.session_state.messages.append({"role": "user", "content": text})
    st.chat_message("user").write(text)

    with st.chat_message("assistant"):
        try:
            response = get_ai_response(st.session_state.messages)
            response_text = st.write_stream(
                chunk.choices[0].delta.content
                for chunk in response
                if chunk.choices and chunk.choices[0].delta.content
            )
        except Exception:
            st.error("응답을 불러오는 중 문제가 발생했어요. 잠시 후 다시 시도해 주세요.")
            st.session_state.messages.pop()  # 실패한 질문은 대화 이력에서 제거
            return

    st.session_state.messages.append({"role": "assistant", "content": response_text})


if "messages" not in st.session_state:
    init_messages()

st.subheader("💬 AI 소믈리에")
st.caption("조건을 선택하거나, 채팅으로 자유롭게 상황을 알려주세요.")

# 조건 선택 기반 추천
with st.expander("🍷 조건으로 추천받기", expanded=len(st.session_state.messages) == 1):
    with st.form("preference_form"):
        col1, col2 = st.columns(2)
        occasion = col1.selectbox("상황", OCCASIONS)
        budget = col2.selectbox("예산", BUDGETS)
        food = st.text_input("함께할 음식", placeholder="예: 스테이크, 회, 치즈 플래터")
        tastes = st.multiselect("선호하는 맛", TASTES)
        submitted = st.form_submit_button("이 조건으로 추천받기")

pending_message = None
if submitted:
    pending_message = build_preference_message(occasion, food, budget, tastes)
    if pending_message is None:
        st.warning("조건을 하나 이상 선택해 주세요.")

# 대화 초기화
if len(st.session_state.messages) > 1:
    if st.button("대화 새로 시작하기"):
        init_messages()
        st.rerun()

# 기존 대화 출력
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# 첫 방문 안내 메시지
if len(st.session_state.messages) == 1 and not pending_message:
    st.chat_message("assistant").write(
        "안녕하세요, AI 소믈리에입니다 🍷\n\n"
        "어떤 자리에서, 어떤 음식과 함께 와인을 드실 예정인가요? "
        "예산이나 좋아하는 맛을 알려주시면 더 잘 맞는 와인을 추천해 드릴게요."
    )

# 사용자 입력 (조건 폼 또는 채팅)
user_input = st.chat_input("예: 다음 주 결혼기념일에 스테이크랑 마실 와인 추천해줘")
if pending_message:
    handle_user_message(pending_message)
elif user_input:
    handle_user_message(user_input)
