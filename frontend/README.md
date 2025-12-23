# AI Policy Assistant - Frontend

Modern React frontend for the PDF-based Policy Chatbot.

## ✨ Features

- **Smooth Chat Interface**: Chat-like messages with animations
- **Auto-scroll**: Automatically scrolls to latest messages
- **Source Citations**: Shows document sources with relevance scores
- **Confidence Indicators**: Visual badges for High/Medium/Low confidence
- **PDF Upload**: Drag and drop or browse to upload policy documents
- **Real-time Stats**: Display collection statistics
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will start on `http://localhost:5173` (or another port if 5173 is in use).

### 3. Ensure Backend is Running

Make sure your FastAPI backend is running on `http://localhost:8000`:

```bash
# From the root directory
python api.py
```

## 🛠️ Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## 🎨 Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Lucide React** - Icon library

## 📡 API Endpoints

The frontend communicates with the following backend endpoints:

- `POST /api/query` - Send questions and get answers
- `POST /api/upload` - Upload PDF documents
- `GET /api/stats` - Get collection statistics

## 🎯 Usage

1. **Upload Documents**: Click "Select PDF Document" and choose a policy PDF
2. **Click Upload & Ingest**: Process the document into the vector database
3. **Ask Questions**: Type questions in the input field at the bottom
4. **View Responses**: Get answers with source citations and confidence levels

## 🔧 Configuration

The API proxy is configured in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

To change the backend URL, update the `target` in `vite.config.js`.

## 🎨 Customization

### Colors

Modify `tailwind.config.js` to change the primary color scheme:

```javascript
colors: {
  primary: {
    // Your custom colors
  }
}
```

### Layout

The main chat interface is in `src/App.jsx`. Adjust the max-width, spacing, or layout as needed.

## 📱 Features Overview

### Message Display
- User messages appear on the right in blue
- Assistant responses on the left in gray
- Smooth fade-in animations for each message

### Source Attribution
- Document name, page number, and section
- Relevance percentage for each source
- Expandable source details

### Confidence Scoring
- 🟢 High (>85% similarity)
- 🟡 Medium (70-85% similarity)
- 🔴 Low (<70% similarity)

### Auto-scroll
- Automatically scrolls to newest messages
- Smooth scroll behavior
- Triggered after user input and responses

## 🐛 Troubleshooting

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Can't connect to backend:**
- Check if the backend is running on port 8000
- Verify the proxy configuration in `vite.config.js`
- Check browser console for CORS errors

**Styles not loading:**
- Ensure PostCSS config exists
- Check that Tailwind directives are in `index.css`
- Clear browser cache

## 📄 License

Part of the AI Policy Assistant project.
