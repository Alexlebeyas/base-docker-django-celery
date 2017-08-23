# Project Starter ReadMe

## Launching a New Project
Launching a new project is easy.
In a terminal window inside project-starter

~~~~
python install PROJECT_NAME
~~~~

## Generating a Secret Key
To generate a random Secret Key for your .env file open a python interpreter
and run the following command

~~~~
from uuid import uuid4
random_key = lambda: str(uuid4()).replace('-', '')
random_key()
~~~~