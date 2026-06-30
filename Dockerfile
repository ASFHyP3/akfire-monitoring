FROM public.ecr.aws/lambda/python:3.12

COPY requirements-akfire_monitoring.txt ${LAMBDA_TASK_ROOT}

RUN dnf -y install git

RUN pip install -r requirements-akfire_monitoring.txt

COPY akfire_monitoring/src ${LAMBDA_TASK_ROOT}

#RUN python ${LAMBDA_TASK_ROOT}/main.py

# NOTE: handler set as CMD by  parameter override outside of the Dockerfile
# CMD [ "lambda_function.handler" ]
