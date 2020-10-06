echo Make sure you have installed the dependencies!
sleep 3
cd tests
python3 testRequest.py
# testRequest uses some deprecated features and causes annoying logging
# so I want to run it first rather than looping over all of them
python3 testConfig.py
python3 testIntervalParser.py
