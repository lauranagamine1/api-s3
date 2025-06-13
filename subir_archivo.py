import boto3
import json
import base64
import botocore

def lambda_handler(event, context):
    try:
        body = event['body']

        nombre_bucket = body['nombre_bucket']
        directorio = body['directorio']  # Ej: 'carpeta1/' o '/' si es raíz
        nombre_archivo = body['nombre_archivo']  # Ej: 'miarchivo.txt'
        archivo_b64 = body['archivo_b64']  # base64 string

        if directorio == '/':
            key = nombre_archivo
        else:
            if not directorio.endswith('/'):
                directorio += '/'
            key = directorio + nombre_archivo

        archivo_binario = base64.b64decode(archivo_b64)

        s3 = boto3.client('s3')
        s3.put_object(Bucket=nombre_bucket, Key=key, Body=archivo_binario)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Archivo "{nombre_archivo}" subido a "{key}" en el bucket "{nombre_bucket}".'
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Falta el parámetro requerido: {str(e)}'})
        }

    except base64.binascii.Error:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'El contenido base64 no es válido.'})
        }

    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }