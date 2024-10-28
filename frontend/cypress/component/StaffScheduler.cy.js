import React from 'react';
import StaffScheduler from '../../src/StaffScheduler';
import { mount } from 'cypress/react';

describe('StaffScheduler Component Tests', () => {
  beforeEach(() => {
    cy.intercept('GET', 'http://127.0.0.1:5000/schedule/staff_schedules?staff_id=140002', {
      fixture: 'ownSchedule.json'
    }).as('getOwnSchedule');
    cy.intercept('GET', 'http://127.0.0.1:5000/schedule/team_schedules?staff_id=140002', {
      fixture: 'teamSchedule.json'
    }).as('getTeamSchedule');
  });

  it('should render the StaffScheduler component', () => {
    mount(<StaffScheduler />);
    cy.get('#scheduler').should('exist');
  });

  it('should fetch and display own schedule', () => {
    mount(<StaffScheduler />);
    cy.wait('@getOwnSchedule');
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });

  it('should switch to Team Schedule and display team schedule', () => {
    mount(<StaffScheduler />);
    cy.wait('@getTeamSchedule');
    cy.get('.dx-radiobutton').contains('Team Schedule').click();
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });

  it('should display correct AM and PM counts for Team Schedule', () => {
    mount(<StaffScheduler />);
    cy.wait('@getTeamSchedule');
    cy.get('.dx-radiobutton').contains('Team Schedule').click();
    cy.get('.ppl_count').should('contain.text', 'AM Count');
    cy.get('.ppl_count').should('contain.text', 'PM Count');
  });

  it('should change view to Week and display schedule', () => {
    mount(<StaffScheduler />);
    cy.get('.dx-scheduler-navigator-caption').click();
    cy.get('.dx-button-content').contains('Day').click();
    cy.get('.dx-list-item-content').contains('Week').click();
    cy.get('.dx-scheduler-appointment').should('have.length.greaterThan', 0);
  });
});