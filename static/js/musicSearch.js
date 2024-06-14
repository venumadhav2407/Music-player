
$(document).ready(function() {
    // Function to filter music list based on search input
    $('#searchinput').on('input', function(event) {
        var searchValue = $(this).val().toLowerCase(); // Get search query
        $('.tracks .song').each(function() {
            var title = $(this).find('.song_info #title').text().toLowerCase(); // Get title
            var artist = $(this).find('.song_info #artist').text().toLowerCase(); // Get artist
            // Check if any of the fields contain the search query
            if (title.includes(searchValue) || artist.includes(searchValue)) {
                $(this).show(); // Show the list item
            } else {
                $(this).hide(); // Hide the list item if not matched
            }
        });
    });
});
