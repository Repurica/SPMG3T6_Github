import React from 'react';
import { mount } from 'cypress/react';
import ViewRequests from '../../src/ViewRequests';

describe('ViewRequests Component', () => {
    let requests;

    beforeEach(() => {
        cy.fixture('viewRequests.json').then((data) => {
            requests = data;
        });

        cy.intercept('POST', 'http://localhost:5000/application/retrieve_pending_requests', {
            fixture: 'viewRequests.json',
        }).as('retrieveRequests');
        mount(<ViewRequests />);
    });

    it('should display the correct number of requests', () => {
        cy.wait('@retrieveRequests');
        cy.get('.request-count').should('have.text', Object.keys(requests).length.toString());
    });

    it('should display the correct request details', () => {
        cy.wait('@retrieveRequests');
        cy.get('.request-card').each((card, index) => {
            const request = Object.values(requests)[index];
            cy.wrap(card).within(() => {
                cy.get('.staff-name').should('have.text', request.staff_fullname);
                cy.get('.detail-text').contains('.detail-label', 'Staff ID:').parent().should('contain.text', request.staff_id);
                cy.get('.detail-text').contains('.detail-label', 'Application Date:').parent().should('contain.text', request.created_at);
                cy.get('.detail-text').contains('.detail-label', 'Type:').parent().should('contain.text', request.request_type === 'ad_hoc' ? 'Ad Hoc' : 'Recurring');
                if (request.request_type === 'ad_hoc') {
                    cy.get('.detail-text').contains('.detail-label', 'Start Date:').parent().should('have.text', `Start Date: ${request.starting_date}`);
                } else {
                    cy.get('.detail-text').contains('.detail-label', 'Start Date:').parent().should('contain.text', request.starting_date);
                    cy.get('.detail-text').contains('.detail-label', 'End Date:').parent().should('contain.text', request.end_date);
                }
                cy.get('.detail-text').contains('.detail-label', 'Timing:').parent().should('have.text', `Timing: ${request.timing === 'full_day' ? 'Full Day' : request.timing}`);});
        });
    });

    it('should open the detailed request modal on card click', () => {
        cy.wait('@retrieveRequests');
        cy.get('.request-card').first().click();
        cy.get('.modal-content').should('be.visible');
    });

    it('should display the correct details in the modal', () => {
        cy.wait('@retrieveRequests');
        cy.get('.request-card').first().click();
        const request = Object.values(requests)[0];
        cy.get('.modal-content').within(() => {
            cy.get('p').contains('Staff Name:').parent().should('contain.text', request.staff_fullname);
            cy.get('p').contains('Position ID:').parent().should('contain.text', request.staff_id);
            cy.get('p').contains('Application Date:').parent().should('contain.text', request.created_at);
            cy.get('p').contains('Request Type:').parent().should('contain.text', request.request_type === 'ad_hoc' ? 'Ad Hoc' : 'Recurring');
            if (request.request_type === 'ad_hoc') {
                cy.get('p').contains('Start Date:').parent().should('contain.text', request.starting_date);
            } else {
                cy.get('p').contains('Start Date:').parent().should('contain.text', request.starting_date);
                cy.get('p').contains('End Date:').parent().should('contain.text', request.end_date);
            }
            cy.get('p').contains('Timing:').parent().should('contain.text', request.timing === 'full_day' ? 'Full Day' : request.timing);
            cy.get('.reason-box').contains('Reason for request:').parent().should('contain.text', request.reason);
        });
    });

    it('should paginate correctly', () => {
        cy.wait('@retrieveRequests');
        cy.get('.navigate').contains('Next').click();
        cy.get('.page-info').should('contain.text', '2');
        cy.get('.navigate').contains('Previous').click();
        cy.get('.page-info').should('contain.text', '1');
    });
});