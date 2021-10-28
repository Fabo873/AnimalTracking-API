
def returnFormat(message='', data={}, status=200) -> tuple:
    return {
        'message': message,
        'data': data
    }, status
