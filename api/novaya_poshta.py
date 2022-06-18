import requests
from DataBase.helper.read_config_Methods import read_config

class NovaPoshtaValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

class NovaPoshta:
	config = None
	apiKey = None
	modelName = None
	calledMethod = None
	methodProperties = None
	dataCity = None
	dataNP = NovaPoshtaValue()

	def __int__(self):
		self.config = read_config()
		self.apiKey = self.config['ApiSettings']['api_key_np']
		self.modelName = ''
		self.calledMethod = ''
		self.methodProperties = {}
		self.dataCity = None
		self.dataNP = None

	def setAll(self, modelName, calledMethod, methodProperties):
		self.modelName = modelName
		self.calledMethod = calledMethod
		self.methodProperties = methodProperties

	def response(self):
		params = {
			"apiKey": '297d79dea16044a690778958c6fc7115',
			"modelName": self.modelName,
			"calledMethod": self.calledMethod,
			"methodProperties": self.methodProperties
		}
		print(self.apiKey, self.modelName, self.calledMethod, self.methodProperties)
		response = requests.post(f'https://api.novaposhta.ua/v2.0/json/{self.modelName}/{self.calledMethod}', json=params)
		print('data response: ',response.json()['data'])
		if(self.calledMethod == 'getCities'):
			self.dataCity = response.json()['data']
		else:
			self.dataNP = response.json()['data']



