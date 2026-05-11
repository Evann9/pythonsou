적용 방법

이 압축파일은 전체 프로젝트가 아니라 '수정/추가 파일 묶음'입니다.

project1_web 폴더 기준으로 같은 경로에 덮어쓰기/추가하세요.

포함 파일:
- app.py
- templates/main.html
- templates/battery_section.html
- static/js/main.js
- static/js/battery_section.js
- static/css/battery_section.css
- models/best_svr_model.pkl
- models/best_svr_model_params.pkl

주의:
- models 폴더가 없으면 새로 생성됩니다.
- app.py에 numpy, pandas, joblib import가 추가되었습니다.
- 실행 환경에 없다면 아래 설치가 필요합니다.
  pip install numpy pandas joblib scikit-learn

제한사항:
- 풍속: 0~5m/s
- 고도: 10~200m
- 좌표: 최대 4개
- 거리: 0보다 크고 1000m 이하
- 총회전량: 0~720deg
