import { User } from "../models/user.model";

export const createUser = async (req, res) => {
    try {
        const {name,eid} = req.body
        const file = req.file
        if(!name || !email || !file){
            return res.status(400).json({
                message: 'Name, email, and image file are required.',
                success: false
            });
        }

        const existingUser = await User.findOne({eid});
        if(existingUser){
            return res.status(400).json({
                message: 'User already exists with this eid.',
                success: false
            });
        }

        const encodedImage = file.buffer.toString('base64')
        const user = new User({
            name,
            eid,
            encodedImage
        })

        await user.save()

        return res.status(201).json({
            message: 'User created successfully.',
            success: true
        });
    } catch (error) {
        console.log(error);
    }
}