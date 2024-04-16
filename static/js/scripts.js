;(function(){
    const dialogModal=new bootstrap.Modal(document.getElementById('modal'))
    const toast=new bootstrap.Toast(document.getElementById('toast'))
    const toastTitle=document.getElementById('toast-title')
    const toastMessage=document.getElementById('toast-message')
    const toastIcon=document.getElementById('toast-icon')

    document.body.addEventListener('htmx:afterSwap',function(e){
        
        if(e.detail.target.id==='dialog'){
            dialogModal.show()          
        }
    })

    document.body.addEventListener('toast',function(e){
        if(e.detail.success){
            toastIcon.className='fas fa-solid fas fa-check text-success mr-2'
        }else{
            toastIcon.className='fas fa-solid fas fa-close text-danger mr-2'
        }
        toastTitle.innerText=e.detail.title
        toastMessage.innerText=e.detail.message
        toast.show()
        dialogModal.hide()
    })
})()