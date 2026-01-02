import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_vector_db(docs, config):
    embeddings = OpenAIEmbeddings(model=config['model']['embedding'])
    db_path = config['path']['vector_db']

    # DB 구축 (Batch processing with progress bar)
    # 기존 DB가 있으면 로드, 없으면 생성
    vectorstore = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    
    from tqdm import tqdm
    
    batch_size = 100
    print(f"[Indexer] Total chunks to index: {len(docs)}")
    
    for i in tqdm(range(0, len(docs), batch_size), desc="Indexing"):
        batch = docs[i : i + batch_size]
        vectorstore.add_documents(batch)
        
    return vectorstore

def load_vector_db(config):
    embeddings = OpenAIEmbeddings(model=config['model']['embedding'])
    db_path = config['path']['vector_db']
    
    if not os.path.exists(db_path):
        return None
        
    vectorstore = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    return vectorstore