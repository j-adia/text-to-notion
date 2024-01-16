document.addEventListener("DOMContentLoaded", function(){
    const startButton = document.getElementById("begin_button");
    const landing = document.querySelector('.landing');
    const upload = document.querySelector('.upload');

    startButton.addEventListener("click", function(){
        landing.classList.add('playTransitionAnimation');
        upload.classList.add('playFadeInAnimation');
        upload.classList.add('visible');
    });

    const fileInpt = document.getElementById('upload');
    fileInpt.onchange = () => {
        const file = fileInpt.files[0];
        console.log(file);
    }
});