# xml_to_parquet

This is a project that includes a function `convert_xml_to_parquet()` that converts an XML file stored in S3 to Parquet format and stores it back in S3. The project also includes a test suite that tests the `convert_xml_to_parquet()` function.

## Installation

To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage

To use the `convert_xml_to_parquet()` function, import it from `my_module.py`:

```python
from my_module import convert_xml_to_parquet

input_s3_path = "s3://my-bucket/input.xml"
output_s3_path = "s3://my-bucket/output.parquet"
convert_xml_to_parquet(input_s3_path, output_s3_path)
```

## To run the test suite, run:
pytest tests/

## Pre-commit

This project includes a pre-commit configuration that enforces 100% coverage and uses black, mypy, and pylama to check for coding style issues. To set up pre-commit, run:
```bash
pip install pre-commit
pre-commit install
```
After setting up pre-commit, the hooks will run automatically before you commit changes. To manually run the hooks, run:
```bash
pre-commit run --all-files
```

## Terraform

Run ```terraform init``` to initialize the Terraform configuration.
Run ```terraform plan``` to see the changes that will be made to your AWS account.
If the plan looks good, run ```terraform apply``` to create the infrastructure in your AWS account.
When you're done with the infrastructure, run ```terraform destroy``` to delete it from your AWS account.
