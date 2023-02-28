# instructions

install protocol buffers
```commandline
brew install protobuf
```

or in linux
```commandline
apt install -y protobuf-compiler
```

make sure you have protoc
```commandline
protoc --version
```

create virtual environment
```commandline
python3 -m venv venv
```

install python dependencies
```commandline
pip install -r requirements.txt
```

generate python code from proto file
```commandline
protoc --python_out=. log.proto
```

should see a log_pb2.py file

run the program
```commandline
python main.py start
```

example REPL calls
```commandline
$ python main.py start
Enter command (add/get/exit): add
Enter city name: San Francisco
Enter population: 884363
Enter land area: 46.9
Added entry for San Francisco
Enter command (add/get/exit): get
Enter city name: San Francisco
Population of San Francisco: 884363
Enter command (add/get/exit): exit
```

todo
- [ ] add tests
- [ ] add compaction and merging algorithm for log files
- [ ] make generic for any key value store (instead of just cities)
- [ ] add more commands (delete, update, etc)
- [ ] fix issue with exit command (it doesn't exit)
- [ ] add size limit to log files and implement log rotation
