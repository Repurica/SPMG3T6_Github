import React from 'react';
import StaffScheduler from '../../src/StaffScheduler';
import { mount } from 'cypress/react';

describe('StaffScheduler Component Tests', () => {
  beforeEach(() => {
    // const date = new Date('2024-10-15T09:00:00+08:00');
    // cy.clock(date.getTime());
    sessionStorage.setItem('id', '140002');
    sessionStorage.setItem('role', '1');
    cy.intercept('GET', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/schedule/staff_schedules?staff_id=140002', {
      fixture: 'ownSchedule.json'
    }).as('getOwnSchedule');
    cy.intercept('GET', 'http://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/schedule/team_schedules?staff_id=140002', {
      fixture: 'teamSchedule.json'
    }).as('getTeamSchedule');
    mount(<StaffScheduler />);
    cy.get('.dx-button-text').then(function checkDate($caption) {
      if (!$caption.text().includes('15 October 2024')) {
        cy.get('.dx-icon-chevronprev').click();
        cy.get('.dx-button-text').then(checkDate); // recursively check the date again
      }
    });

  });

  it('should render the StaffScheduler component', () => {
    cy.get('#scheduler').should('exist');
  });

  it('should fetch and display own schedule', () => {
    cy.wait('@getOwnSchedule');
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });

  it('should switch to Team Schedule and display team schedule', () => {
    cy.wait('@getTeamSchedule');
    cy.get('.dx-radiobutton').contains('Team Schedule').click();
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });

  it('should display correct AM and PM counts for Team Schedule', () => {
    cy.wait('@getTeamSchedule');
    cy.get('.dx-radiobutton').contains('Team Schedule').click();
    cy.get('.ppl_count').should('contain.text', 'AM Count');
    cy.get('.ppl_count').should('contain.text', 'PM Count');
  });

  it('should change view to Week and display schedule', () => {
    cy.get('.dx-scheduler-navigator-caption').click();
    cy.get('.dx-button-content').contains('Day').click();
    cy.get('.dx-list-item-content').contains('Week').click();
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });


});
