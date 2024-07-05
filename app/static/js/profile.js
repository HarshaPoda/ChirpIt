function showFollowers() {
    var modal = document.getElementById("followers-modal");
    modal.style.display = "block";
}

function showFollowing() {
    var modal = document.getElementById("following-modal");
    modal.style.display = "block";
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    var followersModal = document.getElementById("followers-modal");
    var followingModal = document.getElementById("following-modal");
    if (event.target == followersModal) {
        followersModal.style.display = "none";
    }
    if (event.target == followingModal) {
        followingModal.style.display = "none";
    }
}
