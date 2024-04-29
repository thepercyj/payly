;(function(){
    const dialogModal = new bootstrap.Modal(document.getElementById('modal'));
    const popup = new bootstrap.Toast(document.getElementById('popup'));
    const popupTitle = document.getElementById('popup-title');
    const popupMessage = document.getElementById('popup-message');
    const popupIcon = document.getElementById('popup-icon');

    document.body.addEventListener('htmx:afterSwap', function(e){
        if(e.detail.target.id === 'dialog'){
            const dialogContent = document.querySelector('#dialog');
            dialogContent.style.maxHeight = '800px';
            dialogContent.style.overflowY = 'auto';
            dialogModal.show();
        }

    });

    document.body.addEventListener('popup', function(e){
        if(e.detail.success){
            popupIcon.className = 'fas fa-solid fas fa-check text-success mr-2';
        } else {
            popupIcon.className = 'fas fa-solid fas fa-close text-danger mr-2';
        }
        popupTitle.innerText = e.detail.title;
        popupMessage.innerText = e.detail.message;
        popup.show();
        dialogModal.hide();
    });

})();

document.addEventListener("DOMContentLoaded", function() {
    // Get the notification link
    var notificationLink = document.getElementById('notification-link');

    // Check if notificationLink is not null
    if (notificationLink) {
        // Add click event listener
        var onClick = function(event) {
            // Prevent default anchor behavior
            event.preventDefault();

            // Get CSRF token from cookies
            var csrftoken = getCookie('csrftoken');

            // Remove the event listener to prevent further clicks
            notificationLink.removeEventListener('click', onClick);

            // Make an AJAX request to mark the notification as read
            var xhr = new XMLHttpRequest();
            xhr.open('POST', "/webapps2024/notification/notification-seen/", true); // Replace 'mark-as-read' with your actual URL endpoint
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set CSRF token in request headers
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // Continue with setting hx-get, hx-trigger, and hx-swap attributes
                    setHxAttributes();
                } else {
                    // Handle error
                    console.error('Error marking notification as read');
                }
            };
            xhr.onerror = function () {
                // Handle error
                console.error('Error marking notification as read');
            };
            xhr.send();
        };

        // Add click event listener
        notificationLink.addEventListener('click', onClick);
    } else {
        console.error("Notification link element not found.");
    }

    // Function to set hx-get, hx-trigger, and hx-swap attributes based on notification type
    function setHxAttributes() {
        var notificationType = "{{ notification.type }}";
        var hxGetUrl;
        if (notificationType === 'MONREQ') {
            hxGetUrl = "{% url 'transfer-requests' %}";
        } else {
            hxGetUrl = "{% url 'transaction' %}";
        }

        // Set hx-get, hx-trigger, and hx-swap attributes
        notificationLink.setAttribute('hx-get', hxGetUrl);
        notificationLink.setAttribute('hx-trigger', 'load, popup from:body');
        notificationLink.setAttribute('hx-swap', 'outerHtml');
    }
});

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if cookie contains the name we're looking for
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
