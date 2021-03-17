

def lambda_handler(event, context):
    f = open('index.html', 'r')
    html = f.read()
    f.close()

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html
    }
