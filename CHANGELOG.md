## 0.0.30

* Updated README.
* Some methods related to query execution are now thread-safe.

## 0.0.29

* The order of arguments in RawQueryBuilder's add has been corrected to align with other functions.
* Fixed an issue where TimestampNode times were not the same as in the Dart version.
* The returnData flag is now available for Add and ClearAdd queries.
* The returnData flag for various queries has been changed to an optional argument.
* The Actor class now has a collectionPermissions, which uses a dedicated Permissions type.
* As a result, the method for setting permissions in the DeltaTraceDatabase class has been changed from an Enum to a dedicated type.

## 0.0.26

* Several methods in the DeltaTraceDatabase class now have an allows parameter to grant permission
  to execute queries.
* When sorting, you can now convert to a specified type.
* The code documentation has been improved.

## 0.0.25

* Added reset serial option to the clear and clearAdd queries.

## 0.0.23

* The serialKey parameter has been added to Query(add, clearAdd).

## 0.0.21.post1

* Tweaked argument names to reduce discrepancies when compared to the Dart version.

## 0.0.21

* Added UtilQuery class.

## 0.0.20

* When executing a query, users can now specify which queries are explicitly disallowed via optional arguments.

## 0.0.19

* The README has been tweaked.

## 0.0.18.post1

* The GitHub link for the project was incorrect, so it has been fixed.

## 0.0.18

* initial release. The version number is standardized for compatibility with versions in other languages.
