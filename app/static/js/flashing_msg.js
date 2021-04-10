window.addEventListener('DOMContentLoaded', () => {
    flashedMsg = document.getElementById('flash-msg');
    if (flashedMsg){
        window.setTimeout(() => { flashedMsg.remove(); }, 5000);
    };
});
