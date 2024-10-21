describe('The Home Page', () => {
  it('successfully loads', () => {
    cy.visit('http://localhost:300')
  })
})


describe('The Application Form Page', () => {
  it('successfully loads', () => {
    cy.visit('http://localhost:3000/ApplicationForm')
  })
})


describe('The View Requests Page', () => {
  it('successfully loads', () => {
    cy.visit('http://localhost:3000/ViewRequests')
  })
})



describe('The Own Requests Page', () => {
  it('successfully loads', () => {
    cy.visit('http://localhost:3000/OwnRequests')
  })
})