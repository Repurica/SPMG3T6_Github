import React from 'react';
import OwnRequests from '../../src/OwnRequests';
import { mount } from 'cypress/react18';


describe('OwnRequests Component', () => {
    beforeEach(() => {
        cy.intercept('POST', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/application/get_all_requests_staff', {
            fixture: 'ownRequests.json'
        }).as('getRequests');
        
        // cy.intercept('POST', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/withdrawals/staff_store_withdrawal', {
        //     statusCode: 200,
        //     body: { success: true }
        // }).as('withdrawRequest');
        mount(<OwnRequests />);
        cy.mount(<OwnRequests />);
    });

    it('should display loading initially', () => {
        cy.contains('Loading...').should('be.visible');
    });

    it('should display requests after loading', () => {
        cy.wait('@getRequests');
        cy.get('.request-card').should('have.length', 3); // Assuming 3 items per page
    });

    it('should filter requests by status', () => {
        cy.wait('@getRequests');
        cy.get('#status-filter').select('approved');
        cy.get('.request-card').each(($el) => {
            cy.wrap($el).find('.detail-text').contains('Status:').parent().contains('Approved').should('exist');
        });
    });

    it('should open and close withdrawal modal', () => {
        cy.wait('@getRequests');
        cy.get('.withdraw-button').first().click();
        cy.get('.modal-content').should('be.visible');
        cy.get('.close-btn').click();
        cy.get('.modal-content').should('not.exist');
    });

    // it('should handle withdrawal request', () => {
    //     cy.wait('@getRequests');
    //     cy.get('.withdraw-button').first().click();
    //     cy.get('.modal').should('be.visible');
    //     cy.get('textarea').type('Reason for withdrawal');
    //     cy.get('.apply-button').click();
    //     cy.wait('@withdrawRequest');
    //     cy.contains('Dates Withdrawn!').should('be.visible');
    // });

    it('should navigate through pages', () => {
        cy.wait('@getRequests');
        cy.get('.navigate').contains('Next').click();
        cy.get('.page-info').should('contain', '2 of');
        cy.get('.navigate').contains('Previous').click();
        cy.get('.page-info').should('contain', '1 of');
    });
});