# sql_manager

Roadmap
-------- Phase 1
* Finish difference engine
* Implement testing
* Implement 'additive' database updates
-------- Phase 1 complete

-------- Phase 2
* Identify a way to run update scripts so things like drops and field structure changes can be executed by the simple process without undesired data loss:
    Eg. if i want to drop a table but move a protion of data beforehand, i should be able to write a small script to move the data before the drop or change is implemented.

Sequence of events:
* action additions
* action data moves
* action data changes
* action updates
* action drops
* cleanup temp_ dbs, tables and fields