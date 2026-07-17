# AK FIRE Monitoring

The AK FIRE monitoring stack provides the AWS architecture to support fire perimeters in real-time from VIIRS Fire detections.

## Architecture overview
AK FIRE monitoring draws fire perimeters from VIIRS detections pushed into an s3 bucket using two approaches depending on the input format:

* txt: If the input is a text file the monitoring stack will run the [FEDS algorithm](https://github.com/Earth-Information-System/fireatlas) 
* netcdf: If the input file has a netcdf format, the monitoring stack will trigger the [fire tracking algorithm](https://github.com/ASFHyP3/hyp3-fire-tracking)

The output in the case of the FEDS algorithm is a `parquet` file with the fire perimeters. For netcdf, the output is a zip file with json files for the fire tracks and a summary in a `parquet` file.

## Development

### Development environment setup

To create a development environment, run:
```shell
conda env update -f environment.yml
conda activate akfire-monitoring
```

A `Makefile` has been provided to run some common development steps:
* `make tests` runs the PyTest test suite.

Review the `Makefile` for a complete list of commands.

### Environment variables

Many parts of this stack are controlled by environment variables. Below is a non-exhaustive list of some environment variables that you may want to set.
* `HYP3_API`: The HyP3 deployment to which jobs will be submitted, e.g. https://hyp3-ak-fire-safe.asf.alaska.edu.
* `EARTHDATA_USERNAME`: Earthdata Login username for the account which will submit jobs to HyP3. In the production stack, this should the AK FIRE operational user; in the test stack, this should be the team testing user.
* `EARTHDATA_PASSWORD`: Earthdata Login password for the account which will submit jobs to HyP3.
* `JOBS_TABLE_NAME`: The jobs table name for the DynamoDB database associated with the HyP3 deployment jobs are submitted to.
* `PUBLISH_BUCKET`: The bucket where the products are stored.
* `ECR_REGISTRY`: Elastic container with the docker image that includes the fire tracking algorithm.
* `NC_TOPIC_ARN`: SNS Topic with for the netcdf files.
* `TXT_TOPIC_ARN`: SNS Topic with for the text files.

 Refer to [`tests/cfg.env`](tests/cfg.env) for a complete list of environment variables.

### Running the Lambda functions locally

The Lambda functions can be run locally from the command line, or by calling the appropriate function in the Python console.

> [!NOTE]
> To call the functions in the python console, you'll need to add all the `src` directories to your `PYTHONPATH`. With PyCharm, you can accomplish this by marking all such directories as "Sources Root" and enabling the "Add source roots to PYTHONPATH" Python Console setting.
