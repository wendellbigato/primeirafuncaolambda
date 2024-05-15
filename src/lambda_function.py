import json
import boto3
import uuid

def lambda_handler(event, context):
    # Conexão com o DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('NomeDaTabelaDoDynamo')

    # Recuperar o método HTTP da requisição
    http_method = event.get('httpMethod')

    # Tratamento para o método POST
    if http_method == 'POST':
        body = json.loads(event.get('body', '{}'))
        user_id = str(uuid.uuid4())
        item = {
            'id': user_id,
            'Nome': body.get('nome'),
            'Email': body.get('email'),
            'CPF': body.get('cpf')
        }
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps('Usuário cadastrado com sucesso!')
        }

    # Tratamento para o método GET
    elif http_method == 'GET':
        user_id = event.get('queryStringParameters', {}).get('id')
        if user_id:
            response = table.get_item(Key={'id': user_id})
            if 'Item' in response:
                return {
                    'statusCode': 200,
                    'body': json.dumps(response['Item'])
                }
            return {
                'statusCode': 404,
                'body': json.dumps('Usuário não encontrado.')
            }
        return {
            'statusCode': 400,
            'body': json.dumps('ID do usuário não fornecido.')
        }

    # Tratamento para o método PUT
    elif http_method == 'PUT':
        user_id = event.get('queryStringParameters', {}).get('id')
        if user_id:
            body = json.loads(event.get('body', '{}'))
            response = table.get_item(Key={'id': user_id})
            if 'Item' in response:
                table.update_item(
                    Key={'id': user_id},
                    UpdateExpression='set Nome = :n, Email = :e, CPF = :c',
                    ExpressionAttributeValues={
                        ':n': body.get('nome'),
                        ':e': body.get('email'),
                        ':c': body.get('cpf')
                    }
                )
                return {
                    'statusCode': 200,
                    'body': json.dumps('Usuário atualizado com sucesso.')
                }
            return {
                'statusCode': 404,
                'body': json.dumps('Usuário não encontrado.')
            }
        return {
            'statusCode': 400,
            'body': json.dumps('ID do usuário não fornecido.')
        }

    # Resposta padrão para métodos não suportados
    return {
        'statusCode': 405,
        'body': json.dumps('Método não permitido')
    }
