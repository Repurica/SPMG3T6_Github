import React, { useState, useEffect } from 'react';
import './ViewRequests.css'; // Import the CSS file
import { FaInbox } from 'react-icons/fa'; // Import the inbox icon
import DetailedRequestModal from './DetailedRequestModal';
import { fetchWithRetry } from './FetchWithRetry';

function ViewRequests() {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null)
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [reason, setReason] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    
    const test_manager_id = 140894

    const itemsPerPage = 3;


    const totalItems = Object.keys(data).length; // Total number of requests
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    
    const getCurrentItems = () => {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return Object.entries(data).slice(startIndex, endIndex);
    };

    const currentItems = getCurrentItems();






    const handleCardClick = (key) => {
        console.log(`Card with key ${key} clicked`);
        // Add logic for card click, such as opening a detailed view or modal
        const item = currentItems.find(([k]) => k === key)[1];
        setSelectedItem(item);
        setIsModalOpen(true);
    
    };
    
    const handleCardHover = (key, isHovering) => {

    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedItem(null);
        setReason("");
      };
    
      const handleAccept = () => {
        console.log("Accepted:", selectedItem);
        console.log("Reason:", reason);
        handleCloseModal();
      };
    
      const handleReject = () => {
        console.log("Rejected:", selectedItem);
        console.log("Reason:", reason);
        handleCloseModal();
      }



    // fetch data from application.py
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetchWithRetry('http://localhost:5000/application/retrieve_pending_requests', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Send JSON data
                    },
                    body: JSON.stringify({ manager_id: test_manager_id }), // Data to be sent on page load
                }, 3, 2000); // 3 retries with a 1 second delay between retries

                const result = await response.json();
                setData(result);
                setError(null); // Clear any previous errors
            } catch (err) {
                console.log(err.message);
                setError(err.message); // Display error message
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
                        <p class="staff-name">{item.staff_fullname}</p>
                        <p class="detail-text"><span class="detail-label">Position ID:</span> {item.staff_id}</p>
                        <p class="detail-text">
                            <span class="detail-label">Application Date:</span> {item.created_at} &nbsp;&nbsp;
                            {item.request_type === 'ad_hoc' ? (
                                <span class="detail-label">Type: <span class="detail-text">Ad Hoc</span></span> 
                            ) : (
                                <span class="detail-label">Type: <span class="detail-text">Recurring</span></span>
                            )}
                        </p>

                        {item.request_type === 'ad_hoc' ? (
                            <p class="detail-text"><span class="detail-label">Start Date:</span> {item.starting_date}</p>
                        ) : (
                            <p class="detail-text">
                                <span class="detail-label">Start Date:</span> {item.starting_date} &nbsp;&nbsp;
                                <span class="detail-label">End Date:</span> {item.end_date}
                            </p>
                        )}

                        {item.timing === "full_day" ? (
                            <p class="detail-text"><span class="detail-label">Timing:</span> Full Day</p>
                        ) : (
                            <p class="detail-text"><span class="detail-label">Timing:</span> {item.timing}</p>
                        )}                    
                        </div>
                ))}
                      <DetailedRequestModal 
                        isOpen={isModalOpen}
                        selectedItem={selectedItem}
                        reason={reason}
                        setReason={setReason}
                        handleAccept={handleAccept}
                        handleReject={handleReject}
                        handleClose={handleCloseModal}
                        />
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
