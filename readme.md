# xml_to_parquet_to_csv

This is a project that includes functions `convert_xml_to_parquet()` and convert_parquet_to_csv that converts an XML file stored in S3 to Parquet format and stores it back in S3, and can read the parquet writing out a csv. The project also includes a test suite that tests the `convert_xml_to_parquet()` and convert_parquet_to_csv functions.

## Installation

To install the required dependencies, run:
```bash
pip install -r requirements.txt
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

Run init to initialize the Terraform configuration.
```
terraform init
``` 
Run plan to see the changes that will be made to your AWS account.
```
terraform plan
``` 
If the plan looks good, run apply to create the infrastructure in your AWS account.
```
terraform apply
```
When you're done with the infrastructure, run destroy to delete it from your AWS account.
```terraform destroy``` 
