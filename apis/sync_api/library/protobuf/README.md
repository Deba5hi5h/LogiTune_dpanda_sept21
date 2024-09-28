# Logitech VC Protocol Buffer API Modules
This repository contains a set of public and private Protocol Buffer API modules that can be compiled in various combinations to the user's language(s) of choice. This repository currently references the public Sync Protocol Buffer message API along with defining an internal Protocol Buffer message API for Raiden.

## Prerequisites
In order to compile the Protocol Buffer message APIs, you must first do the following:
  
1. Download the Protocol Buffer compiler from [here](https://github.com/protocolbuffers/protobuf/releases). You'll want to download one of the _protoc_ archives that matches your operating system. Add the _protoc_ executable to your PATH.
2. Retrieve the Sync API submodule and ensure that the master branch for that API is checked out by entering the following git commands (from the root project directory):

   _git submodule init_  
   _git submodule update_  
   _cd sync_  
   _git checkout master_
   
## Compiling the Protocol Buffer APIs
For more information on compiling the Protocol Buffer APIs, see the usage notes by running the provided script with the -h option.

_scripts/compile.sh -h_
