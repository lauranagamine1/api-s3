import boto3
import json
import botocore

def lambda_handler(event, context):
    try:
        body = event['body']

        # Obtener nombre del bucket y nombre del directorio
        nombre_bucket = body['nombre_bucket']
        nombre_directorio = body['nombre_directorio']

        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'

        # Cliente S3
        s3 = boto3.client('s3')

        # Crear un objeto vacío para simular el directorio
        s3.put_object(Bucket=nombre_bucket, Key=nombre_directorio)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Directorio "{nombre_directorio}" creado en el bucket "{nombre_bucket}".'
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Falta el parámetro requerido: {str(e)}'})
        }

    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }