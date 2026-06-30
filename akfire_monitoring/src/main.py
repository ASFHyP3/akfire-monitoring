"""akfire-monitoring processing for HyP3."""

import logging
import os
from copy import deepcopy

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


def lambda_handler(event: dict, context: object) -> dict:
    """FEDS processing lambda function.

    Args:
        event: The event dictionary that contains the parameters sent when this function is invoked.
        context: The context in which is function is called.

    Returns:
        FEDS submitted job.
    """
    hyp3 = get_hyp3_instance()
    feds_job = deepcopy(FEDS_JOB_TEMPLATE)
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
    hyp3 = get_hyp3_instance()
    firetrack_job = deepcopy(FIRETRACK_JOB_TEMPLATE)
    firetrack_job = hyp3.submit_prepared_jobs(firetrack_job)
    return firetrack_job


def main() -> None:
    """HyP3 entrypoint for akfire_monitoring."""
    return None


if __name__ == '__main__':
    main()
