File - 1 src/controllers/userController.js:


const User = require('../models/userModel');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

/**
 * Handles user registration.
 * @param {Object} req - Express request object containing registration data.
 * @param {string} req.body.username - The desired username.
 * @param {string} req.body.password - The user's chosen password.
 * @param {Object} res - Express response object.
 * @returns {Object} A JSON response indicating success or failure of registration.
 */
exports.registerUser = async (req, res) => {
  try {
    const { username, password } = req.body;

    // Check for existing username
    const existingUser = await User.findOne({ username });
    if (existingUser) {
      return res.status(409).json({ message: 'Username already exists' });
    }

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10); // Use a strong salt round

    // Create and save new user
    const newUser = new User({ username, password: hashedPassword });
    await newUser.save();

    return res.status(201).json({ message: 'User registered successfully' });

  } catch (error) {
    console.error('Error registering user:', error); // Log errors for debugging
    return res.status(500).json({ message: 'Internal server error' });
  }
};

/**
 * Handles user login.
 * @param {Object} req - Express request object containing login credentials.
 * @param {string} req.body.username - The username.
 * @param {string} req.body.password - The password.
 * @param {Object} res - Express response object.
 * @returns {Object} A JSON response containing the JWT token on success, or an error message.
 */
exports.loginUser = async (req, res) => {
  try {
    const { username, password } = req.body;

    // Find user by username
    const existingUser = await User.findOne({ username });
    if (!existingUser) {
      return res.status(401).json({ message: 'Invalid username or password' });
    }

    // Verify password
    const isPasswordCorrect = await bcrypt.compare(password, existingUser.password);
    if (!isPasswordCorrect) {
      return res.status(401).json({ message: 'Invalid username or password' });
    }

    // Generate JWT
    const token = jwt.sign({ username: existingUser.username }, 'your-secret-key', { expiresIn: '1h' }); 
    return res.status(200).json({ token });

  } catch (error) {
    console.error('Error logging in user:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
};

/**
 * Handles user profile updates (currently only username changes).
 * @param {Object} req - Express request object.
 * @param {string} req.params.username - The current username to update.
 * @param {string} req.body.newUsername - The new username.
 * @param {Object} res - Express response object.
 * @returns {Object} A JSON response indicating success or failure of the update.
 */
exports.updateUserProfile = async (req, res) => {
  try {
    const { username } = req.params;
    const { newUsername } = req.body;
    
    // Update username (add validation/checks if needed)
    await User.updateOne({ username }, { username: newUsername }); 

    return res.status(200).json({ message: 'User profile updated successfully' });

  } catch (error) {
    console.error('Error updating user profile:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
};



File - 2 src/models/userModel.js:

const mongoose = require('mongoose');

// User Schema Definition
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,  // Username is mandatory
    unique: true,    // Ensure usernames are unique
  },
  password: {
    type: String,
    required: true,  // Password is mandatory
  },
});

// Create the User Model based on the schema
const User = mongoose.model('User', userSchema);

module.exports = User; 


File -3 src/routes/userRoutes.js:

const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Define user-related routes
router.post('/register', userController.registerUser);       // POST /users/register
router.post('/login', userController.loginUser);             // POST /users/login
router.put('/:username', userController.updateUserProfile);  // PUT /users/:username

module.exports = router;


File - 4 src/config/database.js:

const mongoose = require('mongoose');

// Database Connection Function
const connectDB = async () => {
  try {
    await mongoose.connect('mongodb://root:password@localhost:27017'); // Replace with your actual connection string
    console.log('MongoDB connected');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1); // Exit with failure if connection fails
  }
};

module.exports = connectDB;



File - 5 src/index.js:

const express = require('express');
const connectDB = require('./config/database');
const userRoutes = require('./routes/userRoutes');

const app = express();

// Connect to the database
connectDB();

// Middleware to parse JSON request bodies
app.use(express.json()); 

// Use the user-related routes
app.use('/users', userRoutes);

// Start the server
const port = 3000; 
app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});