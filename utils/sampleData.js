import mongoose from 'mongoose';
import { User } from '../models/user.model.js';
import dotenv from 'dotenv';

dotenv.config();

const connectDB = async () => {
    try {
      await mongoose.connect("mongodb://127.0.0.1:27017/face_attendance");
      console.log('MongoDB connected successfully');
    } catch (error) {
      console.error('MongoDB connection failed:', error.message);
      process.exit(1);
    }
};

const sampleUsers = [
    {
      name: 'John Doe',
      eid: 'EMP001',
      encodedImage: 'base64EncodedImageString1...', // Replace with actual base64 string
      attendance: [
        {
          date: new Date('2025-02-18'),
          status: 'present'
        },
        {
          date: new Date('2025-02-17'),
          status: 'present'
        }
      ]
    },
    {
      name: 'Jane Smith',
      eid: 'EMP002',
      encodedImage: 'base64EncodedImageString2...', // Replace with actual base64 string
      attendance: [
        {
          date: new Date('2025-02-18'),
          status: 'absent'
        },
        {
          date: new Date('2025-02-17'),
          status: 'present'
        }
      ]
    },
    {
      name: 'Mike Johnson',
      eid: 'EMP003',
      encodedImage: 'base64EncodedImageString3...', // Replace with actual base64 string
      attendance: [
        {
          date: new Date('2025-02-18'),
          status: 'present'
        }
      ]
    }
  ];
  const insertUsers = async () => {
    await connectDB();
    try {
      //  await User.deleteMany({});
      // Insert new users
      const createdUsers = await User.insertMany(sampleUsers);
      console.log(`${createdUsers.length} users added successfully`);
      mongoose.disconnect();
      console.log('MongoDB disconnected');
    } catch (error) {
      console.error('Error inserting users:', error);
      mongoose.disconnect();
    }
  };
  insertUsers();