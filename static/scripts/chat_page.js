document.addEventListener('DOMContentLoaded', () => {
    // make enter key = send

    let msg = document.querySelector('#user_message');
    // whenever user presses enter\return key (aka keycode 13),
    // javascript will click the #send_message button
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    });
})