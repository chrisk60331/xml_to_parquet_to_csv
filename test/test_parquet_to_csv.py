import pytest
import boto3
from moto import mock_s3
from io import StringIO
from my_code import S3ParquetToCsvConverter


@pytest.fixture()
def s3_input_file():
    return 's3://my-bucket/my-input-file.parquet'


@pytest.fixture()
def s3_output_file():
    return 's3://my-bucket/my-output-file.csv'


@pytest.fixture
def s3_bucket():
    mock = mock_s3()
    mock.start()
    s3 = boto3.resource('s3', region_name='us-east-1')
    bucket = s3.Bucket('my-bucket')
    bucket.create()

    yield bucket

    bucket.objects.all().delete()
    bucket.delete()
    mock.stop()


@pytest.fixture()
def mocked_parquet_data():
    import pandas as pd
    from pyarrow import Table, schema
    df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
    arrow_table = pa.Table.from_pandas(df)
    pq_writer = pq.ParquetWriter('/tmp/input.parquet', schema=arrow_table.schema)
    pq_writer.write_table(arrow_table)
    pq_writer.close()

    with open('/tmp/input.parquet', 'rb') as f:
        return f.read()


def test_convert(s3_input_file, s3_output_file, s3_bucket, mocked_parquet_data):
    # upload Parquet data to S3
    s3_bucket.Object(s3_input_file).put(Body=mocked_parquet_data)

    converter = S3ParquetToCsvConverter(s3_input_file=s3_input_file, s3_output_file=s3_output_file)
    converter.convert()

    # download CSV data from S3
    csv_data = s3_bucket.Object(s3_output_file).get()["Body"].read().decode('utf-8')

    # check that CSV data matches expected output
    expected_output = 'A,B\n1,a\n2,b\n3,c\n'
    assert csv_data == expected_output
