import nbformat
import shutil
import os

# Define paths
original_path = "/Users/vamsi_mbmax/Library/CloudStorage/OneDrive-Personal/01_vam_PROJECTS/LEARNING/proj_AI/dev_proj_AI/practise_ai_crewai_learn/notebooks/crewai_sql_agent.ipynb"
new_path = os.path.join(os.path.dirname(original_path), "practise_TBD.ipynb")

# First create a copy of the original notebook
shutil.copy2(original_path, new_path)

# Read the new notebook
with open(new_path, 'r', encoding='utf-8') as f:
    notebook = nbformat.read(f, as_version=4)

# Clear all code cells while preserving other cell types
for cell in notebook.cells:
    if cell.cell_type == 'code':
        cell.source = ''
        cell.outputs = []
        cell.execution_count = None

# Write the modified notebook back to file
with open(new_path, 'w', encoding='utf-8') as f:
    nbformat.write(notebook, f)

print(f"Created cleared notebook at: {new_path}")
