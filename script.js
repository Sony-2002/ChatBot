// JavaScript for handling form submission and validation
document.getElementById("login-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting the traditional way

  // Get the values entered by the user
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Simple validation for demonstration (you can expand this as needed)
  if (username === "admin" && password === "password123") {
    // Redirect to chatbot interface or the next page
    window.location.href = "chatbot_interface.html"; // Redirect to the chatbot page (create chatbot_interface.html)
  } else {
    // Show an error message if login fails
    const errorMessage = document.getElementById("error-message");
    errorMessage.style.display = "block";
    errorMessage.textContent = "Invalid username or password.";
  }
});
