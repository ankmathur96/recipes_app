from django.shortcuts import render
from django.http import HttpResponse
from . import verify as vf
from django.views.decorators.csrf import csrf_exempt
import json

def help_response(json_response):
	response = {}
	response['shouldEndSession'] = False
	response['outputSpeech'] = {'type' : "PlainText", 'text' : "Hi! This is Recipes Guru! - you can use to me cook interactively!", 'ssml' : ''}
	json_response['outputSpeech'] = response
	return json.dumps(json_response)

# Create your views here.
@csrf_exempt
def respond(request):
	print(vf.validate_alexa_request(request.META, request.body))
	request_body = json.loads(request.body)
	intent = request_body['request']
	json_response = {'version' : '1.0'}
	if (intent['type'] == 'LaunchRequest'):
		json_response = help_response(json_response)
	elif (intent['type'] == 'IntentRequest'):
		json_response =  help_response(json_response)
	elif (intent['type'] == "SessionEndedRequest"):
		json_response = help_response(json_response)
	
	response = HttpResponse(status=200)
	response['Content-Type'] = 'application/json'
	print('LOG RESPONSE: ', json_response)
	response.content = json_response
	print('LOG RESPONSE: ', response)
	return response
