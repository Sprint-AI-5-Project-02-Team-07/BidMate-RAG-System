import os
import json
import pandas as pd
from langchain_core.documents import Document

def load_rfp_documents(config: dict):
    csv_path = config['path']['csv_file']
    json_folder = config['path']['files_folder']
    
    print(f"[Loader] 메타데이터 로드: {csv_path}")
    df = pd.read_csv(csv_path)
    
    all_docs = []
    success_count = 0
    fallback_count = 0

    print(f"[Loader] JSON 데이터 로딩 시작... (대상 폴더: {json_folder})")

    for _, row in df.iterrows():
        # 1. 파일명 매핑
        # CSV의 '파일명' (예: 사업계획서.hwp) -> JSON 파일명 (예: 사업계획서_parsed.json)
        original_name = str(row['파일명'])
        base_name = os.path.splitext(original_name)[0] # 확장자 제거
        
        # Upstage 결과 파일명 패턴에 맞춰 수정하세요 (예: _parsed.json)
        json_file_name = f"{base_name}_parsed.json" 
        json_path = os.path.join(json_folder, json_file_name)
        
        # 공통 메타데이터 (CSV에서 가져옴)
        base_metadata = {
            "source": original_name,
            "project_name": row.get('사업명', "Unknown"),
            "organization": row.get('발주 기관', "Unknown"),
            "budget": row.get('사업 금액', 0),
            "deadline": row.get('입찰 참여 마감일', "Unknown")
        }

        # 2. JSON 파일 로드
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    pages_data = json.load(f) # JSON은 리스트 형태 [ {page:1, content:...}, ... ]
                
                # JSON 내의 각 페이지를 Document 객체로 변환
                for page_item in pages_data:
                    # Upstage JSON 구조: {"content": "...", "page": 1, ...}
                    content = page_item.get('content', '')
                    page_num = page_item.get('page', 0)
                    
                    if not content.strip():
                        continue
                        
                    # 페이지별 메타데이터 추가
                    page_metadata = base_metadata.copy()
                    page_metadata['page'] = page_num
                    
                    # Document 생성
                    doc = Document(page_content=content, metadata=page_metadata)
                    all_docs.append(doc)
                
                success_count += 1
                
            except Exception as e:
                print(f"[Error] JSON 파싱 실패 ({json_file_name}): {e}")
                # 실패 시 Fallback으로 이동
        else:
            # JSON 파일이 없는 경우 (이름 불일치 등)
            # print(f"[Warning] JSON 파일 없음: {json_file_name}")
            pass

        # 3. Fallback: JSON이 없으면 CSV 텍스트 사용
        # (방금 로드한 문서 리스트에 해당 소스 파일이 없으면 실패로 간주)
        is_loaded = any(d.metadata.get("source") == original_name for d in all_docs[-50:])
        
        if not is_loaded:
            content = str(row.get('텍스트', ''))
            if content.strip():
                all_docs.append(Document(page_content=content, metadata=base_metadata))
                fallback_count += 1

    print(f"[Loader] 완료: Upstage JSON 로드 {success_count}건, CSV 대체 {fallback_count}건")
    return all_docs