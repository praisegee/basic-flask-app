# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Install system dependencies if needed (optional)
# RUN apt-get update && apt-get install -y --no-install-recommends <your-dependencies>

# Set environment variables
ENV LAMBDA_TASK_ROOT=/var/task
ENV PYTHONPATH=$LAMBDA_TASK_ROOT

# Copy requirements from root and App directory
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
COPY App/requirements.txt ${LAMBDA_TASK_ROOT}/App/

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt && \
    pip install -r ${LAMBDA_TASK_ROOT}/App/requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the function code into the Lambda task root directory
COPY App/lambda_handler.py ${LAMBDA_TASK_ROOT}/
#COPY App/lambda_function.zip ${LAMBDA_TASK_ROOT}/

# If you have additional files or directories to copy, add them here
# COPY some_directory/ ${LAMBDA_TASK_ROOT}/some_directory/

# Set the command to your handler function
CMD ["lambda_handler.handler"]
