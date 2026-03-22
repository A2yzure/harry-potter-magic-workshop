/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'hp-gold': '#D4AF37',
        'hp-dark': '#0A0A0A',
        'hp-purple': '#2E1A47',
        'hp-red': '#740001',
        'hp-green': '#1A472A',
        'hp-blue': '#0E1A40',
      }
    },
  },
  plugins: [],
}
