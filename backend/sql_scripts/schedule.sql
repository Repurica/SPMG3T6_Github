DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    schedule_id INT NOT NULL PRIMARY KEY, -- unique schedule ID
    staff_id INT NOT NULL,  -- Staff ID for staff
    starting_date DATE NOT NULL, -- starting date of WFH arrangement
    end_date DATE, -- end date of WFH arrangement

    monday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    tuesday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    wednesday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    thursday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    friday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    saturday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null
    sunday VARCHAR(50) NOT NULL, -- AM/PM/Whole day/in-office/Null



);