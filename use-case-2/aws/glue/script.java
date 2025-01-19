import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import gs_now

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Source S3 Bucket
SourceS3Bucket_node1729343435468 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://usecase2sourcebucket"], "recurse": True}, transformation_ctx="SourceS3Bucket_node1729343435468")

# Script generated for node Add Migdate
AddMigdate_node1729344089243 = SourceS3Bucket_node1729343435468.gs_now(colName="migdate")

# Script generated for node Target S3 Bucket
TargetS3Bucket_node1729344140227 = glueContext.write_dynamic_frame.from_options(frame=AddMigdate_node1729344089243, connection_type="s3", format="json", connection_options={"path": "s3://usecase2targetbucket", "partitionKeys": ["migdate"]}, transformation_ctx="TargetS3Bucket_node1729344140227")

job.commit()