from botocore.exceptions import ClientError


def create_user(user_id, age, sex, weight, dynamodb):
    table = dynamodb.Table('UserFitness')
    response = table.put_item(
        Item={
            'userId': user_id,
            'generalInfo': {
                "M": {
                    "age": {
                        "N": age
                    },
                    "sex": {
                        "S": sex
                    },
                    "weight": {
                        "N": weight
                    }
                }
            },
            "weightHistory": [],
            "schedule": []
        }
    )
    return response


def get_user_fitness_info(user_id, dynamodb):
    table = dynamodb.Table('UserFitness')

    try:
        response = table.get_item(Key={'userId': user_id})
    except ClientError as e:
        return None;
    else:
        if 'Item' in response.keys():
            return response['Item']
        else:
            return None;


def update_weight(user_id, weight, weight_history, dynamodb):
    table = dynamodb.Table('UserFitness')

    response = table.update_item(
        Key={
            'userId': user_id,
        },
        UpdateExpression="set generalInfo.weight=:w , weightHistory=:wh",
        ExpressionAttributeValues={
            ':w': weight,
            ':wh': weight_history
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
