import requests, json, time
from discord_webhook import DiscordEmbed, DiscordWebhook



class Monitor():
	def __init__(self):
		self.webhook="" #YOUR DISCORD WEBHOOK
		self.coronaEndpoint="https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22confirmed%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22deaths%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22recovered%22%7D%5D"
		self.uaString="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
		self.session=requests.session()
		self.sleepDelay=10000
		self.recovered=132
		self.confirmed=7783
		self.deaths=170

	def send_webhook(self, infected, recovered, dead):
		try:
			wHook=DiscordWebhook(self.webhook, content=":biohazard: Corona Virus Alert :biohazard: ")

			embed=DiscordEmbed(title="Corona Virus Monitor",description="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH")
			wHook.add_embed(embed)
			embed.add_embed_field(name="Infected",value=str(infected))
			embed.add_embed_field(name="Dead",value=str(dead))
			embed.add_embed_field(name="Recovered",value=str(recovered))
			embed.set_thumbnail(url="https://www.multicash.it/pub/media/catalog/product/cache/image/e9c3970ab036de70892d86c6d221abfe/1/2/1274900_1.jpg")
			
			wHook.execute()
		except Exception as e:
			raise e
	def monitor(self):
		try:
			while True:
				r=self.session.request("GET", self.coronaEndpoint, headers={"user-agent":self.uaString})
				cases=r.json()['features'][0]['attributes']
				if cases['confirmed']>self.confirmed or cases['deaths']>self.deaths or cases['recovered']>self.recovered:
					print("new corona virus changes detected")
					self.send_webhook(cases['confirmed'],cases['recovered'],cases['deaths'])
					self.recovered=cases['recovered']
				else:
					print("no new corona virus changes detcted")
					time.sleep(100)
		except Exception as e:
			print(e)
			time.sleep(100)
			self.monitor()
m=Monitor()
if __name__ == '__main__':
	m.monitor()
