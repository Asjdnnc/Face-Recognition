import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    eid: {
        type: String,
        required: true
    },
    encodedImage: {
        type: String,
        required: true
    },
    attendance: [
        {
          date: {
            type: Date,
            default: Date.now
          },
          status: {
            type: String,
            enum: ['present', 'absent'],
            default: 'present'
          }
        }
      ]
}, {
    timestamps: true
});

export const User = mongoose.model('User', userSchema);
