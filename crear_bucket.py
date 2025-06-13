import boto3
import botocore
import json

def lambda_handler(event, context):
    try:
        body = event['body']
        
        nombre_bucket = body['nombre_bucket']

        s3 = boto3.client('s3')
        
        s3.create_bucket(Bucket=nombre_bucket)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Bucket "{nombre_bucket}" creado exitosamente.'
            })
        }
    
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el parámetro "nombre_bucket".'})
        }
    
    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }