document.addEventListener("DOMContentLoaded", function () {
    function fetchAttendance() {
        fetch("/attendance")
            .then(response => response.json())
            .then(data => {
                let list = document.getElementById("attendanceList");
                list.innerHTML = "";
                for (let person in data) {
                    let li = document.createElement("li");
                    li.textContent = `${person}: ${data[person]}`;
                    list.appendChild(li);
                }
            });
    }

    fetchAttendance();
    setInterval(fetchAttendance, 5000);
});
