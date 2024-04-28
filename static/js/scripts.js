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
