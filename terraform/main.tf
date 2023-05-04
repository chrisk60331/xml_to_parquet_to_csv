# Define AWS provider
provider "aws" {
  region = "us-east-1"
}

# Create SNS topics for success and failure notifications
resource "aws_sns_topic" "transform_success" {
  name = "transform_success"
}

resource "aws_sns_topic" "transform_failure" {
  name = "transform_failure"
}

resource "aws_sns_topic" "load_success" {
  name = "load_success"
}

resource "aws_sns_topic" "load_failure" {
  name = "load_failure"
}

# Define Glue jobs
resource "aws_glue_job" "transform" {
  name          = "transform"
  command       = "glueetl"
  default_arguments = {
    "--job-bookmark-option": "job-bookmark-enable"
  }
  role_arn      = aws_iam_role.glue.arn
  command       = "pythonshell"
  python_version = "3"
  max_retries   = 0
  timeout       = 60

  # Set up SNS notifications for success and failure
  notification_property {
    notify_on_success = true
    notify_on_failure = true
    success_topic_arn = aws_sns_topic.transform_success.arn
    failure_topic_arn = aws_sns_topic.transform_failure.arn
  }

  # Define script location
  command {
    name = "glueetl"
    python_version = "3"
    script_location = "s3://my-bucket/glue_scripts/transform.py"
  }
}

resource "aws_glue_job" "load" {
  name          = "load"
  command       = "glueetl"
  default_arguments = {
    "--job-bookmark-option": "job-bookmark-enable"
  }
  role_arn      = aws_iam_role.glue.arn
  command       = "pythonshell"
  python_version = "3"
  max_retries   = 0
  timeout       = 60

  # Set up SNS notifications for success and failure
  notification_property {
    notify_on_success = true
    notify_on_failure = true
    success_topic_arn = aws_sns_topic.load_success.arn
    failure_topic_arn = aws_sns_topic.load_failure.arn
  }

  # Define script location
  command {
    name = "glueetl"
    python_version = "3"
    script_location = "s3://my-bucket/glue_scripts/load.py"
  }
}

# Define IAM role for Glue jobs
resource "aws_iam_role" "glue" {
  name = "glue_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Define Step Function state machine
resource "aws_sfn_state_machine" "etl" {
  name = "etl"
  definition = jsonencode({
    Comment = "ETL state machine"
    StartAt = "Transform"
    States = {
      Transform = {
        Type = "Task"
        Resource = aws_glue_job.transform.arn
        Next = "Load"
        Catch = [
          {
            ErrorEquals = ["States.ALL"]
            ResultPath = "$.error"
            Next = "Failure"
          }
        ]
      }
      Load = {
        Type = "Task"
        Resource = aws_glue_job.load.arn
        End = true
        Catch = [
          {
            ErrorEquals = ["States.ALL"]
            ResultPath = "$.error"
            Next = "Failure"
          }
        ]
      }
      Failure = {
        Type = "Fail"
        Error = "ETL failed"
      }
    }
  })
}
