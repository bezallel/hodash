

$(document).ready(function() {
    // Toggle active class on click for appropriate screen sizes
    $(".wrapper ul li a").on("click", function(e) {
      e.preventDefault();
      var li = $(this).parent("li");
      var screenWidth = $(window).width();
      
      if (screenWidth >= 280 && screenWidth <= 800) {
        li.toggleClass("active");
      }
    });
   
    });
  

    document.addEventListener("DOMContentLoaded", function () {
        const dropdowns = document.querySelectorAll(".custom-dropdown");
    
        dropdowns.forEach(function (dropdown) {
            const selected = dropdown.querySelector(".dropdown-selected");
            const options = dropdown.querySelector(".dropdown-options");
    
            // Toggle dropdown on click
            selected.addEventListener("click", function (event) {
                event.stopPropagation(); // Prevent the click from bubbling up to the document
                
                // Close all other dropdowns first
                closeAllDropdowns();
    
                // Toggle the clicked dropdown
                dropdown.classList.toggle("active");
            });
    
            // Handle option selection
            options.addEventListener("click", function (event) {
                if (event.target.classList.contains("dropdown-option")) {
                    const value = event.target.getAttribute("data-value");
                    const text = event.target.textContent;
    
                    selected.textContent = text;
    
                    // Convert data-value to float and store it
                    const floatValue = parseFloat(value);
                    dropdown.querySelector("input[type='hidden']").value = floatValue;
    
                    dropdown.classList.remove("active"); // Close dropdown after selecting an option
                }
            });
        });
    
        // Close dropdown if clicking outside
        document.addEventListener("click", function (event) {
            closeAllDropdowns();
        });
    
        // Function to close all dropdowns
        function closeAllDropdowns() {
            dropdowns.forEach(function (dropdown) {
                dropdown.classList.remove("active");
            });
        }
        // Create Nightly Rate options dynamically (e.g., $100.00, $200.00, etc.)
        createOptions('nightlyHoursOptions', 50, 1000, 50);
    });




    // Function to reset a specific dropdown menu
function resetDropdown(dropdownId, placeholderText) {
    var dropdown = document.querySelector(dropdownId);
    var selectedText = dropdown.querySelector('.dropdown-selected');
    var options = dropdown.querySelectorAll('.dropdown-option');

    // Reset the selected text to placeholder
    selectedText.textContent = placeholderText;

    // Reset each option to its initial state
    options.forEach(option => {
        option.classList.remove('selected');
    });

    // Reset the hidden input value (if present)
    var hiddenInput = dropdown.querySelector('input[type="hidden"]');
    if (hiddenInput) {
        hiddenInput.value = "";
    }
}

// Function to reset all dropdowns and form inputs
function resetForm() {
    resetDropdown('#hotelDropdown', 'Hotel');
    resetDropdown('#leadTimeDropdown', 'Lead Time');
    resetDropdown('#arrivalMonthDropdown', 'Arrival Month');
    resetDropdown('#weekendNightsDropdown', 'Weekend Nights');
    resetDropdown('#weekNightsDropdown', 'Week Nights');
    resetDropdown('#adultsDropdown', 'Adults');
    resetDropdown('#childrenDropdown', 'Children');
    resetDropdown('#babiesDropdown', 'Babies');
    resetDropdown('#mealDropdown', 'Meal');
    resetDropdown('#countryDropdown', 'Country');
    resetDropdown('#marketSegmentDropdown', 'Market Segment');
    resetDropdown('#isRepeatGuestDropdown', 'Repeat Guest?');
    resetDropdown('#cancellationDropdown', 'Cancellations');
    resetDropdown('#completedDropdown', 'Completed');
    resetDropdown('#reservedDropdown', 'Reserved');
    resetDropdown('#assignedDropdown', 'Assigned');
    resetDropdown('#bookingChangesDropdown', 'Booking Changes');
    resetDropdown('#depositDropdown', 'Deposit Type');
    resetDropdown('#WaitListDropdown', 'Wait List');
    resetDropdown('#customerDropdown', 'Customer Type');
    resetDropdown('#nightlyHoursDropdown', 'Nightly Rate');
    resetDropdown('#requestsDropdown', 'Requests');

    // Reset text input fields
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
        input.value = "";
    });
}




  
  //  form submission to pass prediction data
function predict(event) {
    event.preventDefault(); // Prevent default form submission

    var formData = new FormData(document.querySelector('form'));

    fetch('/estimate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
    });
}


 // Function to create dropdown options
 function createOptions(containerId, start, end) {
    const container = document.getElementById(containerId);
    for (let i = start; i <= end; i++) {
        const option = document.createElement('div');
        option.className = 'dropdown-option';
        option.style.setProperty('--i', 5);
        option.className += ' option-text';
        option.dataset.value = i;
        option.innerText = i;
        container.appendChild(option);
    }
}

// Create options for each dropdown
window.onload = function() {
    createOptions('leadTimeOptions', 0, 737); // Lead time options from 1 to 30 days
    createOptions('nightlyHoursOptions', 1, 1000); // Nightly hours from 1 to 24 hours
    createOptions('daysOnWaitListOptions', 0, 391); // Wait list options from 1 to 370 days
};

  
  // Event listener for the form submission
  document.querySelector('form').addEventListener('submit', predict);
  






//   =================================START background red and green==================================


document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    // Add a single event listener for form submission
    form.addEventListener('submit', submitPredictionEntry);
});

function submitPredictionEntry(event) {
    event.preventDefault(); // Prevent form submission

    // Clear previous error highlights
    clearInputHighlights();

    let isValid = true;

    // Get values from the form
    const hotel = document.querySelector('#hotelDropdown .dropdown-selected').textContent.trim();
    const leadTime = document.querySelector('input[name="lead_time"]').value.trim();
    const arrivalMonth = document.querySelector('#arrivalMonthDropdown .dropdown-selected').textContent.trim();
    const weekendNights = document.querySelector('input[name="stays_in_weekend_nights"]').value.trim();
    const weekNights = document.querySelector('input[name="stays_in_week_nights"]').value.trim();
    const adults = document.querySelector('input[name="adults"]').value.trim();
    const children = document.querySelector('input[name="children"]').value.trim();
    const babies = document.querySelector('input[name="babies"]').value.trim();
    const meal = document.querySelector('#mealDropdown .dropdown-selected').textContent.trim();
    const country = document.querySelector('#countryDropdown .dropdown-selected').textContent.trim();
    const marketSegment = document.querySelector('#marketSegmentDropdown .dropdown-selected').textContent.trim();
    const isRepeatGuest = document.querySelector('#isRepeatGuestDropdown .dropdown-selected').textContent.trim();
    const previousCancellations = document.querySelector('input[name="previous_cancellations"]').value.trim();
    const completedBookings = document.querySelector('input[name="previous_bookings_not_canceled"]').value.trim();
    const reservedRoom = document.querySelector('#reservedDropdown .dropdown-selected').textContent.trim();
    const assignedRoom = document.querySelector('#assignedDropdown .dropdown-selected').textContent.trim();
    const bookingChanges = document.querySelector('input[name="booking_changes"]').value.trim();
    const depositType = document.querySelector('#depositDropdown .dropdown-selected').textContent.trim();
    const waitList = document.querySelector('input[name="days_in_waiting_list"]').value.trim();
    const customerType = document.querySelector('#customerDropdown .dropdown-selected').textContent.trim();
    const nightlyRate = document.querySelector('input[name="adr"]').value.trim();
    const specialRequests = document.querySelector('input[name="total_of_special_requests"]').value.trim();

    const requiredFields = [
        { value: hotel, element: '#hotelDropdown .dropdown-selected' },
        { value: leadTime, element: 'input[name="lead_time"]' },
        { value: arrivalMonth, element: '#arrivalMonthDropdown .dropdown-selected' },
        { value: weekendNights, element: 'input[name="stays_in_weekend_nights"]' },
        { value: weekNights, element: 'input[name="stays_in_week_nights"]' },
        { value: adults, element: 'input[name="adults"]' },
        { value: children, element: 'input[name="children"]' },
        { value: babies, element: 'input[name="babies"]' },
        { value: meal, element: '#mealDropdown .dropdown-selected' },
        { value: country, element: '#countryDropdown .dropdown-selected' },
        { value: marketSegment, element: '#marketSegmentDropdown .dropdown-selected' },
        { value: isRepeatGuest, element: '#isRepeatGuestDropdown .dropdown-selected' },
        { value: previousCancellations, element: 'input[name="previous_cancellations"]' },
        { value: completedBookings, element: 'input[name="previous_bookings_not_canceled"]' },
        { value: reservedRoom, element: '#reservedDropdown .dropdown-selected' },
        { value: assignedRoom, element: '#assignedDropdown .dropdown-selected' },
        { value: bookingChanges, element: 'input[name="booking_changes"]' },
        { value: depositType, element: '#depositDropdown .dropdown-selected' },
        { value: waitList, element: 'input[name="days_in_waiting_list"]' },
        { value: customerType, element: '#customerDropdown .dropdown-selected' },
        { value: nightlyRate, element: 'input[name="adr"]' },
        { value: specialRequests, element: 'input[name="total_of_special_requests"]' },
    ];

    // Validate each required field
    requiredFields.forEach(field => {
        if (field.value === "") {
            isValid = false;
            highlightInput(field.element); // Highlight empty field
    
            // Specifically for custom dropdowns, add the invalid class
            const dropdownElement = document.querySelector(field.element).closest('.custom-dropdown');
            if (dropdownElement) {
                dropdownElement.classList.add('invalid');
            }
        }
    });
    

    // Validate dropdowns
    const dropdowns = document.querySelectorAll('.custom-dropdown');
    dropdowns.forEach(dropdown => {
        const selectedValue = dropdown.querySelector('input[type="hidden"]').value;
        if (selectedValue === "") { // Check if not selected
            dropdown.classList.add('invalid'); // Add highlight class
            isValid = false; // Mark form as invalid
        } else {
            dropdown.classList.remove('invalid'); // Remove highlight class if valid
        }
    });

    if (!isValid) {
        alert("Please fill in all required fields.");
        return; // Stop form submission if validation fails
    }

    // Create formData to send to Flask
    var formData = new FormData(document.querySelector('form'));

    // Send the form data to the server for prediction
    fetch('/estimate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.hasOwnProperty('prediction')) {
            const prediction = data.prediction;

            // Create a new table row
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${hotel}</td>
                <td style="display:none;">${leadTime}</td>
                <td>${arrivalMonth}</td> 
                <td style="display:none;">${weekendNights}</td>
                <td>${weekNights}</td>
                <td>${adults}</td>
                <td>${children}</td>
                <td style="display:none;">${babies}</td>
                <td>${meal}</td>
                <td>${country}</td>
                <td style="display:none;">${marketSegment}</td>
                <td style="display:none;">${isRepeatGuest}</td>
                <td>${previousCancellations}</td>
                <td>${completedBookings}</td>
                <td style="display:none;">${reservedRoom}</td>
                <td>${assignedRoom}</td>
                <td style="display:none;">${bookingChanges}</td>
                <td style="display:none;">${depositType}</td>
                <td style="display:none;">${waitList}</td>
                <td style="display:none;">${customerType}</td>
                <td style="display:none;">${nightlyRate}</td>
                <td style="display:none;">${specialRequests}</td>
            `;

            // Append the new row to the tbody
            const guestBody = document.getElementById('guestBody');
            guestBody.appendChild(newRow);

            // Apply text color to each <td> based on prediction
            const cells = newRow.querySelectorAll('td');
            cells.forEach(cell => {
                if (prediction === 1) {
                    cell.style.color = 'red'; // Prediction: Very Likely (1)
                } else if (prediction === 0) {
                    cell.style.color = 'green'; // Prediction: Not Likely (0)
                }
            });

            // Clear the form fields and reset the dropdowns
            document.querySelector('form').reset();
            resetForm(); // Reset dropdowns and inputs
        } else if (data.hasOwnProperty('error')) {
            console.error(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to highlight incomplete input fields
function highlightInput(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.classList.add('invalid'); // Add invalid class to turn border red
    }
}

// Function to clear previous input highlights
function clearInputHighlights() {
    document.querySelectorAll('input, .dropdown-selected').forEach(element => {
        element.classList.remove('invalid'); // Remove invalid class to reset border
    });
}


//   =================================End background red and green==================================






// ============================================POP-UP INTRO=========================================


document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById('tiltPopup');
    const closeButton = document.getElementById('closePopup');

    // Function to check screen width and show the popup
    function checkScreenWidth() {{
            popup.classList.remove('show'); // Hide popup if wider than 768px
        }
    }

    // Close the popup when the close button is clicked
    closeButton.addEventListener('click', function() {
        popup.classList.remove('show');
    });

    // Check screen width on window resize
    window.addEventListener('resize', checkScreenWidth);

    // Show the popup on page load
    checkScreenWidth(); // Ensure the popup shows up correctly on load
});





// ============================================POP-UP INTRO=========================================
