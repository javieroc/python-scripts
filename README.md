### Simple data transformation script

## Prerequisites

- Python 3.x installed

## How to use.

To run the script you should execute in the console

```
python script.py -c config.json -i before.csv -o after.csv
```

With the flag `-c` we specify a mapping file. This file match the client fields with the fields that the process need. You can pass a config file named different, e.g: `client1.json`, if you don't pass any config file, by default the script looking for a file called `config.json`.

The option `-i` is the name of the file that we want transform. And the flag `-o` is
the name of the output file.

We include some examples related with 2 clients, the `config.json` is related to the
first client, and the `config2.json` is related to the second client.
