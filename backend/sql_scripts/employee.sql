DROP TABLE IF EXISTS Employee

CREATE TABLE Employee (
    Staff_ID INT PRIMARY KEY,  -- Staff ID for staff
    Staff_FName VARCHAR(50) NOT NULL,  -- First Name
    Staff_LName VARCHAR(50) NOT NULL,  -- Last Name
    Dept VARCHAR(50) NOT NULL,  -- Department staff belongs to
    Position VARCHAR(50) NOT NULL,  -- Position in the organization
    Country VARCHAR(50) NOT NULL,  -- Country located
    Email VARCHAR(50) NOT NULL,  -- Email Address
    Reporting_Manager INT,  -- Staff_ID of reporting manager
    Role INT NOT NULL,  -- Role of the user in the system
    CONSTRAINT fk_reporting_manager FOREIGN KEY (Reporting_Manager) REFERENCES Employee(Staff_ID),  -- Foreign Key referencing Staff_ID
    CONSTRAINT chk_role CHECK (Role IN (1, 2, 3))  -- Role should be HR(1), Staff(2), Manager(3)
);

