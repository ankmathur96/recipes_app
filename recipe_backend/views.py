from django.shortcuts import render
from django.http import HttpResponse
from . import verify as vf
from django.views.decorators.csrf import csrf_exempt
import json
import requests

def help_response(json_response):
	response = {}
	response['shouldEndSession'] = False
	response['outputSpeech'] = {'type' : "PlainText", 'text' : "Hi! This is Recipes Guru! - you can use to me cook interactively!", 'ssml' : ''}
	json_response['response'] = response
	return json.dumps(json_response)

def get_recipe(recipeName):
	web_response = ("http://www.simplyrecipes.com/?s="+recipeName)

def check_intent(json_response, request):
	response = {}
	response['shouldEndSession'] = False
	intent = request['intent']
	if (intent['name'] == 'getRecipe'):
		recipeSlots = intent['slots']
		if ('risotto' in recipeSlots):
			response = {'type' : "PlainText", 'text' : "1. Heat the clam juice and water. 2. Saute shallots. 3. Add the rice to the pot. Stir-fry the rice for 2-3 minutes. 4. Add white wine and stir. 5. Add two ladles of clam juice water mixture. 6 Stirring almost constantly, let this liquid reduce until it is almost gone, then add another ladle of broth. 7. Now add in the shrimp, the parsley, and the remaining tablespoon of butter"}
		json_response['response'] = response
		return json.dumps(json_response)
	else:
		response = {'type': "PlainText", 'text': "Sorry. I am unable to tell you a recipe for that"}
		json_response['response'] = response
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
		json_response =  check_intent(json_response, intent)
	elif (intent['type'] == "SessionEndedRequest"):
		json_response = help_response(json_response)

	response = HttpResponse(status=200)
	response['Content-Type'] = 'application/json'
	print('LOG RESPONSE: ', json_response)
	response.content = json_response
	print('LOG RESPONSE: ', response)
	return response
