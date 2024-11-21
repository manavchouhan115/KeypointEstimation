setInterval(() => {
    fetch('/detect')
        .then(response => response.json())
        .then(jsonData => {
            console.log("Received JSON:", jsonData);

            // Display JSON data in the HTML
            const outputDiv = document.getElementById("output");
            outputDiv.innerHTML = `
                <p>smallArmTop: x=${jsonData.smallArmTop.x}, y=${jsonData.smallArmTop.y}</p>
                <p>smallArmBottom: x=${jsonData.smallArmBottom.x}, y=${jsonData.smallArmBottom.y}</p>
                <p>bigArmTop: x=${jsonData.bigArmTop.x}, y=${jsonData.bigArmTop.y}</p>
                <p>bigArmBottom: x=${jsonData.bigArmBottom.x}, y=${jsonData.bigArmBottom.y}</p>
            `;
        })
        .catch(error => console.error("Error fetching data:", error));
}, 500);  // Fetch every 0.5 seconds
