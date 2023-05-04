import pytest
import boto3
from moto import mock_s3
from src.xml_to_parquet import convert_xml_to_parquet


@pytest.fixture
def s3_client():
    with mock_s3():
        yield boto3.client("s3")


@pytest.mark.parametrize(
    "input_s3_path, output_s3_path, expected_value",
    [
        (
            "s3://my-bucket/my-folder/input.xml",
            "s3://my-bucket/my-folder/output.parquet",
            "value1",
        ),
        (
            "s3://my-bucket/other-folder/input.xml",
            "s3://my-bucket/other-folder/output.parquet",
            "value2",
        ),
    ],
)
def test_convert_xml_to_parquet(
    s3_client, input_s3_path, output_s3_path, expected_value
):
    # Set up mock S3 bucket and upload test XML file
    s3_client.create_bucket(Bucket="my-bucket")
    s3_client.upload_file(
        "test/test_input.xml", "my-bucket", "my-folder/input.xml"
    )

    # Convert XML to Parquet using the convert_xml_to_parquet function
    convert_xml_to_parquet(input_s3_path, output_s3_path)

    # Check that the Parquet file was written to S3 and contains the expected value
    obj = s3_client.get_object(
        Bucket="my-bucket", Key="other-folder/output.parquet"
    )
    parquet_bytes = obj["Body"].read()
    # Add any necessary assertions here to check the content of the Parquet file
    # For example, if the Parquet file contains a single column named "my_column", you could do:
    # import pyarrow.parquet as pq
    # table = pq.read_table(parquet_bytes)
    # assert table.column("my_column").to_pylist() == [expected_value]
