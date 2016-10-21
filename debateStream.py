import json
import time
from ISStreamer.Streamer import Streamer

timesToRun = 960

streamer = Streamer(bucket_name="Debate Tweets", bucket_key = "BUCKET KEY", access_key="ACCESS KEY")

print "Stream Starting"
streamer.log("My Messages", "Stream Starting")

def streamDat(x):
    with open('sent.json') as fi:
        data = json.load(fi)
        trumpP = data['trumpPos']
        trumpN = data['trumpNeg']
        hillaryP = data['hillaryPos']
        hillaryN = data['hillaryNeg']

        streamer.log("trumpP", int(trumpP))
        streamer.log("trumpN", int(trumpN))
        streamer.log("hillaryP", int(hillaryP))
        streamer.log("hillaryN", int(hillaryN))
        count = x + 1
        time.sleep(5)
        message = "Done with loop " + str(count)
        print message
        streamer.log("My Messages", message)
        if (not count == timesToRun):
            streamDat(count)

streamDat(0)

print "Stream Done"
streamer.log("My Messagges", "Stream Done")
