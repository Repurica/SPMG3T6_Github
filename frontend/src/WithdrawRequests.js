import React, { useState, useEffect } from 'react';
import './ViewRequests.css'; // Import the CSS file
import { FaInbox } from 'react-icons/fa'; // Import the inbox icon
import DetailedWithdrawModal from './DetailedWithdrawModal';
import { fetchWithRetry } from './FetchWithRetry';
import ApplicationNotificationModal from './ApplicationNotificationModal';

function WithdrawRequests() {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null)
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [reason, setReason] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [notification, setNotification] = useState('');

    const test_manager_id = 140894
    //const test_manager_id = 180001


    const itemsPerPage = 3;


    const totalItems = Object.keys(data).length; // Total number of requests
    let totalPages = Math.ceil(totalItems / itemsPerPage);

    
    const getCurrentItems = () => {
        if (totalPages === 0){
            totalPages = 1
        }
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return Object.entries(data).slice(startIndex, endIndex);
    };

    const currentItems = getCurrentItems();

    //for after modal after approve/reject
    const handleClose = () => {
        window.location.reload(); // Refresh Page
      };
    



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
    
      const handleAccept = async () => {
        if (reason.trim() === ''){
            alert('Enter a reason for approval!')
        }
        else {
            console.log("Accepted:", selectedItem);
            console.log("Reason:", reason);
    
            let toSend = { 
                "outcome_status": "approved",
                "outcome_reason": reason,
                "withdrawal_id": selectedItem.withdrawal_id   
             }         
             try {
                const response = await fetch('http://localhost:5000/withdrawals/manager_approve_reject_withdrawal', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(toSend),
                });
        
                if (response.ok) {
                    const jsonResponse = await response.json();
                    console.log('Success:', jsonResponse);
                    setNotification(`Request Approved!`);
                } else {
                    console.error('Error:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }


        }
      };
    
      const handleReject = async() => {
        if (reason.trim() === ''){
            alert('Enter a reason for rejection!')
        }
        else{
            let toSend = { 
                "outcome_status": "rejected",
                "outcome_reason": reason,
                "withdrawal_id": selectedItem.withdrawal_id   
             }          
             try {
                const response = await fetch('http://localhost:5000/withdrawals/manager_approve_reject_withdrawal', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(toSend),
                });
        
                if (response.ok) {
                    const jsonResponse = await response.json();
                    console.log('Success:', jsonResponse);
                    setNotification(`Request Rejected!`);
                } else {
                    console.error('Error:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }


    
        }
      }



    // fetch data from application.py
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await fetchWithRetry('http://localhost:5000/withdrawals/retrieve_withdrawals', {
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
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        }, []);

    if (loading) {
        return <h1>Loading...</h1>;
    }

    if (error){
        return (<h1>Error occured fetching data.</h1>)
      }
    
    return (
        <div className="container">
            <div className="header">
                <h1>Staff Withdrawal Requests</h1>
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
                        <p class="staff-name">{item.staff_name}</p>
                        <p class="detail-text"><span class="detail-label">Staff ID:</span> {item.staff_id}</p>
                        <p class="detail-text"><span class="detail-label">Dates to Withdraw:</span> {item.withdrawn_dates.dates.join(", ")}</p>

                        {item.wfh_timing === "full_day" ? (
                            <p class="detail-text"><span class="detail-label">Timing:</span> Full Day</p>
                        ) : (
                            <p class="detail-text"><span class="detail-label">Timing:</span> {item.wfh_timing}</p>
                        )}                    
                        </div>
                ))}
                      <DetailedWithdrawModal 
                        isOpen={isModalOpen}
                        selectedItem={selectedItem}
                        reason={reason}
                        setReason={setReason}
                        handleAccept={handleAccept}
                        handleReject={handleReject}
                        handleClose={handleCloseModal}
                        />
            </div>
            <ApplicationNotificationModal message={notification} onClose={handleClose} /> 
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

export default WithdrawRequests;