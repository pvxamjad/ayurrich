//// spinner 

const spinnerElement = document.querySelector('.spinner');

window.addEventListener('load', () => {

    spinnerElement.style.opacity = '0';
    

    setTimeout(() => {
        spinnerElement.style.display = 'none';
    }, 1000);
});

//// spinner end


