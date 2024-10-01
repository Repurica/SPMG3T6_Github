DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee (
    staff_id INT PRIMARY KEY,  -- Staff ID for staff
    staff_fname VARCHAR(50) NOT NULL,  -- First Name
    staff_lname VARCHAR(50) NOT NULL,  -- Last Name
    dept VARCHAR(50) NOT NULL,  -- Department staff belongs to
    position VARCHAR(50) NOT NULL,  -- Position in the organization
    country VARCHAR(50) NOT NULL,  -- Country located
    email VARCHAR(50) NOT NULL,  -- Email Address
    reporting_manager INT,  -- Staff_ID of reporting manager
    role INT NOT NULL,  -- Role of the user in the system
    CONSTRAINT fk_reporting_manager FOREIGN KEY (reporting_manager) REFERENCES employee(staff_id),  -- Foreign Key referencing Staff_ID
    CONSTRAINT chk_role CHECK (role IN (1, 2, 3))  -- Role should be HR(1), Staff(2), Manager(3)
);

