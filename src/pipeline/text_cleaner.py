import json
import re
from pathlib import Path
from typing import Dict, List

# =========================
# 설정
# =========================
MIN_TEXT_LEN = 50      # 너무 짧은 텍스트 제거 (기존 200 -> 50 완화, 필요시 조정)
DOT_RATIO_TH = 0.35    # 점선 비율 임계치

# =========================
# 유틸
# =========================
def remove_decorative_lines(text: str) -> str:
    """점선/장식 위주 라인 제거"""
    lines = []
    for line in text.splitlines():
        l = line.strip()

        # 점선/장식만 있는 줄 제거
        if not l:
            continue
        if re.fullmatch(r"[·\.\-\s]+", l):
            continue

        lines.append(line)

    return "\n".join(lines).strip()


def is_toc_chunk(text: str) -> bool:
    """목차(TOC) 휴리스틱 판별"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return True

    # 명시적 목차 키워드
    if any("목 차" in l or "목차" in l for l in lines[:3]):
        return True

    dot_lines = sum(1 for l in lines if "·" in l)
    digit_lines = sum(1 for l in lines if any(c.isdigit() for c in l))
    long_text_lines = sum(1 for l in lines if len(l) >= 25 and "·" not in l)

    # 점선/숫자 위주 + 실제 문장 거의 없음
    if dot_lines / len(lines) > DOT_RATIO_TH and long_text_lines < 3:
        return True
    if digit_lines / len(lines) > 0.7 and long_text_lines < 3:
        return True

    return False


def is_meaningful(text: str) -> bool:
    """의미 있는 텍스트인지 판단"""
    if len(text) < MIN_TEXT_LEN:
        return False

    # 조사/서술어 기반 간단 체크 (너무 엄격하면 중요 데이터 날아감, 완화)
    # keywords = ["한다", "함", "한다.", "기준", "대상", "방법", "제출", "평가", "수행"]
    # if not any(k in text for k in keywords):
    #     return False

    return True


# =========================
# 정제 파이프라인
# =========================
def clean_chunk(chunk: Dict) -> Dict | None:
    # Upstage Result Structure adaptation
    # Input might be {"content": "...", "metadata": ...}
    # Output should be standard map
    
    raw_text = chunk.get("content") or chunk.get("text", "")
    raw_text = raw_text.strip()
    
    if not raw_text:
        return None

    # 1) 장식 제거
    text = remove_decorative_lines(raw_text)

    # 2) TOC 제거
    if is_toc_chunk(text):
        return None

    # 3) 의미 없는 chunk 제거
    if not is_meaningful(text):
        return None

    # 통과 (Update content)
    chunk["content"] = text
    # Remove text key if exists to standardize on 'content'
    if "text" in chunk:
        del chunk["text"]
        
    return chunk


def process_file(in_path: Path, out_path: Path):
    kept = 0
    removed = 0
    
    # Input is JSON List (from Upstage Parser)
    # Output is JSONL (for Loader)
    
    try:
        with in_path.open("r", encoding="utf-8") as f:
            data = json.load(f) # List of dicts
    except Exception as e:
        print(f"Error reading {in_path}: {e}")
        return

    with out_path.open("w", encoding="utf-8") as fout:
        for item in data:
            cleaned = clean_chunk(item)
            if cleaned is None:
                removed += 1
                continue

            fout.write(json.dumps(cleaned, ensure_ascii=False) + "\n")
            kept += 1

    print(f"✅ {in_path.name}: kept={kept}, removed={removed} -> {out_path.name}")


def run_text_cleaning(input_dir: str, output_dir: str):
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(in_dir.glob("*.json")) # parsed_json outputs .json
    print(f"[Cleaner] Found {len(files)} JSON files in {in_dir}")

    for f in files:
        # parsed.json -> clean.jsonl
        out_name = f.stem.replace("_parsed", "_clean") + ".jsonl"
        out_path = out_dir / out_name
        
        process_file(f, out_path)
