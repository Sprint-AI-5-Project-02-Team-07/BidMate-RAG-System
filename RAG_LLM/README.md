# 🤖 AI 사업 공고 분석 챗봇 (AI Business Notice Analysis Chatbot)

이 프로젝트는 RAG (Retrieval-Augmented Generation) 기술을 활용하여 AI 관련 사업 공고를 분석하고 질의응답을 제공하는 챗봇 애플리케이션입니다.  
사용자의 질문을 분석하여 적절한 문서를 검색하고, LLM을 통해 답변을 생성합니다.

## ✨ 주요 기능 (Key Features)

- **하이브리드 검색 (Hybrid Retrieval)**: 키워드 검색(BM25)과 벡터 검색(Vector Similarity)을 결합하여 정확도 높은 문서를 찾습니다.
- **질문 분해 (Query Decomposition)**: 복잡한 질문을 여러 개의 하위 질문(Sub-queries)으로 나누어 검색하여 답변 품질을 높입니다.
- **자동 필터링 (Auto-Filtering)**: 사용자 질문에서 '기관명', '금액' 등의 조건을 자동으로 추출하여 검색 범위를 좁힙니다.
- **대화 맥락 유지 (Session Context)**: 이전 대화의 필터 조건(예: 특정 지역, 예산 범위)을 기억하여 자연스러운 대화가 가능합니다.
- **Streamlit UI**: 직관적인 웹 인터페이스를 통해 쉽게 챗봇과 대화할 수 있습니다.

## 🛠️ 설치 및 설정 (Installation)

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

`.env` 파일에 필요한 API 키(OpenAI 등)가 설정되어 있어야 합니다.

## 🚀 실행 방법 (Usage)

### 1. 웹 인터페이스 (Streamlit) 실행
가장 권장하는 방법입니다. 웹 브라우저에서 챗봇과 대화할 수 있습니다.

```bash
streamlit run app.py
```

### 2. CLI (Command Line Interface) 실행
터미널에서 직접 질문하고 답변을 받을 수 있습니다.

```bash
# 기본 사용 (텍스트 질문)
python main.py --query "경기도 AI 지원 사업 알려줘"

# 벡터 DB 구축 (처음 실행 시 또는 데이터 변경 시)
python main.py --build

# 필터 적용 예시
python main.py --query "예산 1억 이상 사업" --min_amount 100000000
```

## 📂 프로젝트 구조 (Structure)

- `app.py`: Streamlit 메인 애플리케이션 파일
- `main.py`: CLI 진입점 및 벡터 DB 빌드 스크립트
- `src/`: 핵심 로직 모듈
    - `retrieval.py`: 검색 로직 (Hybrid Retrieval)
    - `generation.py`: LLM 답변 생성
    - `decomposition.py`: 질문 분해 로직
    - `query_extractor.py`: 필터 추출 로직
    - `session_manager.py`: 대화 세션 및 컨텍스트 관리
    - `loader.py`: 데이터 로드 및 전처리
    - `evaluation.py`: RAG 성능 평가 (Ragas 활용)
