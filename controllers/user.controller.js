import { User } from "../models/user.model.js";
import fs from 'fs/promises'

export const createUser = async (req, res) => {
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
            res.redirect('/api/v1/users');
            // res.json({ 
            //     success: true, 
            //     message: 'User registered successfully',
            //     user: {
            //         name: user.name,
            //         eid: user.eid,
            //         createdAt: user.createdAt
            //     }
            //});
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
    };


export const fetchUsers = async (req, res) => {
    try {
        const users = await User.find();
        res.json(users);
    } catch (error) {
        res.status(500).json({ success: false, message: "Error fetching users", error: error.message });
    }
};

let receivedData = {}; // Store received data from Python

// Receive data from Python script
export const receivePythonData = (req, res) => {
    receivedData = req.body;
    console.log("Data received:", receivedData);
    res.status(200).json({ message: "Data received successfully" });
};

// API to return received data
export const fetchReceivedData = (req, res) => {
    res.status(200).json({ data: receivedData, success: true });
};

export const updateAttendance = async (req, res) => {
    try {
        const { eid, isMatched } = req.body;

        if (!eid) {
            return res.status(400).json({ success: false, message: "EID is required" });
        }

        const user = await User.findOne({ eid });

        if (!user) {
            return res.status(404).json({ success: false, message: "User not found" });
        }

        if (isMatched) {
            user.attendance.push({ date: new Date(), status: "Present" });
            await user.save();
            return res.json({ success: true, message: "Attendance marked" });
        } else {
            return res.json({ success: false, message: "Face did not match, attendance not marked" });
        }

    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
}
export const getUserList = async (req, res) => {
    try {
        const users = await User.find();
        res.render('userList', { users });
    } catch (error) {
        res.status(500).json({ success: false, message: "Error fetching users", error: error.message });
    }
}

export const deleteUser = async (req, res) => {
    try {
        const { id } = req.params;
        
        if (!id) {
            return res.status(400).json({ 
                success: false, 
                message: "User ID is required" 
            });
        }

        // Check if user exists
        const user = await User.findById(id);
        if (!user) {
            return res.status(404).json({ 
                success: false, 
                message: "User not found" 
            });
        }

        // Delete the user
        await User.findByIdAndDelete(id);
        
        // Send success response
        res.status(200).json({ 
            success: true, 
            message: "User deleted successfully" 
        });
    } catch (error) {
        console.error('Delete error:', error);
        res.status(500).json({ 
            success: false, 
            message: error.message || "Error deleting user"
        });
    }
};

export const detectFace = async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({
                success: false,
                message: "No image provided"
            });
        }

        // Read the image file and convert to base64
        const imageBuffer = await fs.readFile(req.file.path);
        const encodedImage = imageBuffer.toString('base64');

        // Clean up the uploaded file
        await fs.unlink(req.file.path);

        // Here you would typically:
        // 1. Send the image to your Python face recognition script
        // 2. Get the results back
        // 3. Update attendance if a match is found

        // For now, we'll return a mock response
        return res.json({
            success: true,
            message: "Face detected successfully"
        });

    } catch (error) {
        console.error('Face detection error:', error);
        if (req.file) {
            await fs.unlink(req.file.path).catch(console.error);
        }
        res.status(500).json({
            success: false,
            message: "Error processing image",
            error: error.message
        });
    }
};