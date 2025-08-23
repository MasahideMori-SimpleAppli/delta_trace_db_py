# delta_trace_db_py

* This package is currently under construction.

Python implementation of DeltaTraceDB.

## Usage

Please refer to the [Dart version](https://github.com/MasahideMori-SimpleAppli/delta_trace_db).  
There are some differences,   
such as arguments being snake case by default and an underscore being added after the variable name   
if there is a namespace conflict with a standard function, but the usage is the same.

## Speed

This package is an in-memory database, so it is generally fast.  
Currently, there is no mechanism to speed it up, but it works almost the same as a for loop in a program,  
so there is usually no problem with around 100,000 records.  
I recommend that you test it in an actual environment using speed_test.dart in the test folder.  
However, since it consumes RAM capacity according to the amount of data,  
if you need an extremely large database, consider using a general database.  
For reference, below are the results of a speed test (test/speed_test.dart) run on a slightly  
older PC equipped with a Ryzen 3600 CPU.  
The test conditions were chosen to take a sufficiently long time, but I think it will rarely
cause   
any problems in practical use.
Please note that speeds also depend on the amount of data, so if you have a lot of large data, it will be slower.

```text
tests/test_speed.py speed test for 100000 records
start add
end add: 339 ms
start getAll (with object convert)
end getAll: 659 ms
returnsLength: 100000
start save (with json string convert)
end save: 467 ms
start load (with json string convert)
end load: 557 ms
start search (with object convert)
end search: 818 ms
returnsLength: 100000
start search paging, half limit pre search (with object convert)
end search paging: 379 ms
returnsLength: 50000
start update at half index and last index object
end update: 96 ms
start updateOne of half index object
end updateOne: 31 ms
start conformToTemplate
end conformToTemplate: 79 ms
start delete half object (with object convert)
end delete: 562 ms
returnsLength: 50000
start deleteOne for last object (with object convert)
end deleteOne: 22 ms
returnsLength: 1
```

## Future plans

It is possible to speed up the database, but this is a low priority, so I think that improving
usability and creating peripheral tools will take priority.

## Support

There is essentially no support at this time, but bugs will likely be fixed.  
If you find any issues, please open an issue on Github.

## About version control

The C part will be changed at the time of version upgrade.  
However, versions less than 1.0.0 may change the file structure regardless of the following rules.

- Changes such as adding variables, structure change that cause problems when reading previous
  files.
    - C.X.X
- Adding methods, etc.
    - X.C.X
- Minor changes and bug fixes.
    - X.X.C

## License

This software is released under the Apache-2.0 License, see LICENSE file.

Copyright 2025 Masahide Mori

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Copyright notice

The “Dart” name and “Flutter” name are trademarks of Google LLC.  
*The developer of this package is not Google LLC.
