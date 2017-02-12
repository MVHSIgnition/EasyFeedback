$.getScript("my_lovely_script.js", function(){

   alert("Script loaded but not necessarily executed.");


				
				function publish() {
					pubnub = new PubNub({
					publishKey : 'pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284',
					subscribeKey : 'sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe'
					})
					
					function publishQuestion() {
						console.log([info["Question"],[info["Option1"],info["Option2"],info["Option3"],info["Option4"]]]);
						pubnub.publish( {}
						{
							channel : "s_handler",
							message : [info["Question"],[info["Option1"],info["Option2"],info["Option3"],info["Option4"]]]
						}
						function (status, response){
							//a
						}
						)
					}
					
					pubnub.subscribe({
						channels: ['hello_world'] 
					});
				}
});