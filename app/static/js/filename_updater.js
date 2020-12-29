$('#upload-photo').change(function() {
    var i = $(this).prev('label').clone();
    var file = $('#upload-photo')[0].files[0].name;
    $(this).prev('label').text(file);
});