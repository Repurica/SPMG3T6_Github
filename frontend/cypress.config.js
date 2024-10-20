const { defineConfig } = require("cypress");

try {
  require('devextreme/dist/css/dx.material.blue.light.css');
} catch (error) {
  console.warn("Optional module 'devextreme/dist/css/dx.material.blue.light.css' not found. Continuing without it.");
}

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
