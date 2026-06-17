"""akfire-monitoring processing for HyP3."""


log = logging.getLogger('akfire_monitoring')
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO'))


def lambda_handler(event: dict, context: object) -> dict:
    """Landsat processing lambda function.
    """
    return None


def lambda_bucket_handler(event: dict, context: object) -> dict:
    """Bucket notification processing lambda function.
    """
    return None


def main() -> None:
    """HyP3 entrypoint for akfire_monitoring."""
    return None


if __name__ == '__main__':
    main()
