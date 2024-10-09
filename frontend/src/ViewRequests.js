import React, { useState, useEffect } from 'react';
import './ViewRequests.css'; // Import the CSS file
import { FaInbox } from 'react-icons/fa'; // Import the inbox icon


const handleCardClick = (key) => {
    console.log(`Card with key ${key} clicked`);
    // Add logic for card click, such as opening a detailed view or modal
};

const handleCardHover = (key, isHovering) => {

};

const handleApprove = () => {
    // Logic for approving a request
};

const handleReject = () => {
    // Logic for rejecting a request
};

function ViewRequests() {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null)

    const test_manager_id = 140894

    const itemsPerPage = 3;


    const [currentPage, setCurrentPage] = useState(1);
    const totalItems = Object.keys(data).length; // Total number of requests
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    const getCurrentItems = () => {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return Object.entries(data).slice(startIndex, endIndex);
    };

    const currentItems = getCurrentItems();

    // fetch data from application.py
    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await fetch('http://localhost:5000/application/retrieve_pending_requests', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json', // Send JSON data
            },
            body: JSON.stringify({ manager_id: test_manager_id }), // Data to be sent on page load
            });

            if (!response.ok) {
            throw new Error('Failed to fetch data');

            }

            const result = await response.json();
            setData(result);
            setError(null)
        } catch (err) {
            console.log(err.message);
            // display error message for now
            setError(err.message)
        }

        };

        fetchData();
    }, []);
    console.log(data)


    if (error){
        return (<h1>Error occured fetching data.</h1>)
      }
      else {
    
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
                    <div key={key} className="request-card"
                    onClick={() => handleCardClick(key)}
                    onMouseEnter={() => handleCardHover(key, true)} 
                    onMouseLeave={() => handleCardHover(key, false)}>
                        <div className="button-container">
                            <button onClick={() => handleApprove(key)} className="action-button approve">Approve</button>
                            <button onClick={() => handleReject(key)} className="action-button reject">Reject</button>
                        </div>
                        <p><strong>Application Date:</strong> {item.created_at}</p>
                        <p><strong>Name:</strong> {item.staff_fullname}</p>
                        <p><strong>Position ID:</strong> {item.staff_id}</p>
                        {item.request_type === 'ad_hoc' ? (
                            <p><strong>Start Date:</strong> {item.starting_date}</p>
                        ) : (
                            <p>
                                <strong>Start Date:</strong> {item.starting_date} &nbsp;&nbsp;
                                <strong>End Date:</strong> {item.end_date}
                            </p>
                        )}
                        {item.timing === "full_day" ? (
                            <p><strong>Timing:</strong> Full Day</p>
                        ) : (
                            <p><strong>Timing:</strong> {item.timing}</p>

                        )}
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
}}

export default ViewRequests;
