function fillPage(page) {
    $('#page').val(page);
    $('#page_form').submit();
}


function likeItem(itemType, itemId) {
    $.get('/user-activities/like-item/' + itemType + '/' + itemId).then(res => {
        Swal.fire({
            title: "You liked it",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "green",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function unLikeItem(itemType, itemId) {
    $.get('/user-activities/unlike-item/' + itemType + '/' + itemId).then(res => {
        Swal.fire({
            title: "You Unliked it",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "red",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function followChannel(item_id) {
    $.get('/user-activities/follow-item/' + item_id).then(res => {
        Swal.fire({
            title: "You follow it",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "green",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function unFollowChannel(item_id) {
    $.get('/user-activities/unfollow-item/' + item_id).then(res => {
        Swal.fire({
            title: "You Unfollow it",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "red",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function addToPlaylist(playlistId, itemSlug, itemType) {
    $.get('/user-activities/playlists-to-add/' + playlistId + '/' + itemType + '/' + itemSlug).then(res => {
        Swal.fire({
            title: "The Item is added, successfully",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "green",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function deletePlaylist(playlistId) {
    $.get('/user-panel/playlist-delete/' + playlistId).then(res => {
        Swal.fire({
            title: "The Playlist is deleted, successfully",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#d33",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function deletePlaylistItem(playlistSlug, itemId, itemType) {
    $.get('/user-panel/playlist-item-delete/' + playlistSlug + "/" + itemId + "/" + itemType).then(res => {
        Swal.fire({
            title: "The Item is deleted, successfully",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#d33",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function sendEpisodeComment(episodeId) {
    var comment = $('#CommentText').val();
    var parent_id = $('#parent_id').val();

    $.get('/user-activities/send-comment/', {
        comment_text: comment,
        episode_id: episodeId,
        parent_id: parent_id
    }).then(res => {
        $('#comments_area').html(res);
        $('#CommentText').val('');
        $('#parent_id').val('');
        Swal.fire({
            title: "The Comment is sent, successfully",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "green",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function deleteComment(commentId) {
    $.get('/user-activities/delete-comment/', {comment_id: commentId,}).then(res => {
        Swal.fire({
            title: "The Comment is Deleted, successfully",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "red",
            confirmButtonText: "Ok",

        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '';
            }
        });
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('start_form').scrollIntoView({behavior: "smooth"});
}
