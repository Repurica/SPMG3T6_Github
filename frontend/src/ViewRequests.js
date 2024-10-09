import React, { useState } from 'react';
import './ViewRequests.css'; // Import the CSS file
import { FaInbox } from 'react-icons/fa'; // Import the inbox icon

const itemsPerPage = 3;

const data = {
    "1": {
        "created_at": "2024-10-06",
        "end_date": "2024-10-10",
        "reason": "family matters",
        "request_type": "recurring",
        "staff_fullname": "Susan Goh",
        "staff_id": 140002,
        "starting_date": "2024-09-26",
        "timing": "AM",
        "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    },
    "2": {
        "created_at": "2024-10-06",
        "end_date": "2024-10-10",
        "reason": "family matters",
        "request_type": "recurring",
        "staff_fullname": "Susan Goh",
        "staff_id": 140002,
        "starting_date": "2024-09-26",
        "timing": "AM",
        "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    },
    "3": {
        "created_at": "2024-10-06",
        "end_date": "2024-10-10",
        "reason": "family matters",
        "request_type": "recurring",
        "staff_fullname": "Susan Goh",
        "staff_id": 140002,
        "starting_date": "2024-09-26",
        "timing": "AM",
        "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    },
    "4": {
        "created_at": "2024-10-06",
        "end_date": "2024-10-10",
        "reason": "family matters",
        "request_type": "recurring",
        "staff_fullname": "Susan Goh",
        "staff_id": 140002,
        "starting_date": "2024-09-26",
        "timing": "AM",
        "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    },
    "5": {
        "created_at": "2024-10-06",
        "end_date": "2024-10-10",
        "reason": "family matters",
        "request_type": "ad hoc",
        "staff_fullname": "test",
        "staff_id": 123,
        "starting_date": "2024-09-26",
        "timing": "AM",
        "reason": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    }
    // Add more entries here
};

const handleApprove = () => {
    // Logic for approving a request
};

const handleReject = () => {
    // Logic for rejecting a request
};

function ViewRequests() {
    const [currentPage, setCurrentPage] = useState(1);
    const totalItems = Object.keys(data).length; // Total number of requests
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    const getCurrentItems = () => {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return Object.entries(data).slice(startIndex, endIndex);
    };

    const currentItems = getCurrentItems();

    return (
        <div className="container">
            <div className="header">
                <h1>Staff WFH Requests</h1>
                <div className="inbox">
                    <FaInbox className="inbox-icon" />
                    <span className="request-count">{totalItems}</span>
                </div>
            </div>
            <div>
                {currentItems.map(([key, item]) => (
                    <div key={key} className="request-card">
                        <div className="button-container">
                            <button onClick={() => handleApprove(key)} className="action-button approve">Approve</button>
                            <button onClick={() => handleReject(key)} className="action-button reject">Reject</button>
                        </div>
                        <p><strong>Application Date:</strong> {item.created_at}</p>
                        <p><strong>Name:</strong> {item.staff_fullname}</p>
                        <p><strong>Position ID:</strong> {item.staff_id}</p>
                        {item.request_type === 'ad hoc' ? (
                            <p><strong>Start Date:</strong> {item.starting_date}</p>
                        ) : (
                            <p>
                                <strong>Start Date:</strong> {item.starting_date} &nbsp;&nbsp;
                                <strong>End Date:</strong> {item.end_date}
                            </p>
                        )}
                        <p><strong>Timing:</strong> {item.timing}</p>
                        <p><strong>Reason:</strong> {item.reason}</p>
                    </div>
                ))}
            </div>
            <div className="pagination">
                <button className="navigate" onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1}>
                    Previous
                </button>
                <span className="page-info">{currentPage} of {totalPages}</span>
                <button className="navigate" onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} disabled={currentPage === totalPages}>
                    Next
                </button>
            </div>
        </div>
    );
}

export default ViewRequests;
