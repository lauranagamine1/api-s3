import boto3
import botocore
import json

def lambda_handler(event, context):
    try:
        # 1) parsear el body
        payload = event.get('body', '{}')
        body = json.loads(payload)

        # 2) validar parámetro
        nombre_bucket = body.get('nombre_bucket')
        if not nombre_bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Falta el parámetro "nombre_bucket".'})
            }

        # 3) crear el bucket (asegúrate de usar sólo minúsculas, dígitos y guiones)
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=nombre_bucket)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Bucket "{nombre_bucket}" creado exitosamente.'
            })
        }

    except botocore.exceptions.ClientError as e:
        # extrae sólo el mensaje de error de AWS
        err = e.response.get('Error', {}).get('Message', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': err})
        }
