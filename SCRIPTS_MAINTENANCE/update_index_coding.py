import sys
import os
import pandas as pd
from ragatouille import RAGPretrainedModel

from pathlib import Path
# Add the parent directory of SCRIPTS_MAINTENANCE to the Python path
script_dir = Path(__file__).resolve().parent
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))
from MODULES import paths

# Read the csv file
df = pd.read_csv(paths.CODE_REFERENCE_EXAMPLE_PATH + 'coding.csv', usecols=['query'])
RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
path = RAG.index(
    collection=list(df['query'].to_list()),
    index_name="coding_examples",
)
print(f"Updated Index at {path}")

