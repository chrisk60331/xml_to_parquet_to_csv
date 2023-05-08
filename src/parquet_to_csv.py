from typing import List
import pandas as pd
import pyarrow.parquet as pq
import boto3

class ParquetToCsvConverter:
    def __init__(self, s3_region: str, s3_bucket: str, s3_key: str, csv_file: str):
        self.s3_region = s3_region
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.csv_file = csv_file

    def convert(self):
        s3 = boto3.resource('s3', region_name=self.s3_region)
        obj = s3.Object(self.s3_bucket, self.s3_key)
        parquet = pq.read_table(obj.get()['Body'])
        dataframe = parquet.to_pandas()
        dataframe.to_csv(self.csv_file, index=False)

if __name__ == '__main__':
    region = 'your_aws_region_name'
    bucket = 'your_s3_bucket_name'
    key = 'path_to_your_parquet_file_on_s3'
    output_csv = 'path_to_output_csv_file.csv'
    converter = ParquetToCsvConverter(region, bucket, key, output_csv)
    converter.convert()
