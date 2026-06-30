"""akfire-monitoring processing for HyP3."""

import logging
import os
from copy import deepcopy
from datetime import datetime

import hyp3_sdk as sdk


log = logging.getLogger('akfire_monitoring')
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO'))


FEDS_JOB_TEMPLATE = {
    'job_type': 'AK_FIRE_SAFE',
    'bucket': os.environ.get('PUBLISH_BUCKET'),
    'bucket_prefix': 'feds',
    'job_parameters': {
        'extent': [-169.01, 52.37, -130.16, 71.66],
        'upload_to_db': False,
        'input_bucket': os.environ.get('PUBLISH_BUCKET'),
        'input_prefix': 'txt',
    },
}

FIRETRACK_JOB_TEMPLATE = {
    'job_type': 'FIRE_TRACK',
    'bucket': os.environ.get('PUBLISH_BUCKET'),
    'bucket_prefix': 'firetracks',
    'job_parameters': {'input_bucket': os.environ.get('PUBLISH_BUCKET'), 'input_prefix': 'netcdf'},
}


def get_hyp3_instance() -> sdk.HyP3:
    """Get an instance for the HyP3 sdk.

    Returns:
        hyp3: HyP3 sdk instance.
    """
    hyp3 = sdk.HyP3(
        os.environ.get('HYP3_API'),
        username=os.environ.get('EARTHDATA_USERNAME'),
        password=os.environ.get('EARTHDATA_PASSWORD'),
    )
    return hyp3


def prepare_feds(name: str) -> dict:
    feds_job = deepcopy(FEDS_JOB_TEMPLATE)
    feds_job['name'] = name
    return feds_job


def prepare_firetrack(name: str) -> dict:
    firetrack_job = deepcopy(FIRETRACK_JOB_TEMPLATE)
    firetrack_job['name'] = name
    return feds_job


def lambda_handler(event: dict, context: object) -> dict:
    """FEDS processing lambda function.

    Args:
        event: The event dictionary that contains the parameters sent when this function is invoked.
        context: The context in which is function is called.

    Returns:
        FEDS submitted job.
    """
    sdate = datetime.now().strftime("%y%m%d%H%M%S")
    name = f'FEDS_{sdate}'
    hyp3 = get_hyp3_instance()
    feds_job = prepare_feds(name)
    feds_job = hyp3.submit_prepared_jobs(feds_job)
    return feds_job


def lambda_bucket_handler(event: dict, context: object) -> dict:
    """Fire track notification processing lambda function.

    Args:
        event: The event dictionary that contains the parameters sent when this function is invoked.
        context: The context in which is function is called.

    Returns:
        Fire track submitted job.
    """
    sdate = datetime.now().strftime("%y%m%d%H%M%S")
    name = f'FIRETRACK_{sdate}'
    hyp3 = get_hyp3_instance()
    firetrack_job = prepare_firetrack(name)
    firetrack_job = hyp3.submit_prepared_jobs(firetrack_job)
    return firetrack_job


def main() -> None:
    """HyP3 entrypoint for akfire_monitoring."""
    return None


if __name__ == '__main__':
    main()
