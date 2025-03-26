import sys
import os
import pandas as pd
from ragatouille import RAGPretrainedModel
from langchain_community.document_loaders import PyPDFLoader

from pathlib import Path
# Add the parent directory of SCRIPTS_MAINTENANCE to the Python path
script_dir = Path(__file__).resolve().parent
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))
from MODULES import paths

loader = PyPDFLoader(file_path=paths.nantum_doc_pdf_path)
pages = loader.load_and_split()
full_document = ""
for page in pages:
    full_document += page.page_content

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
path = RAG.index(
    collection=[full_document],
    index_name="nantum_doc",
    split_documents=True,
    max_document_length=512,
)

print(f"Updated Index at {path}")

