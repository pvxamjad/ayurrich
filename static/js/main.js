//// spinner 
document.addEventListener('DOMContentLoaded', () => {
    const spinnerElement = document.querySelector('.spinner');
    
    // Show spinner initially
    spinnerElement.style.opacity = '1';
    spinnerElement.style.visibility = 'visible';
    spinnerElement.style.pointerEvents = 'auto';

    // Simulate a short delay (e.g., 500ms) before hiding the spinner
    setTimeout(() => {
        spinnerElement.style.opacity = '0';
        spinnerElement.style.pointerEvents = 'none';
        spinnerElement.style.visibility = 'hidden';

        setTimeout(() => {
            spinnerElement.style.display = 'none';
        }, 300); // Match the CSS transition duration
    }, 500); // Adjust this duration as needed
});


//// spinner end

