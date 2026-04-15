# AI Course Advisor | Premium Frontend 🎨

The user interface for the AI Course Recommender is built to deliver a premium, focus-oriented experience. It follows the **Obsidian/Apple design aesthetic**, emphasizing readability and fluid interaction.

---

## 🎨 Design Philosophy
- **Obsidian Dark Palette:** Deep blacks and subtle purple accents (`#bb86fc`) for a modern professional feel.
- **Glassmorphism:** Leverages `backdrop-filter: blur()` to create depth and focus.
- **Bento-Box Results:** A grid-based dashboard that scales dynamically to fit different types of content (Skills, Degrees, Courses).

---

## 🛠️ Key Components
- **Multi-Step Profiler:** Breaks down data entry (Personal -> Academic -> Skills -> Goals) into manageable steps.
- **Canvas Particles:** A custom JavaScript background animation that signifies the "Brain" of the AI system.
- **Dynamic Results Engine:** Renders JSON data from the backend into beautifully formatted bento cards.

---

## 🚀 Development
The frontend is built using **Vanilla HTML5, CSS3, and JavaScript**. No heavy frameworks (like React) were used in this version to ensure maximum performance and zero build-time overhead.

### Running the Frontend
1. Ensure the backend is running at `http://localhost:8000`.
2. Open `index.html` in your browser.
3. **Important:** If you are deploying, update the `PRODUCTION_API_URL` in `app.js` to your Render URL.

---

## 📱 Responsiveness
The UI is fully responsive using CSS Grid and Flexbox.
- **Desktop:** 3-column Bento layout.
- **Tablet:** 2-column Bento layout.
- **Mobile:** Single column vertical stack.
