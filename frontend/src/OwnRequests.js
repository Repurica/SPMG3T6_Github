import React, { useState, useEffect } from 'react';
import './OwnRequests.css'; // Import the CSS file
import { FaInbox } from 'react-icons/fa'; // Import the inbox icon
import { fetchWithRetry } from './FetchWithRetry';
import WithdrawalModal from './WithdrawalModal';
import ApplicationNotificationModal from './ApplicationNotificationModal';


function OwnRequests() {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null)
    const [currentPage, setCurrentPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState("all");
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [selectedApplication, setApplication] = useState(null);
    const [reason, setReason] = useState("");
    const [notification, setNotification] = useState('');



    // 140002 for view testing
    const staff_id = 140002
    //const staff_id = 140004

    const itemsPerPage = 3;


    let totalItems = Object.keys(data).length; // Total number of requests
    let totalPages = Math.ceil(totalItems / itemsPerPage);

    
    const getFilteredData = () => {
        if (filter === "all") {
            totalItems = Object.keys(data).length
            totalPages = Math.ceil(totalItems / itemsPerPage);
            return data;
        }
        let filterItems =  Object.fromEntries(
            Object.entries(data).filter(([key, item]) => item.status === filter)
        );
        totalItems = Object.keys(filterItems).length
        totalPages = Math.ceil(totalItems / itemsPerPage);
        return filterItems
    };

    const getCurrentItems = () => {
        const filteredData = getFilteredData();
        if (totalPages === 0){
            totalPages = 1
        }
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return Object.entries(filteredData).slice(startIndex, endIndex);
    };

    const currentItems = getCurrentItems();

    
    const handleCardHover = (key, isHovering) => {

    };

    const WithdrawButton = ({app_status, valid, selected_item, selected_application}) => {
        if ((app_status === 'pending')){
            return ( 
                <div className="button-container">
                    <button onClick={() => handleWithdraw(selected_item, selected_application)} className="withdraw-button">Withdraw</button>
                </div>
            )
        }
        else if (app_status === 'approved' && (valid === 'valid')){
            return ( 
                <div className="button-container">
                    <button onClick={() => handleWithdraw(selected_item, selected_application)} className="withdraw-button">Withdraw</button>
                </div>
            )
        }
        else if (app_status === 'approved' && (valid === 'invalid')){
            return ( 
                <div className="button-container">
                    <button onClick={() => handleWithdraw(selected_item, selected_application)} className="withdraw-button" disabled = {true}>Withdraw</button>
                </div>
            )

        }
    }
    // to note: if applied_dates after update in backend = 0, set status of application to withdrawn
    const handleWithdraw = (selected_item, selected_application) => {
        setSelectedItem(selected_item);
        setApplication(selected_application)
        setIsModalOpen(true);

    }

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedItem(null);
        setApplication(null);
        setReason("");
      };

    //for after modal after approve/reject
    const handleClose = () => {
        window.location.reload(); // Refresh Page
      };

    
    const handleApply = async (dateStatus) => {
        let trueDates = Object.keys(dateStatus).filter(date => dateStatus[date])
        let toSend = { 
            "staff_id" : staff_id,
            "application_id" : Number(selectedApplication),
            "reason" : reason,
            "status_of_request" : selectedItem.status,
            "withdrawn_dates" : {"dates":trueDates},
         }
         console.log(toSend)         
         try {
            const response = await fetch('http://localhost:5000/withdrawals/staff_store_withdrawal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(toSend),
            });
    
            if (response.ok) {
                const jsonResponse = await response.json();
                console.log('Success:', jsonResponse);
                if (selectedItem.status === 'pending')
                setNotification(`Dates Withdrawn!`);
                else {
                    setNotification(`Request Sent!`)
                }
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }

    }

    // fetch data from application.py
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await fetchWithRetry('http://localhost:5000/application/get_all_requests_staff', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Send JSON data
                    },
                    body: JSON.stringify({ staff_id: staff_id }), // Data to be sent on page load
                }, 3, 2000); // 3 retries with a 1 second delay between retries

                const result = await response.json();
                setData(result);
                console.log(result)
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
                <h1>My WFH Requests</h1>
                <div className="inbox">
                    <FaInbox className="inbox-icon" />
                    <span className="request-count">{totalItems}</span>
                </div>
            </div>
            {/* Filter Section */}
            <div className="filter-section">
                <label htmlFor="status-filter">Filter by status:</label>
                <select
                    id="status-filter"
                    value={filter}
                    onChange={(e) => {
                        setFilter(e.target.value);
                        setCurrentPage(1); // Reset to first page on filter change
                    }}
                >
                    <option value="all">All</option>
                    <option value="pending">Pending</option>
                    <option value="approved">Approved</option>
                    <option value="rejected">Rejected</option>
                    <option value="withdrawn">Withdrawn</option>
                </select>
            </div>
            <div>
                {currentItems.map(([key, item]) => (
                    <div key={key} className="request-card"
                    onMouseEnter={() => handleCardHover(key, true)} 
                    onMouseLeave={() => handleCardHover(key, false)}>
                        <WithdrawButton app_status={item.status} valid = {item.validity_of_withdrawal} selected_item = {item} selected_application = {key}></WithdrawButton>
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
                        <p class="detail-text"><span class="detail-label">Reason for request:</span> {item.reason}</p>
                        <p class="detail-text">
                            {item.status === 'pending' ? (
                                <span class="detail-label">Status: <span class="detail-text" style={{color: "blue"}}>Pending</span></span> 
                            ) : 
                            item.status === 'withdrawn' ? (
                                <span class="detail-label">Status: <span class="detail-text" style={{color: "grey"}}>Withdrawn</span></span> 
                            ) : 
                            item.status === 'approved' ? (
                                <span class="detail-label">Status: <span class="detail-text" style={{color: "green"}}>Approved</span></span> 
                            ) : (
                                <span class="detail-label">Status: <span class="detail-text" style={{color: "red"}}>Rejected</span></span> 
                            )}
                        </p>
                        {item.status === "approved" ? (
                            <p class="detail-text"><span class="detail-label">Reason for approval:</span> {item.outcome_reason}</p>
                        ) : 
                        item.status === 'rejected' ? (
                            <p class="detail-text"><span class="detail-label">Reason for rejection:</span> {item.outcome_reason}</p>
                        ) : null}                    
                        </div>
                ))}

            </div>
            <WithdrawalModal 
                        isOpen={isModalOpen}
                        selectedItem={selectedItem}
                        reason={reason}
                        setReason={setReason}
                        handleApply={handleApply}
                        handleClose={handleCloseModal}
                        />

            
            <div className="pagination">
                <button className="navigate" onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1}>
                    Previous
                </button>
                <span className="page-info">{currentPage} of {totalPages}</span>
                <button className="navigate" onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} disabled={currentPage === totalPages}>
                    Next
                </button>
            </div>
            <ApplicationNotificationModal message={notification} onClose={handleClose} /> 


        </div>
    );
}

export default OwnRequests;
