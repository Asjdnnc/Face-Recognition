import express from "express"
import cors from "cors"
import cookieParser from "cookie-parser"
import dotenv from "dotenv"
import multer from 'multer'
import path from 'path'
import { fileURLToPath } from 'url'
import connectDB from "./utils/db.js"
import { User } from "./models/user.model.js"
import fs from 'fs/promises'

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
try {
    await fs.access(uploadsDir);
} catch {
    await fs.mkdir(uploadsDir);
}

dotenv.config()
const app = express()

// Set up EJS as view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())
const corsOptions = {
    origin: "http://localhost:3000",
    credentials: true,
}
// app.use(cors(corsOptions))
app.use(cors())

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadsDir) // Use the uploads directory path
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname)
    }
})

const upload = multer({ storage: storage })

// Routes
app.get('/register', (req, res) => {
    res.render('form');
});

app.post('/register', upload.single('image'), async (req, res) => {
    try {
        const { name, eid } = req.body;
        const imagePath = req.file.path;

        // Read the image file and convert to base64
        const imageBuffer = await fs.readFile(imagePath);
        const encodedImage = imageBuffer.toString('base64');

        // Create new user with base64 image
        const user = new User({
            name,
            eid,
            encodedImage
        });

        await user.save();

        // Delete the temporary uploaded file
        await fs.unlink(imagePath);

        res.json({ 
            success: true, 
            message: 'User registered successfully',
            user: {
                name: user.name,
                eid: user.eid,
                createdAt: user.createdAt
            }
        });
    } catch (error) {
        console.error('Registration error:', error);
        // Clean up the uploaded file if it exists
        if (req.file) {
            await fs.unlink(req.file.path).catch(console.error);
        }
        res.status(500).json({ 
            success: false, 
            message: 'Error registering user',
            error: error.message 
        });
    }
});

//receive data from python script
app.post("/python",(req,res)=>{
    receivedData = req.body;
    console.log("Data received:", receivedData);
    res.status(200).json({
        message: "Data received successfully"
    })
})
// Fetch data from MongoDB 
app.get("/fetch-data", async (req, res) => {
    try {
      const data = await User.find();
      res.json(data);
    } catch (error) {
      res.status(500).json({ error: "Error fetching data" });
    }
  });
//api to mark attendance
app.get("/api",(req,res)=>{
    res.status(200).json({
        data: receivedData,
        success: true
    })
})
app.get("/", (req,res)=>{
    res.status(200).json({
        message: "Hello World"
    })}
)

const PORT = process.env.PORT || 3000;
let receivedData = {};

app.listen(PORT, () => {
    connectDB()
    console.log(`Server is running on port ${PORT}`)
})