/** @type {import('tailwindcss').Config} */
export default {
  content: {
    files: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'], // Define the paths to all template files
  },
  theme: {
    extend: {
      colors: {
        primary: {
          base: "#660f31",
          shadow: "#450327",
          bg: "#835B86",
          accent: {
            light: "#9c173b",
            bright: "#ff0546"
          },
          dark: {
            base: "#270022",
            shadow: "#17001d",
            deep: "#09010d"
          },
          
        },
        alerts: {
          base: "#0098db",
          accent: "#0ce6f2",
          shadow: "#1e579c",

        },
        accent: {
          yellow: {
            base: "#fee801",
            shadow: "#9c8e00",
          }
          
        }
      },
    },
  },
}
