window.addEventListener('DOMContentLoaded', (event) => {
    let nick = document.getElementById('current-user-nick').value();
    if (nick == 'None'){
        document.getElementById('background-content').classList.add('disable-background');
        document.body.style.overflow = 'hidden';
        document.getElementById('set-nick-window').classList.remove('disable-background');
    } else {
        document.getElementById('background-content').classList.remove('disable-background');
        document.body.style.overflow = 'hidden';
    };
});
