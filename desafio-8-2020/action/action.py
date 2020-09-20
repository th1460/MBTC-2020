from cgi import parse_multipart, parse_header
from io import BytesIO
from base64 import b64decode
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
import json, os

# Aqui importamos as classes que cuidam dos serviços do Natural Language Understanding e do Speech-to-Text
from ibm_watson import NaturalLanguageUnderstandingV1, SpeechToTextV1

# Puxamos, para o natural language understanding, as classes de Features e EntitiesOptions que serão úteis para obter as entidades e os sentimentos associdados
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

# Só é possível se conectar aos seus serviços se você se autenticar, e a classe que cuidará disso é o IAMAuthenticator
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(args):

    # Parse incoming request headers
    _c_type, p_dict = parse_header(
        args['__ow_headers']['content-type']
    )
    
    # Decode body (base64)
    decoded_string = b64decode(args['__ow_body'])

    # Set Headers for multipart_data parsing
    p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
    p_dict['CONTENT-LENGTH'] = len(decoded_string)
    
    # Parse incoming request data
    multipart_data = parse_multipart(
        BytesIO(decoded_string), p_dict
    )
    
    text = multipart_data.get('text')
    
    if text is not None:
        text = text[0]
    else:
        
        # Build flac file from stream of bytes
        fo = open("audio_sample.flac", 'wb')
        fo.write(multipart_data.get('audio')[0])
        fo.close()

        # Basic Authentication with Watson STT API
        stt_authenticator = BasicAuthenticator(
            'apikey',
            '9kesqvRxa7lKR3WUkcR81zFXfhrJXXYl3dzobsEWEfCM'
        )
    
        # Construct a Watson STT client with the authentication object
        stt = SpeechToTextV1(
            authenticator=stt_authenticator
        )
    
        # Set the URL endpoint for your Watson STT client
        stt.set_service_url(
                'https://api.us-south.speech-to-text.watson.cloud.ibm.com'
        )
    
        # Read audio file and call Watson STT API:
        with open(
            os.path.join(
                os.path.dirname(__file__), './.',
                'audio_sample.flac'
            ), 'rb'
        ) as audio_file:
            # Transcribe the audio.flac with Watson STT
            # Recognize method API reference: 
            # https://cloud.ibm.com/apidocs/speech-to-text?code=python#recognize
            stt_result = stt.recognize(
                audio=audio_file,
                content_type='audio/flac',
                model='pt-BR_BroadbandModel'
            ).get_result()
    
        # Print STT API call results
        print(json.dumps(stt_result, indent=2))
    
        # Return a dictionary with the transcribed text
        transcript = stt_result['results'][0]['alternatives'][0]['transcript']
        text = transcript
        
    # Serviço NLU
    nlu_apikey = "rv_tVs7qTDhdlEtEwcY-D11AGDdI6VVkVh8RaZj1jwQ-"
    nlu_service_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com"
    nlu_entity_model = "187ea1d8-ea11-4285-b96e-32db2996a9aa"
    
    # Cria-se um autenticador
    nlu_authenticator = IAMAuthenticator(apikey=nlu_apikey)

    # Criamos o serviço passando esse autenticador
    nlu_service = NaturalLanguageUnderstandingV1(version='2018-03-16', authenticator=nlu_authenticator)

    # Setamos a URL de acesso do nosso serviço
    nlu_service.set_service_url(nlu_service_url)
    
    # O método analyze cuida de tudo
    nlu_response = nlu_service.analyze(text=text, features=Features(entities=EntitiesOptions(model=nlu_entity_model, sentiment=True)), language='pt').get_result()

    return { 'result': json.dumps(nlu_response['entities'][0], indent=2, ensure_ascii=False) }
