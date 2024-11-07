import React from 'react';
import { mount } from 'cypress/react';
import ApplicationForm from '../../src/ApplicationForm';

describe('ApplicationForm Component Tests', () => {
  beforeEach(() => {
    cy.intercept('POST', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/application/available_dates', {
      statusCode: 200,
      body: { results: [] },
    }).as('fetchAvailableDates');

    cy.intercept('POST', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/application/store_application', {
      statusCode: 200,
      body: { message: 'Success' },
    }).as('storeApplication');

    mount(<ApplicationForm />);
  });

  it('should render the form with initial state', () => {
    cy.get('h1').contains('WFH Application Form');
    cy.get('input[type="radio"][value="recurring"]').should('exist');
    cy.get('input[type="radio"][value="ad_hoc"]').should('exist');
    cy.get('input[placeholder="Select a start date"]').should('exist');
    cy.get('textarea[placeholder="Enter your reason for WFH application here. Max 300 characters"]').should('exist');
    cy.get('button[type="submit"]').contains('Submit');
  });

  it('should select ad hoc and set start date', () => {
    cy.get('input[type="radio"][value="ad_hoc"]').check();
    cy.get('input[placeholder="Select a start date"]').click();
    cy.get('.react-datepicker__day--001').first().click(); // Select the first day of the month
    cy.get('input[placeholder="Select a start date"]').should('have.value', '11/01/2024');
  });

  it('should show error if reason is empty on submit', () => {
    cy.get('input[type="radio"][value="ad_hoc"]').check();
    cy.get('input[placeholder="Select a start date"]').click();
    cy.get('.react-datepicker__day--001').first().click();
    cy.get('button[type="submit"]').click();
    cy.on('window:alert', (text) => {
      expect(text).to.contains('Please enter a non-empty reason for request');
    });
  });

  it('should submit the form successfully', () => {
    cy.get('input[type="radio"][value="ad_hoc"]').check();
    cy.get('input[placeholder="Select a start date"]').click();
    cy.get('.react-datepicker__day--001').first().click();
    cy.get('textarea').type('Test reason');
    cy.get('input[type="radio"][value="full_day"]').check();
    cy.get('button[type="submit"]').click();
    cy.wait('@storeApplication');
    cy.get('.modal').contains('Form submitted successfully!');
  });
});