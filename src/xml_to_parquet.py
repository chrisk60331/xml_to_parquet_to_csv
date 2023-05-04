from typing import Optional

from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame


def convert_xml_to_parquet(
    input_s3_path: str,
    output_s3_path: str,
    job_name: Optional[str] = "xml-to-parquet",
    group_size: Optional[str] = "1048576",
) -> None:
    """
    Converts an S3 XML file to Parquet format and writes it back to S3.

    Args:
        input_s3_path: S3 path of the input XML file.
        output_s3_path: S3 path of the output Parquet file.
        job_name: The name of the Glue PySpark job. Defaults to 'xml-to-parquet'.
        group_size: The size of each group when reading files from S3. Defaults to '1048576'.
    """
    # Create a Spark session and Glue context
    spark = SparkSession.builder.appName(job_name).getOrCreate()
    glue_context = GlueContext(SparkContext.getOrCreate())

    # Load the XML file from S3 into a DynamicFrame
    xml_dynamic_frame = glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={
            "paths": [input_s3_path],
            "recurse": True,
            "groupFiles": "inPartition",
            "groupSize": group_size,
        },
        format="xml",
        transformation_ctx="xml_dynamic_frame",
    )

    # Convert the DynamicFrame to a DataFrame and perform any necessary transformations
    xml_data_frame = xml_dynamic_frame.toDF()
    # Perform any necessary transformations on the data frame here

    # Write the DataFrame to Parquet format and save it back to S3
    parquet_data_frame = xml_data_frame.write.mode("overwrite").parquet(
        output_s3_path
    )

    # Convert the Parquet data frame back to a DynamicFrame and write it to S3
    parquet_dynamic_frame = DynamicFrame.fromDF(
        parquet_data_frame, glue_context, "parquet_dynamic_frame"
    )
    glue_context.write_dynamic_frame.from_options(
        frame=parquet_dynamic_frame,
        connection_type="s3",
        connection_options={"path": output_s3_path},
        format="parquet",
        transformation_ctx="parquet_dynamic_frame",
    )
