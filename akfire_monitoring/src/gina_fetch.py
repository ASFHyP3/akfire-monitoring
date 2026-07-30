"""Utilities for fetching VIIRS products and uploading them into S3 prefixes."""

import logging
import os
from pathlib import Path

import boto3
import requests
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from gina_nrt_fetch.fetch_products import (
    SearchParams,
    filter_by_wildcard,
    retrieve_product_list,
)


log = logging.getLogger('akfire_monitoring')
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO'))

PUBLISH_BUCKET = os.getenv('PUBLISH_BUCKET')


def fetch_viirs_detections() -> tuple[list[str], list[str]]:
    """Fetch VIIRS fire products and return paired TXT and NetCDF URLs.

    Returns:
        A tuple of two URL lists: TXT product URLs and paired NetCDF product URLs.
    """
    search_params = SearchParams(sensor='viirs', processing_level='fire')

    products = retrieve_product_list(search_params.to_query_params())
    txt_products = filter_by_wildcard(products, '.txt')
    txt_file_paths = [Path(t) for t in txt_products]

    nc_products = filter_by_wildcard(products, '.nc')
    nc_products = [n for n in nc_products if Path(n).with_suffix('.txt') in txt_file_paths]
    if not sorted([t.stem for t in txt_file_paths]) == sorted([Path(n).stem for n in nc_products]):
        raise ValueError('Not all .txt files have a paired .nc file (or vice versa)')
    return txt_products, nc_products


def exists_on_s3(s3: BaseClient, bucket: str, key: str) -> bool:
    """Return True when the object exists in S3, otherwise False for 404-like responses."""
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as exc:
        error_code = exc.response.get('Error', {}).get('Code', '')
        if error_code in {'404', 'NotFound', 'NoSuchKey'}:
            return False
        raise


def check_and_upload_s3(file: str, s3: BaseClient, bucket: str, key: str) -> None:
    """Upload URL content to S3 when the destination key does not already exist."""
    if not exists_on_s3(s3, bucket, key):
        log.info('Uploading file %s', file)
        with requests.get(file, stream=True) as response:
            response.raise_for_status()

            s3.upload_fileobj(
                Fileobj=response.raw,
                Bucket=bucket,
                Key=key,
                ExtraArgs={'ContentType': response.headers.get('content-type')},
            )
    else:
        log.debug('File already in bucket: %s', file)


def run_upload(s3_bucket: str) -> None:
    """Fetch VIIRS detections and upload paired TXT/NetCDF products to S3."""
    s3 = boto3.client('s3')

    txt_files, nc_files = fetch_viirs_detections()

    for f in txt_files:
        key = f'txt/{Path(f).name}'
        check_and_upload_s3(f, s3, s3_bucket, key)

    for nc in nc_files:
        key = f'netcdf/{Path(nc).name}'
        check_and_upload_s3(nc, s3, s3_bucket, key)
