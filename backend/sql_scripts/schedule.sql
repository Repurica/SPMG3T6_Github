DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    Staff_ID INT NOT NULL,  -- Staff ID for staff
    Starting_Date DATE NOT NULL, -- starting date of WFH arrangement
    End_Date DATE, -- end date of WFH arrangement

    Monday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Tuesday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Wednesday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Thursday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Friday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Saturday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    Sunday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null



    PRIMARY KEY (Staff_ID,Starting_Date,End_Date) -- composite primary key to uniquely identify schedule based on date & am/pm
);