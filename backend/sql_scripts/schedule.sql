DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    Staff_ID INT NOT NULL,  -- Staff ID for staff
    Date DATE NOT NULL,  -- Date of WFH arrangement
    Timing VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office
    PRIMARY KEY (Staff_ID,Date) -- composite primary key to uniquely identify schedule based on date & am/pm
);