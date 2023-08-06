/** @type {import('tailwindcss').Config} */

const { join } = require('path');

module.exports = {
  content: [
    join(__dirname, 'app/**/*.{html,js}'),
    join(__dirname, 'node_modules/flowbite/**/*.js'),
    // ".app/templates/**/*.{html,js}",
    // "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

