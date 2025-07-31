// Middle Ware to handle RFID data and send it to the client
const express = require('express');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');
const http = require('http');
const axios = require('axios');

const app = express();
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

// Serve static files
app.use(express.static(__dirname + '/templates'));

// Port based on system
//const portName = 'COM4';
const portName = '/dev/ttyACM0'
const serialPort = new SerialPort({ path: portName, baudRate: 9600 });
const parser = serialPort.pipe(new ReadlineParser({ delimiter: '\n' }));

// Handle RFID data (runs once)
parser.on('data', async (data) => {
    const rfidTag = data.trim();
    console.log('Scanned RFID:', rfidTag);


    try {
        //check if rfid exists in the database
        const response = await axios.get(`http://192.168.1.114:3030/userData/${rfidTag}`);

        if (response.data.exists) {
            // If RFID exists in the database, send error to client
            io.emit('rfidError', 'RFID already exists');
        } else {
            // if RFID doesn't exist, send it to the client
            io.emit('rfidData',rfidTag);
        }
    } catch (error) {
        console.error('Error querying the database:', error);
        io.emit('rfidError', 'Error validating RFID');
    }
});

// Handle client connections
io.on('connection', (socket) => {
    console.log('Client connected');

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// Start the server on port 3000
server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000.');
});
