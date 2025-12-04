import pandas as pd

def write_to_excel(rows, output_path):
    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
