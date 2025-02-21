import jwt from 'jsonwebtoken';

const isAuthenticated = async (req, res, next) => {
    try {
        const token = req.cookies.token;

        if (!token) {
            return res.redirect('/api/v1/login');
        }

        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            req.admin = decoded;
            next();
        } catch (error) {
            res.clearCookie('token');
            return res.redirect('/api/v1/login');
        }
    } catch (error) {
        return res.status(500).render('admin-login', {
            error: 'Authentication error. Please try again.'
        });
    }
};

export default isAuthenticated;