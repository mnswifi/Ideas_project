const socket = io.connect("http://127.0.0.1:8001");
        socket.on('connect', () => {
            console.log('Connected to server');
        });
        socket.on('update_data', (data) =>{
            console.log('Received data:', data);
            document.getElementById("name").innerHTML = "Name: " + data.full_name;
            document.getElementById("staff_id").innerHTML = "Staff ID: " + data.staff_id;
            document.getElementById("directorate").innerHTML = "Directorate: " + data.directorate;
            document.getElementById("time").innerHTML = "Time: " + data.time;
            document.getElementById("status").innerHTML = "Status: " + data.status;
            const attendanceInfo = document.getElementById('attendance-info');
            attendanceInfo.innerHTML = `
                <p>Name: ${data.full_name}</p>
                <p>Staff ID: ${data.staff_id}</p>
                <p>Directorate: ${data.directorate}</p>
                <p>Time: ${data.time}</p>
                <p>Status: ${data.status}</p>
            `;
        });
        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });