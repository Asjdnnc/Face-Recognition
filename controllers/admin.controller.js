import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import {Admin} from '../models/admin.model.js';

// export const createAdmin = async (req, res) => {
//     const { username, password } = req.body;

//     try {
//         // Check if admin already exists
//         const existingAdmin = await Admin.findOne({username});

//         if (existingAdmin) {
//             return res.status(400).json({ 
//                 message: 'Admin with this username or email already exists' 
//             });
//         }

//         // Hash password
//         const salt = await bcrypt.genSalt(10);
//         const hashedPassword = await bcrypt.hash(password, salt);

//         // Create new admin
//         const admin = new Admin({
//             username,
//             password: hashedPassword
//         });

//         await admin.save();

//         // Create JWT token
//         const token = jwt.sign({ id: admin._id }, process.env.JWT_SECRET, {
//             expiresIn: '1h'
//         });

//         res.status(201).json({
//             message: 'Admin created successfully',
//         });
//     } catch (error) {
//         res.status(500).json({ message: 'Server error', error: error.message });
//     }
// };

export const login = async (req, res) => {
    const { username, password } = req.body;

    try {
        // Find admin by username
        const admin = await Admin.findOne({ username });
        if (!admin) {
            return res.status(404).render('admin-login', { 
                error: 'Admin not found' 
            });
        }

        // Check if password matches
        const isMatch = await bcrypt.compare(password, admin.password);
        if (!isMatch) {
            return res.status(400).render('admin-login', { 
                error: 'Invalid credentials' 
            });
        }

        // Create JWT token
        const token = jwt.sign({ id: admin._id }, process.env.JWT_SECRET, {
            expiresIn: '1h',
        });

        // Store token in cookie
        res.cookie('token', token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            maxAge: 3600000 // 1 hour
        });

        // Redirect to userList page
        res.redirect('/api/v1/users');
    } catch (error) {
        res.status(500).render('admin-login', { 
            error: 'Server error. Please try again.' 
        });
    }
};