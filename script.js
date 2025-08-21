// Container data storage
let containers = [];
let editingIndex = -1;

// DOM elements
const form = document.getElementById('containerForm');
const tableBody = document.getElementById('tableBody');
const noDataMessage = document.getElementById('noDataMessage');
const cancelEditBtn = document.getElementById('cancelEdit');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Auto-populate today's date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    
    // Load data from localStorage if available
    loadDataFromStorage();
    
    // Update table display
    updateTable();
    
    // Form submission handler
    form.addEventListener('submit', handleFormSubmit);
    
    // Cancel edit handler
    cancelEditBtn.addEventListener('click', cancelEdit);
});

// Handle form submission
function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const containerData = {
        date: formData.get('date'),
        port: formData.get('port'),
        containerNumber: formData.get('containerNumber'),
        status: formData.get('status'),
        arrivalTime: formData.get('arrivalTime'),
        comment: formData.get('comment') || ''
    };
    
    if (editingIndex >= 0) {
        // Update existing entry
        containers[editingIndex] = containerData;
        editingIndex = -1;
        cancelEditBtn.style.display = 'none';
        document.querySelector('.submit-btn').textContent = 'Add Entry';
    } else {
        // Add new entry
        containers.push(containerData);
    }
    
    // Save to localStorage
    saveDataToStorage();
    
    // Reset form
    form.reset();
    // Re-populate today's date after reset
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    
    // Update table
    updateTable();
}

// Update the table display
function updateTable() {
    tableBody.innerHTML = '';
    
    if (containers.length === 0) {
        noDataMessage.style.display = 'block';
        document.getElementById('containerTable').style.display = 'none';
        return;
    }
    
    noDataMessage.style.display = 'none';
    document.getElementById('containerTable').style.display = 'table';
    
    containers.forEach((container, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${container.date}</td>
            <td>${container.port}</td>
            <td>${container.containerNumber}</td>
            <td>${container.status}</td>
            <td>${container.arrivalTime}</td>
            <td>${container.comment}</td>
            <td>
                <div class="action-buttons">
                    <button class="edit-btn" onclick="editEntry(${index})">Edit</button>
                    <button class="delete-btn" onclick="deleteEntry(${index})">Delete</button>
                </div>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Edit an entry
function editEntry(index) {
    const container = containers[index];
    
    // Populate form with existing data
    document.getElementById('date').value = container.date;
    document.getElementById('port').value = container.port;
    document.getElementById('containerNumber').value = container.containerNumber;
    document.getElementById('status').value = container.status;
    document.getElementById('arrivalTime').value = container.arrivalTime;
    document.getElementById('comment').value = container.comment;
    
    // Set editing mode
    editingIndex = index;
    cancelEditBtn.style.display = 'inline-block';
    document.querySelector('.submit-btn').textContent = 'Update Entry';
    
    // Scroll to form
    form.scrollIntoView({ behavior: 'smooth' });
}

// Cancel edit operation
function cancelEdit() {
    editingIndex = -1;
    cancelEditBtn.style.display = 'none';
    document.querySelector('.submit-btn').textContent = 'Add Entry';
    
    // Reset form
    form.reset();
    // Re-populate today's date after reset
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}

// Delete an entry
function deleteEntry(index) {
    if (confirm('Are you sure you want to delete this container entry?')) {
        containers.splice(index, 1);
        saveDataToStorage();
        updateTable();
        
        // If we were editing this entry, cancel the edit
        if (editingIndex === index) {
            cancelEdit();
        } else if (editingIndex > index) {
            // Adjust editing index if necessary
            editingIndex--;
        }
    }
}

// Save data to localStorage
function saveDataToStorage() {
    localStorage.setItem('containerEntries', JSON.stringify(containers));
}

// Load data from localStorage
function loadDataFromStorage() {
    const savedData = localStorage.getItem('containerEntries');
    if (savedData) {
        try {
            containers = JSON.parse(savedData);
        } catch (error) {
            console.error('Error loading data from localStorage:', error);
            containers = [];
        }
    }
}

// Utility function to format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB');
}

// Utility function to format time for display
function formatTime(timeString) {
    return timeString;
}