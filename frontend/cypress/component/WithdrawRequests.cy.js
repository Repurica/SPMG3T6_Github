import React from 'react';
import { mount } from 'cypress/react';
import WithdrawRequests from '../../src/WithdrawRequests';

describe('WithdrawRequests Component', () => {
    let requests;

    beforeEach(() => {
        cy.fixture('withdrawRequests.json').then((data) => {
            requests = data;
        });

        cy.intercept('POST', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/withdrawals/retrieve_withdrawals', {
            fixture: 'withdrawRequests.json',
        }).as('retrieveWithdrawRequests');
        mount(<WithdrawRequests />);
    });

    it('should display the correct number of requests', () => {
        cy.wait('@retrieveWithdrawRequests');
        cy.get('.request-count').should('have.text', Object.keys(requests).length.toString());
    });

    it('should display the correct request details', () => {
        cy.wait('@retrieveWithdrawRequests');
        cy.get('.request-card').each((card, index) => {
            const request = Object.values(requests)[index];
            cy.wrap(card).within(() => {
                cy.get('.staff-name').should('have.text', request.staff_name);
                cy.get('.detail-text').contains('.detail-label', 'Staff ID:').parent().should('contain.text', request.staff_id);
                cy.get('.detail-text').contains('.detail-label', 'Dates to Withdraw:').parent().should('contain.text', request.withdrawn_dates.dates.join(", "));
                cy.get('.detail-text').contains('.detail-label', 'Timing:').parent().should('have.text', `Timing: ${request.wfh_timing === 'full_day' ? 'Full Day' : request.wfh_timing}`);
            });
        });
    });

    it('should open the detailed request modal on card click', () => {
        cy.wait('@retrieveWithdrawRequests');
        cy.get('.request-card').first().click();
        cy.get('.modal-content').should('be.visible');
    });

    it('should display the correct details in the modal', () => {
        cy.wait('@retrieveWithdrawRequests');
        cy.get('.request-card').first().click();
        const request = Object.values(requests)[0];
        cy.get('.modal-content').within(() => {
            cy.get('p').contains('Staff Name:').parent().should('contain.text', request.staff_name);
            cy.get('p').contains('Staff ID:').parent().should('contain.text', request.staff_id);
            cy.get('p').contains('Dates to Withdraw:').parent().should('contain.text', request.withdrawn_dates.dates.join(", "));
            cy.get('p').contains('Timing:').parent().should('contain.text', request.wfh_timing === 'full_day' ? 'Full Day' : request.wfh_timing);
        });
    });

    it('should paginate correctly', () => {
        cy.wait('@retrieveWithdrawRequests');
        cy.get('.navigate').contains('Next').click();
        cy.get('.page-info').should('contain.text', '2');
        cy.get('.navigate').contains('Previous').click();
        cy.get('.page-info').should('contain.text', '1');
    });
});