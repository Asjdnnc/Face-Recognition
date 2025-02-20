import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    eid: {
        type: String,
        required: true,
        unique: true
    },
    attendance:[{
        date: { type: Date, default: Date.now },
        status: { type: String, enum: ["Present", "Absent"], default: "Absent" }
    }],
    encodedImage: {
        type: String,
        required: true
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

export const User = mongoose.model('User', userSchema);