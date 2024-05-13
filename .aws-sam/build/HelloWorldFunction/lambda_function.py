import json
# comentario
def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World from Lambda! Versao 2')
    }

