DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    Schedule_ID PRIMARY KEY INT NOT NULL, --Schedule ID for staff
    Staff_ID INT NOT NULL,  -- Staff ID for staff
    Date DATE NOT NULL,  -- Date of WFH arrangement
    Timing VARCHAR(50) NOT NULL -- AM/PM/Whole day/in-office
);