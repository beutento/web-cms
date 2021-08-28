from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_s3_deployment as s3deploy,
    core
)


class InfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "web-cms-s3",
                           bucket_name = "web-cms-project",
                           public_read_access=True,
                           website_index_document = "index.html",
                           website_error_document = "404.html"
                          )
        core.CfnOutput(self, "webcmsbucketname", value = bucket.bucket_name)
        core.CfnOutput(self, "webcmsbucketURL", value = bucket.bucket_website_url)
        
        source_config = cloudfront.SourceConfiguration(
            s3_origin_source = cloudfront.S3OriginConfig(
                s3_bucket_source = bucket,
            ),
            behaviors = [cloudfront.Behavior(is_default_behavior=True)]    
        )
        
        distribution = cloudfront.CloudFrontWebDistribution(
                            self, "web-cf-dist",
                            origin_configs = [source_config]
        )
        core.CfnOutput(self, "web_distribution_id", value = distribution.distribution_id)
        core.CfnOutput(self, "web_cloudfront_domain", value = distribution.domain_name)