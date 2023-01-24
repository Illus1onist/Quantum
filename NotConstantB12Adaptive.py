import pandas


d = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}

pd.DataFrame(data=d, index=[0, 1, 2, 3])