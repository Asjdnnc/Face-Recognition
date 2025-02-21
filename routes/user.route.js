import express from "express"
import multer from "multer"
import { createUser, fetchUsers, receivePythonData, updateAttendance,getUserList, deleteUser, detectFace } from "../controllers/user.controller.js"
import { login } from "../controllers/admin.controller.js";
import isAuthenticated from "../middlewares/auth.middleware.js";

const upload = multer({ dest: "uploads/" });

const router = express.Router()
// router.route('/create-admin').post(createAdmin)
// router.route('/login').get((req, res) => {
//     res.render('admin-login');
// });
router.route('/login')
    .get((req, res) => {
        res.render('admin-login', { error: req.query.error });
    })
    .post(login);
router.route('/create-user').post(upload.single("image"),createUser)
router.route('/fetch-data').get(fetchUsers)
router.route('/receive-data').post(receivePythonData)
router.route('/update-attendance').post(updateAttendance)
router.route('/users').get(isAuthenticated,getUserList)
router.route('/delete-user/:id').post(deleteUser)
router.route('/live-attendance').get(isAuthenticated,(req, res) => {
    res.render('live-attendance');
});

router.route('/detect-face').post(upload.single('image'), detectFace);
export default router