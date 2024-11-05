class AddScene:
    def __init__(self):
        self.__table_features_any = []
        self.__table_features = []

    def any(self):
        def wrapper(func):
            self.__table_features_any.append(func)
        return wrapper

    def command(self, *args):
        def wrapper(func):
            self.__table_features.append({func: args[0]})
        return wrapper

    def __get_response(self, command_txt, ctx, data):
        for func in self.__table_features:
            for text_f in func:
                if command_txt in func[text_f]:
                    return text_f(ctx, data)
        return None

    def __route_scene(self, ctx, command_txt, data):
        if not (result_response := self.__get_response(command_txt, ctx, data)):
            result_response = self.__table_features_any[0](ctx, data)
        return result_response
    
class ReactAlice:

    def __init__(self):
        self.__table_features = []
        self.__table_features_any = []
        self.__table_features_start = []
        self.__table_features_timeout = []

    def start(self):
        def wrapper(func):
            self.__table_features_start.append(func)
        return wrapper
    
    def timeout(self):
        def wrapper(func):
            self.__table_features_timeout.append(func)
        return wrapper

    def any(self):
        def wrapper(func):
            self.__table_features_any.append(func)
        return wrapper

    def command(self, *args):
        def wrapper(func):
            if not type(args[0]) == list:
                self.__table_features.append({func: [args[0]]})
            else:
                self.__table_features.append({func: args[0]})
        return wrapper

    def __get_custom_func(self, command_txt, ctx, data):
        for func in self.__table_features:
            for text_f in func:
                if command_txt in func[text_f]:
                    return text_f(ctx, data)
        return None
    
    def __rout_scene(self, ctx, data):
        command_txt = ' '.join(ctx['request']['nlu']['tokens'])
        if not (scene := ctx['state']['session'].get('s')):
            if not(custom_response := self.__get_custom_func(command_txt, ctx, data)):
                custom_response = self.__table_features_any[0](ctx, data)
            return custom_response
        if scene_custom := getattr(self, scene, None):
            return scene_custom._AddScene__route_scene(ctx, command_txt, data)
        raise ValueError(f'!! -> Ошибка.. Сцены "{scene}" не существует.')

    def __create_response_json(self, custom_response):
        result_response = {
        "response": {
            "text": "",
            "tts": "",
            "end_session": False,
            "directives": {}
        },
        "session_state": {},
        "user_state_update": {},
        "application_state": {},
        "analytics": {},
        "version": "1.0"
        }
        if custom_response.get('data'):
            if custom_response['data']['us']:
                result_response['session_state']['d'] = custom_response['data']['us']
            if custom_response['data']['ws']:
                result_response['user_state_update'] = custom_response['data']['ws']
            if custom_response['data']['as']:
                result_response['application_state'] = custom_response['data']['as']
            if custom_response['data']['scene']:
                result_response['session_state']['s'] = custom_response['data']['scene']
        result_response["response"]['text'], result_response["response"]['tts'] = self.__get_txt_tts(custom_response)
        if custom_response.get('buttons', None):
            result_response["response"]['buttons'] = custom_response['buttons']
        if custom_response.get('card', None):
            result_response["response"]['card'] = custom_response['card']
        print('!!', result_response)
        return result_response
    
    def run(self, ctx, timeout=3):
        import asyncio
        data = {
            'us': ctx['state']['session'].get('d', {}),
            'ws': ctx['state'].get('user', {}),
            'as': ctx['state'].get('application', {}),
            'scene': ctx['state']['session'].get('s', '')
        }
        async def handler():
            # await asyncio.sleep(5)
            if not ctx['session']['message_id']:
                custom_response = self.__table_features_start[0](ctx, data)
            else:   
                custom_response = self.__rout_scene(ctx, data)
            return self.__create_response_json(custom_response)
        async def timeout_function(timeout):
            try:
                result_ok = await asyncio.wait_for(handler(), timeout)
                return result_ok
            except asyncio.TimeoutError:
                if self.__table_features_timeout:
                    return self.__table_features_timeout[0](ctx, data)
        result_response = asyncio.run(timeout_function(timeout))
        return result_response

    def __get_txt_tts(self, custom_response):
        if type(custom_response['txt']) == list:
            from random import choice
            custom_response = choice(custom_response['txt'])
            if type(custom_response) == str:
                return custom_response, custom_response
        return custom_response['txt'], custom_response.get('tts', custom_response['txt'])

Alice = ReactAlice()