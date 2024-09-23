DROP TABLE IF EXISTS application;

CREATE TABLE application (
    Application_ID INT PRIMARY KEY, --
    Request_Type VARCHAR(20), -- Ad hoc or recurring basis
    Starting_Date DATE NOT NULL, -- starting date of WFH arrangement
    End_Date DATE NOT NULL, -- end date of WFH arrangement
    Reason VARCHAR(1000) NOT NULL, -- reason for WFH arrangement
    Timing VARCHAR(50) NOT NULL, -- AM/PM/Whole day
    Staff_ID INT NOT NULL,  -- Staff ID for staff
    Status VARCHAR(50) NOT NULL, -- status of application (pending/approved/rejected)
    CONSTRAINT fk_reporting_manager FOREIGN KEY (Staff_ID) REFERENCES schedule(Staff_ID) -- foreign key referencing staff id in schedule table
); 