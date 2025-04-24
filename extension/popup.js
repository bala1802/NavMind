document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('inputText');
    const submitButton = document.getElementById('submitButton');
    const responseDiv = document.getElementById('response');
  
    submitButton.addEventListener('click', function() {
      const text = inputText.value.trim();
      
      if (!text) {
        alert('Please enter some text');
        return;
      }
  
      responseDiv.textContent = 'Processing...';
      responseDiv.style.display = 'block';
  
      // Send the text to your Python server
      fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        responseDiv.textContent = data.response || JSON.stringify(data);
      })
      .catch(error => {
        responseDiv.textContent = 'Error: ' + error.message;
        console.error('Error:', error);
      });
    });
  });
  