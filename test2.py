from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
pnconfig.ssl = False
 
pubnub = PubNub(pnconfig)

pubnub.subscribe().channels('main_eh').execute()

def publish_callback(result, status):
    pass

pubnub.publish().channel('main_eh').message(["what","theheck"])\
        .should_store(True).use_post(True).async(publish_callback)
