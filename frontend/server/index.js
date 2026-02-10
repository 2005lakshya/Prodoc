const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Multer setup for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage });

// Ensure uploads directory exists
const fs = require('fs');
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

// API Routes
app.post('/api/analyze', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    console.log('Received file:', req.file.originalname);

    // Mock analysis result (This will be replaced by the AI model later)
    const analysisResult = {
        overallAccuracy: 85,
        issues: [
            "Low contrast in tax identification number field",
            "Slight blurriness on the bottom right corner",
            "Minor font variation detected in signature area"
        ],
        extractedInfo: [
            { field: "Document Type", value: "Tax Invoice", accuracy: 98 },
            { field: "Issuer Name", value: "ProTech Solutions Inc.", accuracy: 95 },
            { field: "Date", value: "24/05/2025", accuracy: 100 },
            { field: "Invoice ID", value: "INV-2025-0892", accuracy: 82 },
            { field: "Total Amount", value: "$1,240.50", accuracy: 91 }
        ]
    };

    // Simulate processing delay
    setTimeout(() => {
        res.json(analysisResult);
    }, 2000);
});

app.get('/', (req, res) => {
    res.send('PRO DOC Backend is running');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
