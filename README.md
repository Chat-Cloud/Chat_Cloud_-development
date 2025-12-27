Chat_cloud 로고
<img width="445" height="445" alt="Gemini_Generated_Image_hvto3ghvto3ghvto" src="https://github.com/user-attachments/assets/9ad6d225-6b9f-4ee8-82f9-9720cc96dea9" />

# Chat Insight Dashboard (KakaoTalk + Service Chat Analytics)

메신저 채팅 데이터를 분석하여 **감정 흐름·대화 패턴·상호작용 특징**을 한눈에 확인할 수 있는 **인사이트 대시보드**입니다.  
카카오톡 대화 로그(외부 데이터)부터 서비스 내 채팅(실시간 데이터)까지 동일한 분석 파이프라인으로 연결해 **총 13개 시각화**를 제공합니다.

---

## 1) 프로젝트 개요

- **목표**: 비정형 채팅 로그를 구조화하고, 감정/패턴/상호작용 지표를 정량화하여 사용자가 원문을 다시 읽지 않아도 대화 흐름을 파악할 수 있도록 지원
- **데이터 규모**: 카카오톡 대화 로그 약 **10,000건**
- **결과물**: **13개 시각화**로 구성된 Streamlit 대시보드

---

## 2) 핵심 기능 (Features)

- 카카오톡 대화 로그 업로드/수집 → 파싱/정제 → 데이터 저장
- 감정 분석(HuggingFace) 기반 분위기(톤) 추적
- 빈도/리듬 분석: 날짜·요일·시간대 활동량, 대화 세션/끊김, 응답 속도 등
- 키워드/주제 요약: OKT 기반 키워드 추출 및 시각화
- 기간/참여자/채팅방 필터링으로 탐색 가능한 대시보드 제공

---

## 3) 시스템 아키텍처 (SQL / NoSQL 분리)

본 프로젝트는 **두 가지 데이터 유입 경로**를 지원하며, 최종적으로 동일한 인사이트 파이프라인을 탑니다.

### A. 실시간 서비스 채팅 경로 (RDB 중심)
Client(Streamlit) → Chat API → **MySQL(RDB, ERD 기반)** `chat` 테이블 적재  
→ 집계/분석 서비스 → MySQL 지표 테이블 저장 → Dashboard 시각화

### B. 카카오톡 외부 로그 경로 (NoSQL → RDB)
Kakao Export(txt/zip) → Parser/정제 → **MongoDB(NoSQL, JSON Raw Zone)** 원본 보존  
→ 스키마 매핑/정규화 → **MySQL(RDB, ERD 기반)** 적재  
→ 집계/분석 서비스 → MySQL 지표 테이블 저장 → Dashboard 시각화

- **MongoDB(NoSQL)**: 포맷이 유동적인 원본/중간 결과를 유연하게 보존(재처리/예외 케이스 대응)
- **MySQL(RDB)**: ERD 기반 정규화 데이터와 반복 조회되는 집계 지표를 안정적으로 관리(빠른 조회/유지보수)

---

## 4) 시각화 지표 — 한 줄 설명

1. **메시지 수 추이(일/주)**: 기간에 따른 대화량 변화를 보여줍니다.  
2. **시간대별 대화 **: 하루 중 대화가 집중되는 시간대를 한눈에 확인합니다.  
3. **참여자별 메시지 비중**: 누가 대화를 주도하는지 비율로 보여줍니다.  
4. **감정 분포(긍정/중립/부정)**: 전체 대화 분위기를 5단계 감정 비율로 요약합니다.  
5. **감정 추이(시간 변화)**: 특정 시점 이후 분위기(톤) 변화 흐름을 추적합니다.  
6. **시간대별 감정 변화**: 시간대에 따라 감정 톤이 어떻게 달라지는지 비교합니다.  
7. **호감/애정 표현 패턴**: 관계 신호(칭찬/애정 표현 등)의 등장 빈도를 집계합니다.  
8. **키워드 Top N / 워드클라우드**: 자주 등장한 핵심 단어로 대화 주제를 요약합니다.

> 위 지표 구성은 프로젝트 구현에 따라 약간 달라질 수 있습니다.

---

## 5) 기술 스택 (Tech Stack)

- **Frontend / App**: Streamlit
- **Data / ML**: Python, HuggingFace(감정 분석), KoNLPy OKT(키워드)
- **DB**: MySQL(RDB), MongoDB(NoSQL)
- **Visualization**: Matplotlib / Seaborn (프로젝트 구성에 따라)

---

## 6) 실행 방법 (Quick Start)

### 6.1 환경 준비
- Python 3.10+ 권장
- MySQL, MongoDB 실행 환경 필요

## 7) Main Page
<img width="1836" height="1497" alt="스크린샷 2025-12-24 152420" src="https://github.com/user-attachments/assets/42eecb0c-95a1-4008-b535-8baeaef3279a" />

## 8) 대시보드에 나오는 대화 인사이트(시각화)
<img width="1915" height="1084" alt="스크린샷 2025-12-02 012111" src="https://github.com/user-attachments/assets/1fd680fb-366a-4ceb-a61a-ab5136bbe975" />
<img width="1913" height="1078" alt="스크린샷 2025-12-02 012145" src="https://github.com/user-attachments/assets/c3f2b546-e9ba-4f3e-a4d9-566e8e0341b6" />
<img width="1900" height="975" alt="스크린샷 2025-12-02 012216" src="https://github.com/user-attachments/assets/29c9a912-ce16-4205-bacd-98b556ac8da1" />
<img width="1915" height="1385" alt="스크린샷 2025-12-02 012235" src="https://github.com/user-attachments/assets/fa176d59-4178-4336-a85a-b0009668bfc6" />
<img width="1903" height="1063" alt="스크린샷 2025-12-02 012332" src="https://github.com/user-attachments/assets/ae763b3e-72c1-423e-9ea7-e2727a86559e" />

