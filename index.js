import express from "express"
import cors from "cors"
import cookieParser from "cookie-parser"
import dotenv from "dotenv"
import connectDB from "./utils/db.js"

dotenv.config({})
const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())
const corsOptions = {
    origin: "http://localhost:3000",
    credentials: true,
}
// app.use(cors(corsOptions))
app.use(cors())
const PORT = process.env.PORT || 3000;
let receivedData = {};

app.listen(PORT, () => {
    connectDB()
    console.log(`Server is running on port ${PORT}`)
})
app.post("/python",(req,res)=>{
    receivedData = req.body;
    console.log("Data received:", receivedData);
    res.status(200).json({
        message: "Data received successfully"
    })
})
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