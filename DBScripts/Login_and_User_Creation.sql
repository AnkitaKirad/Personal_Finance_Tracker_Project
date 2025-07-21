/*
=============================================================
Create Login and User
=============================================================
Script Purpose:
    This script creates a new Login named 'etl_user'. 
    Additionally, the script creates the user 'etl_user' for same login in the database 'PersonalFinanceDW'
    with the premissions SELECT, INSERT, UPDATE.
	
WARNING:
    Don't give the premission for the user directly on the Database in the real world usecase it should always have only schema or table level premissions
*/


--Creating SQL Server Authentication Login to the server
USE [master]
CREATE LOGIN etl_user WITH PASSWORD = 'YourPassword';

--Creating User for the login created before
USE [PersonalFinanceDW];
CREATE USER etl_user FOR LOGIN etl_user;

--Granting premissions to use user
USE [PersonalFinanceDW];
GRANT SELECT, INSERT, UPDATE ON DATABASE::[PersonalFinanceDW] TO etl_user;
