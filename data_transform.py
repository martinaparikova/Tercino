import pandas as pd
import datetime as dt
import column_list
import csv

delimiter = '|'
sheet = 0
skip_rows = 1


# source_file_path = 'C:/Users/marti/OneDrive - Operátor ICT, a.s/Terka/Granty MHMP žadatelé 2020-03.xlsx'
# target_file_path =  'C:/Users/marti/OneDrive - Operátor ICT, a.s/Terka/Granty MHMP žadatelé 2020-03_krasa.csv'
source_file_path = 'C:/Users/marti/Downloads/Granty MHMP žadatelé_2020-03-11.xlsx'
target_file_path = 'C:/Users/marti/Downloads/Granty MHMP žadatelé_2020-03-11.csv'
list_of_cols = column_list.zadatele_mhmp
# source_file_path = 'C:/Users/OP3282/Downloads/Granty MHMP žadatelé xlsx.xlsx'
# target_file_path = 'C:/Users/OP3282/Downloads/Granty MHMP žadatelé xlsx.csv'



# list_of_cols = column_list.zadatele_mhmp

# source_file_path = 'C:/Users/OP3282/Documents/projekty/Airbnb/airbnb_data_2020-01-22.xlsx'
# target_file_path = 'C:/Users/OP3282/Documents/projekty/Airbnb/airbnb_data_2020-01-22_listings.csv'
# list_of_cols = column_list.airbnb_listings


# source_file_path = 'C:/Users/OP3282/Documents/projekty/Airbnb/airbnb_data_2019-12-17.xlsx'
# target_file_path = 'C:/Users/OP3282/Documents/projekty/Airbnb/airbnb_data_2019-12-17_upraveno.csv'

# source_file_path = 'C:/Users/OP3282/Documents/projekty/Verejne zakazky/prosinec2019-Analyticky_report-14.01.2020.xls'
# target_file_path = 'C:/Users/OP3282/Documents/projekty/Verejne zakazky/prosinec2019-Analyticky_report-14.01.2020_upraveno.csv'

# source_file_path = 'C:/Users/OP3282/Documents/projekty/Verejne zakazky/TEST_SPATNY_DATA.xlsx'
# target_file_path = 'C:/Users/OP3282/Documents/projekty/Verejne zakazky/TEST_SPATNY_DATA_upraveno.csv'

date_cols = []
money_cols = []
column_names = []
drop_rows = []
str_cols = []




# sheet = 0 is sheet else sheet

for col in list_of_cols:
    column_names.append(col[1])
    if col[3] == "money":
        money_cols.append(col[1])
    if col[3] == "date":
        date_cols.append(col[1])
    if col[3] == "str":
        str_cols.append(col[1])

file_data = pd.read_excel(source_file_path, skiprows=skip_rows, names=column_names, sheet_name=sheet,
                          encoding='utf-8', keep_default_na=False)

# cleaning data
for column in file_data:
    # return numeric type for selected columns
    if column in money_cols:
        for rowindex, row in file_data.iterrows():
            pd.to_numeric(file_data.loc[rowindex, column])
    # delete rows with invalid date in selected columns (specific for airbnb data)
    if column in date_cols:
        for rowindex, row in file_data.iterrows():
            if str(file_data.loc[rowindex, column]).startswith('6') \
                    or file_data.loc[rowindex, column] > dt.datetime.now():
                drop_rows.append(rowindex)
        file_data = file_data.drop(index=file_data.index[drop_rows])
    if column in str_cols:
        for rowindex, row in file_data.iterrows():
            file_data.loc[rowindex, column] = str(file_data.loc[rowindex, column].strip())
            # remove line endings inside fields
            file_data.loc[rowindex, column] = str(file_data.loc[rowindex, column]).replace('\n', '')

# create csv
if list_of_cols in (column_list.granty_mhmp, column_list.zadatele_mhmp):
    file_data.to_csv(target_file_path, sep=delimiter, header=column_names, index=False,
                     quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
else:
    file_data.to_csv(target_file_path, sep=delimiter, index=False)

# print copy command for PostgreSQL
print(F'COPY verejne_zakazny_raw '
      F'FROM \'{target_file_path}\' DELIMITER \'|\' CSV HEADER;')
