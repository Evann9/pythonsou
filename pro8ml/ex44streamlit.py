# 작업 결과를 간단하게 웹으로 출력하기
# Python Streamlit 라이브러리 사용
# pip install streamlit

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = [
    '광고성 메일을 확인하세요',
    '회의 일정 변경 공지',
    '무료 쿠폰을 지금 사용하세요',
    '중요한 계약 내용을 확인해주세요',
    '지금 할인 중입니다',
    '오늘 업무 일정 다시 확인해 주세요',
    '지금 바로 확인하세요',
    '사내 공지입니다',
    '긴급 이벤트에 당첨되셨습니다!',
    '회의록을 메일로 보내주세요',
    '지금 할인 쿠폰 드립니다',
    '업무 보고서를 작성해 주세요',
    '당신의 계정이 해킹되었습니다',
    '사내 행사 공지입니다',
    '신상품을 최대 50% 할인합니다',
    '다음 주 회의 일정을 공유드립니다',
    '무료 선물 받기 클릭!',
    '결재 요청이 도착했습니다',
    '지금 쿠폰을 받으세요',
    '담당자와 연락 바랍니다',
    '대출 상담 가능합니다 최저 금리',
    '내일 오전 10시 팀 미팅',
    '축하합니다! 경품 이벤트 당첨',
    '프로젝트 마감 기한 연장 안내',
    '비트코인 급등 정보 지금 확인',
    '신규 입사자 오리엔테이션 일정',
    '해외 결제 승인 완료 본인 아니면 클릭',
    '주간 업무 보고서 제출 바랍니다',
    '로또 번호 무료 추출 서비스',
    '연말 정산 서류 안내 드립니다',
    '성인 전용 익명 채팅방 초대',
    '시스템 점검 공지사항',
    '부업으로 월 500만원 보장',
    '출장 신청서 승인 부탁드립니다',
    '투자 수익률 300% 보장',
    '건강검진 대상자 명단 확인',
    '현금 사은품 증정 이벤트',
    '인사고과 면담 일정 안내',
    '지금 바로 입금 확인하세요',
    '사내 동호회 모집 공고',
    '최저가 쇼핑몰 바로가기',
    '회의실 예약 현황 공유',
    '무료 체험단 모집 중',
    '보안 프로그램 업데이트 권장',
    '단기 고수익 알바 모집',
    '복지 포인트 사용 안내',
    '상금 1억원의 주인공은?',
    '신규 프로젝트 기획안 검토',
    '카지노 무료 칩 증정',
    '퇴직금 정산 내역서입니다'
]

labels = [
    'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
    'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
    'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
    'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
    'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham'
]

vect = CountVectorizer()
x = vect.fit_transform(texts)

model = MultinomialNB()
model.fit(x, labels)

# streamlit UI-----------
import streamlit as st
st.title('스팸 메일 분류기')

user_input = st.text_input('이메일 내용을 입력하세요')

if user_input:
    x_new = vect.transform([user_input])
    pred = model.predict(x_new)[0]
    prob = model.predict_proba(x_new)[0]
    
    spam_prob = prob[model.classes_.tolist().index('spam')]
    ham_prob = prob[model.classes_.tolist().index('ham')]

    st.write(f'예측 결과 : {pred} ')
    st.progress(spam_prob if pred == 'spam' else ham_prob)
    st.write(f'확률 결과 → spam : {spam_prob*100:.2f} / ham : {ham_prob*100:.2f}')
