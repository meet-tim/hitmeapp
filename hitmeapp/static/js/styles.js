const modal = document.querySelector(".modal")
const searchBtn = document.querySelectorAll(".fa-magnifying-glass")


searchBtn[0].parentElement.addEventListener("click",(e)=>{
    modal.style.opacity = "1";
    modal.style.transform = "translateX(0%)";

})

searchBtn[1].parentElement.addEventListener("click",(e)=>{
    modal.style.opacity = "1";
    modal.style.transform = "translateX(0%)";

})


document.addEventListener("click",(e)=>{
    if (e.target.classList.contains("modal") || e.target.classList.contains("fa-circle-xmark")){
        modal.style.opacity = "0";
        modal.style.transform = "translateX(100%)";
    }
   
})

