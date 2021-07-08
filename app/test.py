from pathlib import Path
path = Path(__file__).parent
file_path = (path / "./data/test.csv").resolve()
print(file_path)
print(path)


# import pandas as pd
# confirmed = pd.read_csv((path / '../data/time_series_covid19_confirmed_global.csv').resolve())