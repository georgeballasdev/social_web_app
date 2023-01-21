var mouseX;
var mouseY;
const profilePopUp = $('#profile-popup');
const profile = $('#profile');
const profileCaret = profile.find('i');
const profileMenu = profile.find('#profile-menu');

$(document).mousemove( (e) => {
   mouseX = e.pageX; 
   mouseY = e.pageY;
});  

$(".pop-up").mouseenter( () => {
  profilePopUp.css({'top':mouseY-10,'left':mouseX-10});
  profilePopUp.toggle();
});

profilePopUp.mouseout( () => {
    profilePopUp.toggle();
});

profile.click( () => {
    profileCaret.toggleClass('fa-caret-up');
    profileCaret.toggleClass('fa-caret-down');
    profileMenu.toggleClass('hidden');
})