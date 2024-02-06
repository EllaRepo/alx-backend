// Import necessary modules and libraries
const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

// Create a Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create a Kue queue
const queue = kue.createQueue();

// Initialize express app
const app = express();
app.use(express.json());

// Set the initial number of available seats to 50
client.set('available_seats', 50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Define function to reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Define function to get current available seats
async function getCurrentAvailableSeats() {
  return await getAsync('available_seats');
}

// Define route to get current available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats });
});

// Define route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
  } else {
    // Create and queue a job in the reserve_seat queue
    const job = queue.create('reserve_seat').save((err) => {
      if (err) {
        res.json({ status: "Reservation failed" });
      } else {
        res.json({ status: "Reservation in process" });
      }
    });
  }
});

// Define route to process the queue
app.get('/process', async (req, res) => {
  let numberOfAvailableSeats = await getCurrentAvailableSeats();
  numberOfAvailableSeats = parseInt(numberOfAvailableSeats);

  if (numberOfAvailableSeats > 0) {
    // Decrease the number of available seats
    await reserveSeat(numberOfAvailableSeats - 1);
    if (numberOfAvailableSeats === 1) {
      reservationEnabled = false;
    }
    res.json({ status: "Queue processing" });
  } else {
    res.status(400).json({ message: "Not enough seats available" });
  }
});

// Start the server
const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
