LOAD DATA INFILE 'C:/wamp64/tmp/employeenew.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role);