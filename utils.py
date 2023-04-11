import openai


def gpt_35_api(api_key: str, messages: list):
    """_summary_

    Args:
        messages (list): _description_
        api_key (str): _description_

    Returns:
        tuple: (results, error_desc)
    """
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
        )
        messages.append({
            'role':
            response['choices'][0]['message']['role'],
            'content':
            response['choices'][0]['message']['content'],
        })
        return (True, '')
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')
