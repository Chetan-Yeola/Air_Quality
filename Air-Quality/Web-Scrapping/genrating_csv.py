import os
import sys

import pandas as pd



class CSV_Generation:

    def parse_html_for_years(self, years_range: list) -> pd.DataFrame:
        final_data_df = pd.DataFrame()
        for year in years_range:
            for month in range(1, 13):
                file_html = open(f'data/html_data/{year}/{month}.html', 'rb')
                plain_text = file_html.read()

                final_data = []
                soup = BeautifulSoup(plain_text, "lxml")
                for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
                    for tr in table:
                        temp_data = []
                        for td in tr:
                            text = td.get_text()
                            temp_data.append(text)
                        final_data.append(temp_data)

                # skip header rows and 2 footer rows
                monthly_data_df = pd.DataFrame(final_data[1:len(final_data) - 2], columns=final_data[0])
                # drop unnecessary columns
                col_idx_to_drop = [0, 4, 10, 11, 12, 13, 14]
                for col in reversed(col_idx_to_drop):
                    monthly_data_df.drop(monthly_data_df.columns[col], axis=1, inplace=True)
                final_data_df = final_data_df.append(monthly_data_df)
        final_data_df.reset_index(inplace=True, drop=True)
        return final_data_df

    def combine_features_with_target(self, features: pd.DataFrame, yearly_dict: dict) -> pd.DataFrame:
        pm_2_5_data = []
        for year in yearly_dict.keys():
            for idx, rows in enumerate(yearly_dict[year]):
                pm_2_5_data.append(yearly_dict[year][idx])
        features['PM_2_5'] = pm_2_5_data
        return features