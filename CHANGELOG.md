## 0.0.38.post1

* Updated docs.

## 0.0.38

* Updated readme.

## 0.0.37

* Added docs.
* Refactoring was performed.
* Fixed an issue where the return type hints for initiated_at and finalized_at in TemporalTrace were incorrect.
* Fixed an issue where the Actor class did not inherit CloneableFile.
* Fixed an issue where the Query class did not inherit CloneableFile.

## 0.0.36

* Refactoring was performed.
* The Actor class has had roles and permissions removed, replaced by the simpler collectionPermissions.
* Fixed an issue where hash calculation for collectionPermissions was not done.
* The hash calculation method for the Actor class has been changed to be similar to the method used in other language versions.

## 0.0.35.post2

* Updates regarding version upgrades of libraries that this package depends on.

## 0.0.35.post1

* Added top-level exports, which allow classes to be imported from the top level of their package.

## 0.0.35

* The required Python version has been changed to 3.12 or later. This change makes it easier to interoperate with Datetime data in frontends.
* Added setOffset, setStartAfter, setEndBefore, setLimit method to QueryBuilder and RawQueryBuilder.

## 0.0.34.post1

* Fixed a bug in the SingleSort object that caused sorting to fail when v_type was EnumValueType.datetime_.

## 0.0.34

* In search queries, sortObj is no longer required when using offset, startAfter, or endBefore. If not specified, the queries will be processed in the order they were added to the database.
* The getAll query now supports offset, startAfter, endBefore, and limit, making it easier to implement paging within a collection.
* Fixed an error that occurred when specifying sortObj in getAll.
* Fixed bug that caused sorting to be disabled when returnData was true in delete and update query.

## 0.0.33

* The searchOne query has been added, which works quickly when searching for only one item. 
* The removeCollection query has been added.
* Fixed a bug in the clearAdd function where only clearing would be performed if the serial key was invalid. This change may affect past queries, so if any of your failing queries(version less than 6) have this, use a clear query to fix it.
* Updated readme and test.
* Refactored RawQueryBuilder to match the variable ordering to the Dart version and to make input types stricter.

## 0.0.32

* Security fixes. This is important, so please update if you are running an older version.
* Logging on the app has been changed to be handled using the default [logging](https://docs.python.org/ja/3/library/logging.html). The method for obtaining logs may change, so please refer to the logging explanation as necessary.
* Added findCollection and removeCollection method to DeltaTraceDataBase class.
* The name option has been added to the addListener and removeListener methods of the DeltaTraceDataBase and Collection classes.
* When executing listeners for the DeltaTraceDataBase class and Collection class, if an error occurs in the callback, processing will stop there. This has been changed so that subsequent processing can continue even if an error occurs during the callback.
* Fixed a bug that caused transaction queries to not work correctly under certain conditions.
* The collectionToDict method of the deltaTraceDatabase class has been modified to return null if a non-existent collection is specified.
* Added explanatory text for QueryBuilder and RawQueryBuilder.

## 0.0.31

* The QueryResult class now has a target parameter, which is set to the target at the time the query was issued, making debugging a bit easier.

## 0.0.30.post1

* To improve data consistency when saving, RLock has been extended to the entire DeltaTraceDatabase, excluding ineffective methods such as raw.

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
